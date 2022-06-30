import pandas as pd
import calendar
import time

from config import column_count, url
from scraper import parse_table
from utils import (fuzzy_name_matcher, get_az_regions_dict,
                   get_ip_list_whitelist, get_srvc_tag_count, get_srvc_tag_cidrs)

if __name__ == '__main__':
    # there are 2 tables to parse from the url
    gmt = time.gmtime()
    ts = str(calendar.timegm(gmt))
    tables = {"table1-" + ts: 1, "table2-" + ts: 2}
    for table_name, table_number in tables.items():
        # step 1: parse the udr official website, choose table 1 or 2
        parsed_content_df = parse_table(url, table_number, column_count)
        # step 2: get cli output to see all deployment format
        az_regions_dict = get_az_regions_dict()
        adb_service_tags = get_srvc_tag_cidrs()
        # step 3: add command line version of az region to parsed content, prepare terraform deployment
        parsed_content_df["az_region_to_deploy_fuzzy_match"] = parsed_content_df["region"].apply(
            lambda x: fuzzy_name_matcher(x, az_regions_dict))
        # step 4: compute domain resolution test and get ip list to whitelist
        parsed_content_df["whitelistips"] = parsed_content_df["value"].apply(
            lambda x: get_ip_list_whitelist(str(x), table_number))
        # step 5: determine if included in the service tag 
        parsed_content_df["is_in_service_tag"] = parsed_content_df["whitelistips"].apply(
            lambda x: get_srvc_tag_count(list(x), adb_service_tags))

        print(parsed_content_df.head())
        parsed_content_df.to_csv(
            f"./outputs/result_{table_name}.csv", index=False)
