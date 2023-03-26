import pandas as pd
import bs4
import requests


def parse_row(row):
    cols = row.findAll("td")
    col_data = {x["data-stat"]: x.text.strip() for x in cols}

    try:
        player = row.find("a").text
    except AttributeError:
        player_last, player_first = row.find("th").text.split(", ")
        player = f"{player_first} {player_last}"

    return {"player": player, **col_data}


if __name__ == "__main__":
    base_url = "https://www.hockey-reference.com/friv/current_nhl_salaries.cgi"
    r = requests.get(base_url)

    # https://datascience.stackexchange.com/questions/10857/how-to-scrape-a-table-from-a-webpage
    players = bs4.BeautifulSoup(r.content)
    rows = players.find("tbody").findAll("tr")

    all_rows = pd.DataFrame(map(parse_row, rows))
    all_rows[["salary", "caphit"]] = (
        all_rows[["salary", "caphit"]]
        .apply(lambda x: x.replace("[^0-9]", "", regex=True))
        .astype(int)
    )

    all_rows.to_csv("./data/player_salaries_2022.csv", index=False)
