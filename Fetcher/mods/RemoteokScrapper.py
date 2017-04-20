__author__ = 'alrifqi'
import urllib2
import re

from bs4 import BeautifulSoup
from .GeneralUtils import work_insert_to_db

url = "http://remoteok.io"



class RemoteokScrapper():
    def get_work(self):
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "lxml")
        contents = soup.find_all("tr", class_="job")
        data = []
        for content in contents:
            temp_cont = {}
            job_id = self.get_job_id(content)
            company_detail = content.find(class_="company_and_position")
            jobtitle = content.findChild("h2")
            company = content.findChild("h3")
            urls = company_detail.find(class_='preventLink')
            description = soup.find(class_='expand-'+job_id)
            description = description.findChild('p')
            tags = content.find(class_="tags")
            tags = tags.find_all('h3')

            temp_cont['title'] = jobtitle.contents[0]
            temp_cont['company'] = company.contents[0]
            temp_cont['url'] = "http://remoteok.io"+urls['href']
            temp_cont['source'] = "http://remoteok.io"
            temp_cont['desc'] = self.clean_description(description.text)
            temp_cont['skill'] = self.extract_tags(tags)
            data.append(temp_cont)
        work_insert_to_db(data)


    def get_job_id(self, content):
        job_id = content.get('class')
        for temp_id in job_id:
            if 'job-' in temp_id:
                split_res = temp_id.split("-")
                return split_res[1]


    def clean_description(self, desc):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', desc)
        return cleantext


    def extract_tags(self, tags_data):
        result = ''
        for tag in tags_data:
            t = tag.text.replace('3>','')
            result = result + t + '|'
        return result[:-1]
