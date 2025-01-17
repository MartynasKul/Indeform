from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Skelbimas 
from .utils import scrapePurchases  
from django.core.management import call_command

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def triggerScrape(request):
    urlType=request.data.get('urlType', 'default')

    urls = {
        'default': 'https://cvpp.eviesiejipirkimai.lt/?pageNumber=1&pageSize=1000',
        'other': 'https://cvpp.eviesiejipirkimai.lt/',
    }

    filters = {
        '_url': request.data.get('url', 'https://cvpp.eviesiejipirkimai.lt/?pageNumber=1&pageSize=1000'),
        '_created': request.data.get('created'),
        '_deadline': request.data.get('deadline'),
        '_adType': request.data.get('adType'),
        '_purchaseType': request.data.get('purchaseType'),
    }
    try:
        call_command(
            'scrapePurchases',
            url=filters['_url'],
            created=filters['_created'],
            deadline=filters['_deadline'],
            adType=filters['_adType'],
            purchaseType=filters['_purchaseType'],

        )

        return Response({"message": "Nuskaitymas pavyko", "Panaudoti filtrai:" : filters})
    except Exception as e:
        return Response({"message": f"Problema: {e}"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getScrapedData(request):

    createdDate = request.query_params.get('createdDate')
    deadline = request.query_params.get('deadline')
    adType = request.query_params.get('adType')
    # purchaseType = request.query_params.get('purchaseType')

    querySet = Skelbimas.objects.all()

    if createdDate:
        querySet = querySet.filter(data_gte=createdDate)
    if deadline:
        querySet = querySet.filter(terminas_lte=deadline)
    if adType:
        querySet = querySet.filter(skelbimoTipas=adType)
    # if purchaseType:
    #     querySet = querySet.filter(pirkimoTipas=purchaseType)


    data_list = [
        {
            'id': item.id,
            'pavadinimas': item.pavadinimas,
            'vykdytojoPavadinimas': item.vykdytojoPavadinimas,
            'nuoroda': item.nuoroda,
            'data': item.data,
            'terminas': item.terminas,
            'bvpzKodas': item.bvpzKodas,
            'skelbimoTipas': item.skelbimoTipas,
        }
        for item in querySet
    ]
    return Response(data_list)