import requests
import pandas as pd
import bs4


url = "https://www.capfriendly.com/income-tax-calculator/870000/capitals"

r = requests.get(url)
soup = bs4.BeautifulSoup(r.content)

html_table = soup.find("table", {"id": "ptc"})
table_headers = [
    x.text
    for x in html_table.find("thead")
    .find("tr", {"class": "column_head"})
    .findAll("th", {"class": "center"})
]

table_body = html_table.find("tbody")


def parse_row(row):
    team_name = row.find("td").text
    est_tax_rate = int(row["data-sort-est_tax_rate"]) / 1000
    return team_name, est_tax_rate


table_rows = table_body.findAll("tr")
team_tax_rates = pd.DataFrame(map(parse_row, table_rows)).set_axis(
    ["Team", "EffTaxRate"], axis=1
)

# manually create some team metadata
# Team Name, Abbrev, State/Prov, Country, Conference, Division, O6,
team_location_data = [
    ("Anaheim Ducks", "ANA", "CA", "USA", "Western", "Pacific", False),
    ("Arizona Coyotes", "ARI", "AZ", "USA", "Western", "Central", False),
    ("Boston Bruins", "BOS", "MA", "USA", "Eastern", "Atlantic", True),
    ("Buffalo Sabres", "BUF", "NY", "USA", "Eastern", "Atlantic", False),
    ("Calgary Flames", "CGY", "AB", "CA", "Western", "Pacific", False),
    ("Carolina Hurricanes", "CAR", "NC", "USA", "Eastern", "Metropolitan", False),
    ("Chicago Blackhawks", "CHI", "IL", "USA", "Western", "Central", True),
    ("Colorado Avalanche", "COL", "CO", "USA", "Western", "Central", False),
    ("Columbus Blue Jackets", "CBJ", "OH", "USA", "Eastern", "Metropolitan", False),
    ("Dallas Stars", "DAL", "TX", "USA", "Western", "Central", False),
    ("Detroit Red Wings", "DET", "MI", "USA", "Eastern", "Atlantic", True),
    ("Edmonton Oilers", "EDM", "AB", "CA", "Western", "Pacific", False),
    ("Florida Panthers", "FLA", "FL", "USA", "Eastern", "Atlantic", False),
    ("Los Angeles Kings", "LAK", "CA", "USA", "Western", "Pacific", False),
    ("Minnesota Wild", "MIN", "MN", "USA", "Western", "Central", False),
    ("Montreal Canadiens", "MTL", "QC", "CA", "Eastern", "Atlantic", True),
    ("Nashville Predators", "NSH", "TN", "USA", "Western", "Central", False),
    ("New Jersey Devils", "NJD", "NJ", "USA", "Eastern", "Metropolitan", False),
    ("New York Rangers", "NYR", "NY", "USA", "Eastern", "Metropolitan", True),
    ("New York Islanders", "NYI", "NY", "USA", "Eastern", "Metropolitan", False),
    ("Ottawa Senators", "OTT", "ON", "CA", "Eastern", "Atlantic", False),
    ("Philadelphia Flyers", "PHI", "PA", "USA", "Eastern", "Metropolitan", False),
    ("Pittsburgh Penguins", "PIT", "PA", "USA", "Eastern", "Metropolitan", False),
    ("San Jose Sharks", "SJS", "CA", "USA", "Western", "Pacific", False),
    ("Seattle Kraken", "SEA", "WA", "USA", "Western", "Pacific", False),
    ("St. Louis Blues", "STL", "MO", "USA", "Western", "Central", False),
    ("Tampa Bay Lightning", "TBL", "FL", "USA", "Eastern", "Atlantic", False),
    ("Toronto Maple Leafs", "TOR", "ON", "CA", "Eastern", "Atlantic", True),
    ("Vancouver Canucks", "VAN", "BC", "CA", "Western", "Pacific", False),
    ("Vegas Golden Knights", "VGK", "NV", "USA", "Western", "Pacific", False),
    ("Washington Capitals", "WSH", "DC", "USA", "Eastern", "Metropolitan", False),
    ("Winnipeg Jets", "WPG", "MB", "CA", "Western", "Central", False),
]

loc_data = pd.DataFrame(team_location_data).set_axis(
    ["Team", "Abbr", "State/Prov", "Country", "Conference", "Division", "O6"], axis=1
)

team_metadata = loc_data.merge(team_tax_rates, how="left", on="Team")

team_metadata.to_csv("./data/team_metadata.csv", index=False)
