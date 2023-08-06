import re
from datetime import datetime, timezone

import requests
from typing import Any, Dict, Optional, Iterable
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_sec.core_scraper.scraper import scrap_company_report

sec_url = 'https://www.sec.gov'


def generate_timestamp(requested_timestamp_type):

    the_datetime = datetime.now(tz=timezone.utc)

    if requested_timestamp_type == 'hive':
        # TRINO and HIVE requires this format for native timestamps in parquet
        return round(int(the_datetime.timestamp()*1000000), -3)
    else:
        # POSTGRESQL
        return the_datetime.isoformat() + 'Z'


class TapSECStream(RESTStream):

    url_base = 'https://www.sec.gov/cgi-bin/browse-edgar'

    @property
    def http_headers(self) -> dict:

        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['HOST'] = 'www.sec.gov'

        return headers

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        ?CIK={}&owner=exclude&action=getcompany&type=13F-HR'
        """
        params: dict = {}

        params['CIK'] = context['cik_partition']
        params["owner"] = "exclude"
        params["action"] = "getcompany"
        params["type"] = "13F-HR"

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:

        current_query_time = generate_timestamp("hive")

        soup_xml, filing_date = scrap_company_report(response)

        issuers = soup_xml.body.findAll(re.compile('nameofissuer'))
        cusips = soup_xml.body.findAll(re.compile('cusip'))
        values = soup_xml.body.findAll(re.compile('value'))
        sshprnamts = soup_xml.body.findAll('sshprnamt')
        sshprnamttypes = soup_xml.body.findAll(re.compile('sshprnamttype'))
        investmentdiscretions = soup_xml.body.findAll(re.compile('investmentdiscretion'))
        soles = soup_xml.body.findAll(re.compile('sole'))
        shareds = soup_xml.body.findAll(re.compile('shared'))
        nones = soup_xml.body.findAll(re.compile('none'))

        for issuer, cusip, value, sshprnamt, sshprnamttype, investmentdiscretion, sole, shared, none in zip(issuers,
                                                                                                            cusips,
                                                                                                            values,
                                                                                                            sshprnamts,
                                                                                                            sshprnamttypes,
                                                                                                            investmentdiscretions,
                                                                                                            soles,
                                                                                                            shareds,
                                                                                                            nones):
            row = {
                "name_of_issuer": str(issuer.text),
                "cusip": str(cusip.text),
                "value": int(value.text)*1000,
                "shares_amount": int(sshprnamt.text),
                "shares_type": str(sshprnamttype.text),
                "investment_discretion": str(investmentdiscretion.text),
                "voting_sole": int(sole.text),
                "voting_shared": int(shared.text),
                "voting_none": int(none.text),
                "quarterly_reporting_date": filing_date,
                "query_start_time": current_query_time
            }

            yield row

