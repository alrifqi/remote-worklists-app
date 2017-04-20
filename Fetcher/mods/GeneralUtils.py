__author__ = 'alrifqi'
from Fetcher.models import Company, Work, Source

def work_insert_to_db(datas):
    for data in datas:
        company, created_company = Company.objects.get_or_create(name=data['company'])
        source, created_source = Source.objects.get_or_create(site=data['source'])
        w = Work(title=data['title'], skills=data['skill'], url=data['url'], source=source, company=company)
        w.save()
