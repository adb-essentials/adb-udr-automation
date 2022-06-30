import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import desired_column_names


def parse_table(url: str, table_number: int, column_count: int) -> pd.DataFrame:
    # fetch raw html
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html")
    # save all tables into a list
    tables = soup.findChildren('table')
    # table_number from 0 to n-1, n=total number of tables in url
    rows = tables[table_number].findChildren(['th', 'tr'])

    # each time a value is None, its subsequent 2 values are lumped into the same list
    # major tables that contain important info are well formatted, with a fixed 3-column structure
    # first value extracted will always be a key (a region name)
    parsed_res = []

    for row in rows:
        cells = row.findChildren('td')
        # group every 3 elements
        for cell in cells:
            # need to fix for <br></br> and convert to ' and ' 
            value = cell.get_text(" and ")
            parsed_res.append(value)

    # Create list of lists, for 3-column structure table, using 3 as constant
    composite_list = [parsed_res[x:x+column_count]
                      for x in range(0, len(parsed_res), column_count)]
    previous_available_region = "seed_non_null"

    for each in composite_list:
        temp_region = each[0]
        if temp_region is '':
            # overwrite list value
            each[0] = previous_available_region
        else:
            # update previous available region value
            previous_available_region = each[0]
            continue

    df = pd.DataFrame.from_records(composite_list)
    # set column names
    df.columns = desired_column_names
    return df
