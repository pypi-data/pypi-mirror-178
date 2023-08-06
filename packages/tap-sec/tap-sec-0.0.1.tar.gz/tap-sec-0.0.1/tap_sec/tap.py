from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_sec.streams import SECThirteenFStream

STREAM_TYPES = [
    SECThirteenFStream
]


class TapSEC(Tap):

    name = "tap-sec-filings"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "get_latest_only",
            th.BooleanType,
            required=True,
            secret=False,  # Flag config as protected.
            description="Do you want to retrieve the latest report ONLY"
        ),
        th.Property("user_agent", th.StringType, required=True)
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapSEC.cli()
