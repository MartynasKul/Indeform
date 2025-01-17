import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraper.models import Skelbimas
from django.db import connection

#pagalbine funkcija db id resetinimui
def reset_sequence(model):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{model._meta.db_table}';")

def getDetailedInfo(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
            
        detailSoup = BeautifulSoup(response.text, 'html.parser')
        
        # BVPZ kodu isgavimas
        cpvCodes = []
        cpvSection = detailSoup.find('div', string=lambda text: text and 'CPV codes:' in text)
        
        if cpvSection:
            # Pereina pr visus span, kurie turi text-underline klase
            cpvSpans = detailSoup.find_all('span', class_='text-underline')
            for span in cpvSpans:
                codeText = span.text.strip()
                # Pilno kodo atskyrimas per tarpa arba &nbsp;
                codeParts = codeText.split('\xa0')  # perskiria per &nbsp; (taip svetaineje padaryti tarpai sioje vietoje)
                if not codeParts:  # jeigu pirmas splitas neveikia, bandoma paprastai splittint
                    codeParts = codeText.split()

                if codeParts:  # jeigu padalinta, pirmoji splito dalis pridedama
                    fullCode = codeParts[0].strip()
                    cpvCodes.append(fullCode)
        
        return {
            'cpvCodes': cpvCodes
        }
        
    except Exception as e:
        print(f"Nepavyko gauti praplestos informacijos: {str(e)}")
        return None

def scrapePurchases(url, filterPurchaseType=None, filterAdType=None, filterStartDate=None, filterEndDate=None):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Nepavyko pasiekti puslapio: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        #duomenu isvalymas pries pradedant duomenu isgavima(naudojama kad 
        # filtravimas su filtrais filtruotu, o ne atnaujintu esancius duomenis)
        Skelbimas.objects.all().delete()
        reset_sequence(Skelbimas)

        #duomenu isgavimas is skelbimu
        ads = soup.find_all('div', class_='notice-search-item')
        
        for ad in ads:
            try:
                # Duomenu isgavimas is skelbimo
                header = ad.find('div', class_='notice-search-item-header')
                if not header:
                    continue

                # Gaunamas skelbimo pavadinimas ir nuoroda i detalia skelbimo informacija
                title = header.find('a').text.strip() if header.find('a') else ''
                extraLink = header.find('a')['href'] if header.find('a') else ''
                
                #Pirkejo pavadinimas bei nuoroda i ju puslapi
                buyerDiv = ad.find('div', class_='left-col')
                if buyerDiv:
                    buyerLink = buyerDiv.find('a')
                    if buyerLink:
                        buyer = buyerLink.text.strip()
                        link = buyerLink['href']
                    else:
                        buyer = ''
                        link = ''
                else:
                    buyer = ''
                    link = ''
                
                #Skelbimo tipo gavimas
                typeOfAdDiv = ad.select_one('div:contains("Skelbimo tipas:")')
                if typeOfAdDiv:
                    # <strong> suradimas dive
                    typeOfAdStrong = typeOfAdDiv.find('strong')
                    typeOfAd = typeOfAdStrong.text.strip() if typeOfAdStrong else ''
                else:
                    typeOfAd = ''

                # Skelbimo sukurimo data
                creationDiv = ad.find('div', string=lambda text: text and 'Paskelbimo data:' in text if text else False)
                if creationDiv:
                    # Datos atskyrimas nuo teksto po ':' ir tarpų panaikinimas
                    creationDate = creationDiv.text.split(':')[1].strip()

                # Termino datos gavimas
                deadline = None
                # Bandomi keli  variantai, jeigu kuris nors neveiktu :P
                deadlineDiv = ad.find('div', class_='label-info') or \
                            ad.find('span', class_='label-info') or \
                            ad.find('div', string=lambda text: text and 'Pasiūlymų pateikimo terminas:' in text if text else False)
                
                if deadlineDiv:
                    if ':' in deadlineDiv.text:
                        deadline = deadlineDiv.text.split(':')[1].strip()
                    else:
                        deadline = deadlineDiv.text.strip()

                # Pavertimas is datetime i date
                try:
                    creationDate = datetime.strptime(creationDate, '%Y-%m-%d').date() if creationDate else None
                except ValueError:
                    try:
                        # jei nepavyko paversti i date, perduodama kaip datetime
                        creationDate = datetime.strptime(creationDate, '%Y-%m-%d %H:%M:%S').date() if creationDate else None
                    except ValueError:
                        creationDate = None

                try:
                    deadlineDate = datetime.strptime(deadline, '%Y-%m-%d').date() if deadline else None
                except ValueError:
                    try:
                        deadlineDate = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S').date() if deadline else None
                    except ValueError:
                        print(f"Could not parse deadline date: {deadline}")
                        deadlineDate = None

                detailedInfo = getDetailedInfo(extraLink) if extraLink else None
                #Filtravimas 

                # Filtravimas pagal data
                if filterStartDate and creationDate:
                    filterStart = datetime.strptime(filterStartDate, '%Y-%m-%d').date()
                    if creationDate < filterStart:
                        continue

                if filterEndDate and deadlineDate: 
                    filterDeadline = datetime.strptime(filterEndDate, '%Y-%m-%d').date()
                    if deadlineDate > filterDeadline:
                        continue

                if filterAdType and typeOfAd:
                    if str(typeOfAd) != str(filterAdType):
                        continue
                
                
                # filtras filtruoja pagal bvpz, nes scrapinant duomenis neradau kur yra pirkimo tipas :(( 
                #P.S. Po papildomu testavimu gali buti kad sis filtravimas neveikia
                if filterPurchaseType and detailedInfo.get('cpvCodes', []):
                    if filterPurchaseType in detailedInfo.get('cpvCodes', []):
                        continue

                # gaunama papildoma informacija is detalios informacijos puslapio (tiktai BVPZ kodai)
               
                
                # Debug print
                print(f"""Nuskaityta informacija:
                    Pavadinimas: {title}
                    Pirkejas: {buyer}
                    Nuoroda: {link}
                    Sukurimo data: {creationDate}
                    Terminas: {deadlineDate}
                    CPV kodai: {detailedInfo.get('cpvCodes', []) if detailedInfo else []}
                    Skelbimo tipas: {typeOfAd}
                    Papildomos info nuoroda: {extraLink}
                """)

                #informacijso saugojimas i db naudojant skelbimo pavadinima kaip unikalu raktą
                Skelbimas.objects.update_or_create(
                    pavadinimas = title,
                    defaults={
                        
                        'vykdytojoPavadinimas': buyer,
                        'nuoroda': link,
                        'data': creationDate,
                        'terminas': deadlineDate,
                        'bvpzKodas': detailedInfo.get('cpvCodes', []) if detailedInfo else [],
                        'skelbimoTipas': typeOfAd,
                    }
                )
            except Exception as e:
                print(f"Error processing entry {title}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error in main scraping function: {str(e)}")
        raise