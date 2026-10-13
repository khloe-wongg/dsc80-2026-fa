# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():
    # tricky_1 = pd.DataFrame(
    #     [['one', 'a', 1],
    #      ['two', 'b', 2],
    #      ['three', 'c', 3],
    #      ['four', 'd', 4],
    #      ['five', 'e', 5]],
    #      columns = ['Name', 'Name', 'Age']
    # )
    # tricky_1.to_csv('tricky_1.csv', index = False)
    # tricky_2 = pd.read_csv('tricky_1.csv')
    return 3

# bools = pd.DataFrame(
#     [[0, 0, 1, 1],
#      [1, 1, 0, 0],
#      [0, 1, 0, 1],
#      [1, 0, 1, 0]],
#     columns = [True, True, False, False])
def trick_bool():
    return [4, 10, 13]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    num_nonnull = df.count()
    prop_nonnull = num_nonnull / len(df)
    num_distinct = df.nunique()
    prop_distinct = num_distinct / num_nonnull
    return pd.DataFrame({
        'num_nonnull': num_nonnull,
        'prop_nonnull': prop_nonnull,
        'num_distinct': num_distinct,
        'prop_distinct': prop_distinct
    })


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N=10):
    pd_out = pd.DataFrame(index = range(N))
    for col in df.columns:
        counts = df[col].value_counts().iloc[:N]
        pd_out[col + '_values'] = pd.Series(counts.index)
        pd_out[col + '_counts'] = pd.Series(counts.values)
    return pd_out


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    named_powers = powers.set_index('hero_names')
    num_powers = named_powers.sum(axis=1)
    most_powers = num_powers.idxmax()
    flight = named_powers[named_powers['Flight']].drop(columns = 'Flight')
    most_common = flight.sum().idxmax()
    one_power = named_powers[num_powers == 1].sum().idxmax()
    return [most_powers, most_common, one_power]


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(heroes):
    return heroes.replace(['-', -99], np.nan)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return ['Onslaught', 'George Lucas', 'bad', 'Marvel Comics', 'NBC - Heroes', 'Groot']
    

# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    df = df.copy()
    df['institution'] = df['institution'].replace('\n', ', ')
    df['broad_impact'] = df['broad_impact'].astype(int)
    nationrank_split = df['national_rank'].str.split(', ', n=1, expand=True)
    df['nation'] = nationrank_split[0]
    df['national_rank_cleaned'] = nationrank_split[1].astype(int)
    df = df.drop(columns = 'national_rank')
    df['nation'] = df['nation'].replace({'Czechia': 'Czech Republic',
                                         'UK': 'United Kingdom',
                                         'USA': 'United States'})
    df['is_r1_public'] = (df['control'] == 'Public') & df['city'].notna() & df['state'].notna()

def university_info(cleaned):
    group = cleaned.groupby('state')
    means = group['score'].mean()[group.size() >= 3]
    lowestmean_state = means.idxmin()
    top100 = cleaned[cleaned['world_rank'] <= 100]
    propintop100 = float((top100['quality_of_faculty'] <= 100).mean())
    private_prop = (~cleaned['is_r1_public']).groupby(cleaned['state']).mean()
    privates_states = int((private_prop >= 0.50).sum())
    best_in_nation = cleaned[cleaned['national_rank_cleaned'] == 1]
    worst_world = best_in_nation.loc[best_in_nation['world_rank'].idxmax(), 'institution']
    return [lowestmean_state, propintop100, privates_states, worst_world]

