__author__ = 'alrifqi'
import requests
from lxml import html

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
        result = self.session_requests.post(
            self.login_url,
            data = self.payload,
            headers = dict(referer="https://angel.co/login")
        )