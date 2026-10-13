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
    ...


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    ...


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(heroes):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    ...

def university_info(cleaned):
    ...

