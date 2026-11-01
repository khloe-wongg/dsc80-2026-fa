# project.py


import pandas as pd
import numpy as np
np.set_printoptions(threshold=20, suppress=True, legacy='1.21')

from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pd.options.plotting.backend = 'plotly'

from IPython.display import display

# DSC 80 preferred styles
pio.templates["dsc80"] = go.layout.Template(
    layout=dict(
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=True,
        width=600,
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5, xanchor="center"),
    )
)
pio.templates.default = "simple_white+dsc80"
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_loans(loans):
    out = loans.copy()
    out['emp_title'] = out['emp_title'].str.strip().str.lower().replace('rn', 'registered nurse')
    out['issue_d'] = pd.to_datetime(loans['issue_d'], format = "%b-%Y")
    out['term'] = out['term'].str.split().str[0].astype(int)
    out['term_end'] = out.apply(lambda row: row['issue_d'] + pd.DateOffset(months = row['term']), axis = 1)

    return out


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def correlations(df, pairs):
    lst = []
    idxs = []
    for tup in pairs:
        idxs.append("r_" + tup[0] + "_" + tup[1])
        corrcoef = np.corrcoef(df[tup[0]].to_numpy(), df[tup[1]].to_numpy())[0, 1]
        lst.append(corrcoef)
    return pd.Series(lst, index = idxs)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_boxplot(loans):
    df = loans.copy()
    edges = [580, 670, 740, 800, 850]
    df['Credit Score Range'] = pd.cut(loans['fico_range_low'], bins = edges, right=False).astype(str)
    df['Loan Length (Months)'] = df['term'].astype(str)
    order = ['[580, 670)', '[670, 740)', '[740, 800)', '[800, 850)']

    fig = px.box(
        df,
        x='Credit Score Range',
        y='int_rate',
        color='Loan Length (Months)',
        color_discrete_map={'36': 'blue', '60': 'red'},
        category_orders={
            'Credit Score Range': order,
            'Loan Length (Months)': ['36', '60'],
        },
        labels={'int_rate': 'Interest Rate (%)'},
        title='Interest Rate vs. Credit Score',
    )
    fig.update_layout(title_x=0.5)
    return fig


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def ps_test(loans, N):
    has_ps = loans['desc'].notna().to_numpy()
    rates = loans['int_rate'].to_numpy()
    observed = rates[has_ps].mean() - rates[~has_ps].mean()
    differences = []
    for _ in range(N):
        shuffled = np.random.permutation(has_ps)
        difference = rates[shuffled].mean() - rates[~shuffled].mean()
        differences.append(difference)
    return (differences >= observed).mean()
    
def missingness_mechanism():
    return 2
    
def other_missingness():
    return 2


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def tax_owed(income, brackets):
    tax_total = 0
    i = 0
    while i + 1 < len(brackets) and income > brackets[i+1][1]:
        tax_total += (brackets[i+1][1] - brackets[i][1]) * brackets[i][0]
        i += 1
    tax_total += (income - brackets[i][1]) * brackets[i][0]
    return tax_total


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(state_taxes_raw): 
    state_taxes_raw = state_taxes_raw.dropna(how='all').copy()
    states = state_taxes_raw['State'].mask(state_taxes_raw['State'].str.startswith('(', na=False))
    state_taxes_raw['State'] = states.ffill()

    rate = state_taxes_raw['Rate'].astype(str).str.strip()
    rate = rate.str.replace('none', '0%', regex=False)
    rate = rate.str.replace('%', '', regex=False).astype(float) / 100
    state_taxes_raw['Rate'] = rate.apply(lambda x: round(x, 2))

    limit = state_taxes_raw['Lower Limit'].fillna('0').astype(str)
    limit = limit.str.replace(r'[$,\s]', '', regex=True)
    state_taxes_raw['Lower Limit'] = limit.astype(int)

    return state_taxes_raw


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(state_taxes):
    pairs = list(zip(state_taxes['Rate'].tolist(), state_taxes['Lower Limit'].tolist()))
    return (state_taxes.assign(bracket_list=pairs).groupby('State')[['bracket_list']].agg(list))
    
def combine_loans_and_state_taxes(loans, state_taxes):
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
        
    # Now it's your turn:
    brackets = state_brackets(state_taxes)
    brackets.index = brackets.index.map(state_mapping)
    brackets.index.name = "State"
    return (loans.rename(columns = {'addr_state': 'State'}).merge(brackets, left_on='State', right_index = True, how='left'))


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def find_disposable_income(loans_with_state_taxes):
    df = loans_with_state_taxes.copy()
    FEDERAL_BRACKETS = [
     (0.1, 0), 
     (0.12, 11000), 
     (0.22, 44725), 
     (0.24, 95375), 
     (0.32, 182100),
     (0.35, 231251),
     (0.37, 578125)
    ]
    return df.assign(federal_tax_owed = lambda d: d['annual_inc'].apply(lambda inc: tax_owed(inc, FEDERAL_BRACKETS)),
                     state_tax_owed = lambda d: d.apply(lambda row: tax_owed(row['annual_inc'], row['bracket_list']), axis = 1)).assign(
                     disposable_income = lambda d: d['annual_inc'] - d['federal_tax_owed'] - d['state_tax_owed'])


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    result = pd.DataFrame()
    for keyword in keywords:
        col_name = f'{keyword}_mean_{quantitative_column}'
        has_kw = loans[loans['emp_title'].str.contains(keyword, na=False)]
        by_group = has_kw.groupby(categorical_column)[quantitative_column].mean()
        by_group.loc['Overall'] = has_kw[quantitative_column].mean()
        result[col_name] = by_group
    result.index.name = categorical_column
    groups = [g for g in result.index if g != 'Overall']
    return result.loc[groups + ['Overall']]


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    agg = aggregate_and_combine(loans, keywords, quantitative_column, categorical_column)
    diff = agg.iloc[:, 0] - agg.iloc[:, 1]
    return bool(((diff.iloc[:-1] > 0).all() and diff.iloc[-1] < 0) or ((diff.iloc[:-1] < 0).all() and diff.iloc[-1] > 0))
    
def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': ['manager', 'driver'],
        'quantitative_column': 'int_rate',
        'categorical_column': 'verification_status'
    }
