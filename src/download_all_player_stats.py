import pandas as pd
import requests
import io
import time
import logging


logger = logging.getLogger(__name__)


def retrieve_url(url, wait=10):
    logger.info(f"Retrieving {url}.")
    r = requests.get(url)

    logger.info(f"Sleeping for {wait} seconds...")
    time.sleep(wait)
    with io.StringIO(r.content.decode("utf-8")) as f:
        skater_stats = pd.read_csv(f)
    return skater_stats


if __name__ == "__main__":

    logging.basicConfig(level = logging.INFO)
    urls = [
        f"https://moneypuck.com/moneypuck/playerData/seasonSummary/{year}/regular/skaters.csv"
        for year in range(2009, 2023)
    ]

    all_data_sets = [retrieve_url(url) for url in urls]
    pd.concat(all_data_sets).to_csv("./data/all_player_data.csv")
