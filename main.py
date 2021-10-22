import pandas as pd
from azure.cli.core import get_default_cli

from config import column_count, url
from scraper import parse_table
from utils import get_az_regions_dict, get_ip_list_whitelist, fuzzy_name_matcher

if __name__ == '__main__':
    # step 1: parse the udr official website
    parsed_content_df = parse_table(url, 1, column_count)
    # step 2: get cli output to see all deployment format
    az_regions_dict = get_az_regions_dict()
    # step 3: add command line version of az region to parsed content, prepare terraform deployment
    parsed_content_df["az_region_to_deploy_fuzzy_match"] = parsed_content_df["region"].apply(
        lambda x: fuzzy_name_matcher(x, az_regions_dict))
    # step 4: compute domain resolution test and get ip list to whitelist
    parsed_content_df["whitelistips"] = parsed_content_df["value"].apply(
        lambda x: get_ip_list_whitelist(str(x)))
    parsed_content_df.to_csv("./outputs/result.csv")
