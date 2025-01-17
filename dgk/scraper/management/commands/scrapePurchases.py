from django.core.management.base import BaseCommand
from scraper.utils import scrapePurchases

class Command(BaseCommand):
    help= ' Nuskaityti informacija is duotos svetaines'
    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='https://cvpp.eviesiejipirkimai.lt/?pageNumber=1&pageSize=1000')
        parser.add_argument('--purchaseType', type=str, required=False)
        parser.add_argument('--adType', type=str, required=False)
        parser.add_argument('--created', type=str, required=False)
        parser.add_argument('--deadline', type=str, required=False)

    def handle(self, *args, **options):
        url=options['url']
        self.stdout.write(f"Skaitoma informacija is {url}")

        scrapePurchases(
            url=url,
            filterPurchaseType=options['purchaseType'], 
            filterAdType=options['adType'], 
            filterStartDate=options['created'], 
            filterEndDate=options['deadline']
        )

        self.stdout.write("Nuskaityti pavyko")