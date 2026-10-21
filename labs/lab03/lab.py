# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):
    cols = ['first name', 'last name', 'current company', 'job title', 'email', 'university']
    dirname = Path(dirname)
    dframes = []
    for filepath in dirname.iterdir():
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip().str.lower().str.replace('_', ' ')
        dframes.append(df[cols])
    out = pd.concat(dframes, ignore_index=True)
    for c in cols:
        out[c] = out[c].str.strip()
    return out


def com_stats(df):
    ohio_uni = df[df['university'].str.contains('Ohio', na=False)]
    prop = ohio_uni['job title'].str.contains('Programmer', na=False).mean()

    job_titles = df['job title'].dropna()
    eng = job_titles[job_titles.str.endswith('Engineer')].nunique()

    max_title = job_titles.loc[job_titles.str.len().idxmax()]

    managers = job_titles[job_titles.str.lower().str.contains('manager', na=False)].sum()

    return [prop, eng, max_title, managers]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    dirname = Path(dirname)
    files = [fp for fp in dirname.iterdir()]
    files.sort(key=lambda fp: (len(fp.name), fp.name))
    dataframe = []
    
    for file in files:
        dataframe.append(pd.read_csv(file, index_col='id'))
    return pd.concat(dataframe, axis=1)


def check_credit(df):
    pts = df.drop(columns='name')
    answered = pts.notna() & (pts != '(no genres listed)')
    indiv = (answered.mean(axis=1) >= 0.5) * 5
    class_cred = min((answered.mean() >= 0.9).sum(), 2)

    return pd.DataFrame({'name' : df['name'], 'ec' : indiv + class_cred})


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    df = pets.merge(procedure_history, on='PetID')
    return df['ProcedureType'].value_counts().idxmax()

def pet_name_by_owner(owners, pets):
    pet_name = pets.groupby('OwnerID')['Name'].apply(lambda names: names.iloc[0] if len(names) == 1 else list(names))
    merged = owners.merge(pet_name.rename('PetName'), on='OwnerID')
    return merged.set_index('Name')['PetName']

def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    merged = (owners.merge(pets, on='OwnerID', how='left')
    .merge(procedure_history, on='PetID', how='left')
    .merge(procedure_detail, on=['ProcedureType', 'ProcedureSubCode'], how='left'))
    return merged.groupby('City')['Price'].sum()


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(sales):
    return sales.groupby('Name')[['Total']].mean().rename(columns = {'Total': 'Average Sales'})
    

def product_name(sales):
    return sales.pivot_table(index = 'Name', columns = 'Product', values = 'Total', aggfunc = 'sum')

def count_product(sales):
    return sales.pivot_table(index = ['Product', 'Name'], columns = 'Date', values = 'Total', aggfunc = 'count', fill_value = 0)

def total_by_month(sales):
    month = pd.to_datetime(sales['Date'], format='%m.%d.%Y').dt.month_name()
    return sales.assign(Month=month).pivot_table(index = ['Name', 'Product'], columns = 'Month', values = 'Total', aggfunc = 'sum', fill_value = 0)
