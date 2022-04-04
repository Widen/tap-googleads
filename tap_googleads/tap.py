"""GoogleAds tap class."""

import datetime
from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_googleads.streams import (
    CustomerStream,
    CampaignsStream,
    AdGroupsStream,
    AdGroupsPerformance,
    AccessibleCustomers,
    CustomerHierarchyStream,
    CampaignPerformance,
    CampaignPerformanceByAgeRangeAndDevice,
    CampaignPerformanceByGenderAndDevice,
    CampaignPerformanceByLocation,
    GeotargetsStream,
    ConversionsByLocation,
    CustomReport,
)

STREAM_TYPES = [
    CustomerStream,
    CampaignsStream,
    AdGroupsStream,
    AdGroupsPerformance,
    AccessibleCustomers,
    CustomerHierarchyStream,
    CampaignPerformance,
    CampaignPerformanceByAgeRangeAndDevice,
    CampaignPerformanceByGenderAndDevice,
    CampaignPerformanceByLocation,
    GeotargetsStream,
    ConversionsByLocation,
]


class TapGoogleAds(Tap):
    """GoogleAds tap class."""

    name = "tap-googleads"

    # TODO: Add Descriptions
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
        ),
        th.Property(
            "developer_token",
            th.StringType,
            required=True,
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            required=True,
        ),
        th.Property(
            "customer_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "login_customer_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "start_date",
            th.StringType,
            required=False,
            default=datetime.date.today().isoformat(),
        ),
        th.Property(
            "end_date",
            th.StringType,
            required=False,
            default=datetime.date.today().isoformat(),
        ),
        th.Property(
            "custom_reports",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "name",
                        th.StringType,
                        required=True,
                    ),
                    th.Property(
                        "gaql",
                        th.StringType,
                        required=True,
                    ),
                    th.Property(
                        "primary_keys_jsonpaths",
                        th.ArrayType(th.StringType),
                        required=True,
                    ),
                    th.Property(
                        "primary_keys",
                        th.ArrayType(th.StringType),
                        required=False,
                        default=["_sdc_primary_key"],
                    ),
                    th.Property(
                        "replication_key",
                        th.StringType,
                        required=False,
                        default=None
                    ),
                    th.Property(
                        "schema_filepath",
                        th.StringType,
                        required=True,
                    ),
                )
            ),
            required=False,
            default=datetime.date.today().isoformat(),
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        default_streams = [stream_class(tap=self) for stream_class in STREAM_TYPES]

        custom_reports = self.config.get("custom_reports")
        custom_report_streams = []
        if custom_reports:
            for report in custom_reports:
                custom_report_streams.append(
                    CustomReport(
                        tap=self,
                        name=report["name"],
                        gaql=report["gaql"],
                        primary_keys_jsonpaths=report["primary_keys_jsonpaths"],
                        primary_keys=report["primary_keys"],
                        replication_key=report.get("replication_key"),
                        schema_filepath=report["schema_filepath"],
                    )
                )

        return default_streams + custom_report_streams
