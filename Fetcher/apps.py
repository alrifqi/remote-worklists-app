from __future__ import unicode_literals

from django.apps import AppConfig

from Fetcher.mods.RemoteokScrapper import RemoteokScrapper
from Fetcher.models import Company

class FetcherConfig(AppConfig):
    name = 'Fetcher'

# class Worker():
def fetch_works(self):
    try:
        ro = RemoteokScrapper()
        company = Company.objects.create(name='2nd Reza Corp')
    except Exception as err:
        print("error")

def work_insert_to_db(self, datas):
    for data in datas:
        print(data)