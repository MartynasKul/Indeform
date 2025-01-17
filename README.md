# Indeform praktikos bandomoji uzduotis
 Indeform praktikos bandomoji uzduotis


Analyzeris - frontend dalis padaryta su Vuejs 3, typescript ir tailwindcss
dgk - django python backend ir duomenų gavybos komponentas :)

duomenų gavybos komponentas įdomus reikalas, jeigu teisingai supratau, čia turi būti web scraperis.
Filtravimo turbūt neteisingai supratau arba ne taip padariau, nes filtravimas pagal kodą neitin funkcionuoja, filtravimas pagal sukūrimo datą, terminą, skelbimo tipą veikia (kiek testavau)


# Norint pasibandyti backend/frontend funkcionalumą:

Atsidaryti du VS Code langus, viename atsidaryti dgk aplanką, kitame analyzeris aplanką.

dgk aplanko instrukcija
```bash
# Paleisti backend serveri
python manage.py runserver
```
analyzeris aplanko instrukcija
```bash
#Atsidyti vidini analyzeris aplanką
cd analyzeris

#Įsirašyti/pasitikrinti bibliotekas su
npm install

#Paleisti frontend
npm run dev
```
