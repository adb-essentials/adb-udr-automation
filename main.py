import pandas as pd
from azure.cli.core import get_default_cli

from config import column_count, url
from scraper import parse_table
from utils import get_az_regions_dict, get_ip_list_whitelist

if __name__ == '__main__':
    parsed_content_df = parse_table(url, 1, column_count)

    az_regions_dict = get_az_regions_dict()

    print(parsed_content_df.head())

    print(az_regions_dict)

    print(get_ip_list_whitelist(
        "consolidated-australiaeast-prod-metastore.mysql.database.azure.com"))
