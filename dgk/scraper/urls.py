from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.triggerScrape, name='triggerScrape'),
    path('data/', views.getScrapedData, name='getData'),
]