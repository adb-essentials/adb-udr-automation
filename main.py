import pandas as pd

from config import column_count, url
from scraper import parse_table

if __name__ == '__main__':
    df = parse_table(url, 1, column_count)
    print(df.head())