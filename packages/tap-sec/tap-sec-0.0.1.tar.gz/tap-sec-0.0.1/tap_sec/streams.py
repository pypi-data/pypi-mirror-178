from singer_sdk import typing as th  # JSON Schema typing helpers
from tap_sec.client import TapSECStream


class SECThirteenFStream(TapSECStream):

    name = "sec-13f"
    path = "/sec13f"
    primary_keys = ["cusip", "reporting_date"]
    replication_key = None

    partitions = [{"cik_partition": [1037389]}]  # Hard coded to query Renaissance Technologies

    schema = th.PropertiesList(
        th.Property("name_of_issuer", th.StringType),
        th.Property("cusip", th.StringType),
        th.Property("value", th.IntegerType),
        th.Property("shares_amount", th.IntegerType),
        th.Property("shares_type", th.StringType),
        th.Property("investment_discretion", th.StringType),
        th.Property("voting_sole", th.IntegerType),
        th.Property("voting_shared", th.IntegerType),
        th.Property("voting_none", th.IntegerType),
        th.Property("quarterly_reporting_date", th.IntegerType),
        th.Property("query_start_time", th.IntegerType)

    ).to_dict()
