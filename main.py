import pandas as pd
from azure.cli.core import get_default_cli

from config import column_count, url
from scraper import parse_table
from utils import get_az_regions_dict, get_ip_list_whitelist, fuzzy_name_matcher

if __name__ == '__main__':
    parsed_content_df = parse_table(url, 1, column_count)

    az_regions_dict = get_az_regions_dict()

    print(parsed_content_df.head())

    print(az_regions_dict)

    res = fuzzy_name_matcher("Australia cenio", az_regions_dict)
    print(get_ip_list_whitelist(
        "consolidated-australiaeast-prod-metastore.mysql.database.azure.com"))

    # add command line version of az region to parsed content, prepare terraform deployment
    parsed_content_df["az_region_to_deploy_fuzzy_match"] = parsed_content_df["region"].apply(
        lambda x: fuzzy_name_matcher(x, az_regions_dict))

    print(parsed_content_df.head())
