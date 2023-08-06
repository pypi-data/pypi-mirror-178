import re
import calendar
import datetime
import requests
from bs4 import BeautifulSoup

sec_url = 'https://www.sec.gov'


def get_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'HOST': 'www.sec.gov',
    }
    return requests.get(url, headers=headers)


def scrap_report_by_url(url):
    response_two = get_request(url)
    soup_two = BeautifulSoup(response_two.text, "html.parser")
    tags_two = soup_two.findAll('a', attrs={'href': re.compile('xml')})
    xml_url = tags_two[3].get('href')

    response_xml = get_request(sec_url + xml_url)
    soup_xml = BeautifulSoup(response_xml.content, "lxml")

    # DERIVE THE FILING PERIOD
    filing_soup = soup_two.find_all("div", {"class": "formGrouping"})
    filing_timestamp = ""
    for item in filing_soup:
        if "Period of Report" in item.text:
            sub_soup = item.find_all("div", {"class": "info"})
            filing_date_str = sub_soup[0].text
            timestamp1 = calendar.timegm(datetime.datetime.strptime(filing_date_str, "%Y-%m-%d").timetuple())
            filing_timestamp = int(timestamp1*1000000)

    return soup_xml, filing_timestamp


def scrap_company_report(response):
    # Find mutual fund by CIK number on EDGAR

    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.findAll('a', id="documentsbutton")
    last_report = (sec_url + tags[0]['href'])

    soup_xml, filing_date = scrap_report_by_url(last_report)

    return soup_xml, filing_date
