from django.shortcuts import render


from Fetcher.models import Company
from Fetcher.mods.RemoteokScrapper import RemoteokScrapper
# Create your views here.


def fetch_works():
    ro = RemoteokScrapper()
    ro.get_work()


def work_insert_to_db(datas):
    for data in datas:
        print(data)

fetch_works()