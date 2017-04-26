__author__ = 'alrifqi'
import requests
from lxml import html
import json
import urllib
from time import sleep
import re

from bs4 import BeautifulSoup
from .GeneralUtils import work_insert_to_db


class AngellistScrapper():
    def __init__(self):
        self.session_requests = requests.session()
        self.login_url = "https://angel.co/users/login"
        self.payload = {
            "username": "angellist@vpsorg.pro",
            "password": "abcd1234",
            "authenticity_token": ""
        }
        self.job_listing_urls = "https://angel.co/job_listings/startup_ids"


    def get_job(self):
        result = self.session_requests.get(self.login_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]
        self.payload["authenticity_token"] = authenticity_token
        cookie = self.session_requests.post(
            self.login_url,
            data = self.payload,
            headers = dict(referer="https://angel.co/login")
        )

        if cookie.status_code == 200:
            page_jobs = self.session_requests.get("https://angel.co/jobs")
            tree = html.fromstring(result.text)
            authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]
            headers = {"referer": "https://angel.co/jobs",
                       "Origin": "https://angel.co",
                       "X-CSRF-Token": authenticity_token,
                       }

            result_jobs = self.session_requests.post(
                "https://angel.co/job_listings/startup_ids",
                data = {
                    "tab": "find",
                    "filter_data[remote]": 1
                },
                headers = {"referer":"https://angel.co/jobs",
                           "Origin":"https://angel.co",
                           "X-CSRF-Token":authenticity_token,
                           "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                           "X - Requested - With": "XMLHttpRequest",
                },
                cookies=cookie.cookies
            )
            result_jobs = json.loads(result_jobs.text)
            flats = []
            [flats.append(x) for sublist in result_jobs['listing_ids'] for x in sublist if x not in flats]
            company_list = ""
            i = 0
            for flat in flats:
                company_list += urllib.urlencode({"startup_ids[]":flat})+"&"
                i += 1
                page = 1
                if i>=100:
                    company_jobs = self.session_requests.get(
                        "https://angel.co/job_listings/browse_startups_table?"+company_list+"&promotion_event_id=false&tab=find&page="+str(page),
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 ("
                                               "KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                                 },
                        cookies=cookie.cookies
                    )
                    i = 0
                    page += 1
                    if company_jobs.status_code == 200:
                        self.extract_work(company_jobs)
                    sleep(3)


    def extract_work(self, data):
        soup = BeautifulSoup(data.text, "lxml")
        contents = soup.find_all("div", class_="browse_startups_table_row")
        data = []
        for content in contents:
            temp_cont = {}
            name = content.find(class_='startup-link')
            job_box = content.find(class_='details')
            job_box = job_box.find(class_='jobs')
            job_lists = job_box.find(class_='listing-row')
            if job_lists is not None:
                for job in job_lists:
                    temp_cont = {}
                    title = job.find('a')
                    if hasattr(title, 'contents'):
                        # print job_lists
                        temp_cont['title'] = title.contents[0]
                        temp_cont['url'] = title['href']
                        temp_cont['source'] = "http://angel.co"
                        tags = job_box.find('div', class_='tags')
                        temp_cont['skill'] = self.clean_tags(tags.text)
                        temp_cont['desc'] = ''
                        data.append(temp_cont)
                work_insert_to_db(data)

    def clean_description(self, desc):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', desc)
        return cleantext

    def clean_tags(self, tags):
        tags = tags.encode('ascii','ignore')
        tag = tags.replace(" \xb7 ",",")
        return tag