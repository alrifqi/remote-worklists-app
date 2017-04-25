__author__ = 'alrifqi'
import requests
from lxml import html
import json
import urllib


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
            flats = [x for sublist in result_jobs['listing_ids'] for x in sublist]

            company_list = ""
            for flat in flats:
                company_list += urllib.urlencode({"startup_ids[]":flat})+"&"
            company_jobs = self.session_requests.get(
                "https://angel.co/job_listings/browse_startups_table?"+company_list,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 ("
                                       "KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                         },
                cookies=cookie.cookies
            )