import pandas as pd
import pathlib

player_salary_files = list(pathlib.Path('./data').glob('salaries_*.csv'))
all_salaries = pd.concat(map(pd.read_csv, player_salary_files))

all_salaries['PLAYER'] = all_salaries['PLAYER'].replace('[0-9\.]', '', regex=True)
all_salaries[['CAP HIT', 'SALARY']] = all_salaries[['CAP HIT', 'SALARY']].replace('[^0-9]', '', regex=True)

all_salaries['CAP HIT %'] = all_salaries['CAP HIT %'].str.replace('%', '').astype(float).div(100)

all_salaries.to_csv('./data/all_salaries_cleaned.csv', index=False)

