import pandas as pd
import pymc as pm
from pymc import distributions as dist

df = pd.read_csv('./data/fm_data.csv')

coords = {
    'team': df['team'].unique(),
    'players': df['name'].unique(),
    'position': df['position'].unique(),
    'country': df['Country'].unique(),
    'type': df['TYPE'].unique(),
    'extension': df['EXTENSION'].unique()
}

with pm.Model(coords=coords) as model:

    global_salary = pm.Normal('global_salary', 12, 3)

    salary_sigma = pm.HalfCauchy('salary_sigma', 5)
    y = pm.Cauchy('log_salary', alpha=global_salary, beta=salary_sigma, observed = df['L_Salary'])
    pm.model_to_graphviz(model)

with model:
    trace = model.sample(1000, 4)
    

