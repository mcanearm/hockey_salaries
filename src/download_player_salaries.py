"""
Downloading data code modified from
# https://datascience.stackexchange.com/questions/10857/how-to-scrape-a-table-from-a-webpage
"""

import pandas as pd
import bs4
import requests
import logging
import time
import numpy as np

logger = logging.getLogger(__name__)


def parse_column(col):
    logger.debug(f"Parsing {col}")
    try:
        return col.find("span")["data-num"]
    except TypeError:
        pass

    if ":" in col.text:
        m, s = col.text.split(":")
        return int(m) * 60 + int(s)
    else:
        return col.text.strip()


def parse_row(row, header):
    logger.debug(f"{row}")
    cols = row.findAll("td")
    return {colname: parse_column(col) for colname, col in zip(header, cols)}


def retrieve_dataframe_from_url(url, year, sleep_time=2):
    pg = 1
    season_results = []
    while pg < 35:
        params = {
            "stats-season": year,
            "pg": pg,
            "display": "weightkg,heightcm,caphit-percent",
        }
        r = requests.get(url, params=params)
        logger.info(r.url)

        time.sleep(sleep_time)

        players = bs4.BeautifulSoup(r.content, features="html.parser")
        column_header = players.find("tr", {"class": "column_head"}).findAll("th")
        rows = players.find("tbody").findAll("tr")
        if not rows or not column_header:
            break
        else:
            header = [c.text for c in column_header]
            all_rows = pd.DataFrame([parse_row(row, header) for row in rows])
            all_rows.columns = header
            all_rows["SEASON"] = f"{year - 1}-{year}"
            all_rows = all_rows.replace("-", np.nan)
            season_results.append(all_rows)
            pg += 1

    return pd.concat(season_results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    url = "https://www.capfriendly.com/browse/active"
    years = range(2022, 2010, -1)

    for year in years:
        salary_data = retrieve_dataframe_from_url(url, year)
        salary_data.to_csv(f'./data/salaries_{year}.csv', index=False)
