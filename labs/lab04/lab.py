# lab.py


import pandas as pd
import numpy as np
import io
from pathlib import Path
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):
    format_dt = "%Y-%m-%d %H:%M:%S"
    times = pd.to_datetime(login['Time'], format=format_dt)
    primetime = (times.dt.hour >= 16) & (times.dt.hour < 20)
    return primetime.groupby(login['Login Id']).sum().to_frame('Time')


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def count_frequency(login):
    curr = pd.Timestamp("2024-01-31 23:59:00")
    times = pd.to_datetime(login['Time'])

    def logins_per_day(group):
        full_day = (curr - group.min()).days
        return len(group) / full_day
    
    return times.groupby(login['Login Id']).agg(logins_per_day)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def cookies_null_hypothesis():
    return [1, 2]
                         
def cookies_p_value(N):
    observed = 15
    runs = np.random.binomial(250, 0.04, size=N)
    return (runs >= observed).mean()


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def car_null_hypothesis():
    return [1, 4]

def car_alt_hypothesis():
    return [2, 6]

def car_test_statistic():
    return [1, 4]

def car_p_value():
    return 4


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def superheroes_test_statistic():
    return [1, 2, 3]
    
def bhbe_col(heroes):
    blond = heroes['Hair color'].str.lower().str.contains('blond', na=False)
    blue_eyed = heroes['Eye color'].str.lower().str.contains('blue', na=False)
    return pd.Series(blond & blue_eyed)

def superheroes_observed_statistic(heroes):
    bhbe = bhbe_col(heroes)
    return (heroes.loc[bhbe, 'Alignment'] == 'good').mean()

def simulate_bhbe_null(heroes, N):
    bhbe = bhbe_col(heroes).sum()
    good = (heroes['Alignment'] == 'good').mean()
    return np.random.binomial(bhbe, good, size=N) / bhbe

def superheroes_p_value(heroes):
    sims = simulate_bhbe_null(heroes, 100000)
    p_val = (sims >= superheroes_observed_statistic(heroes)).mean()
    decision = 'Reject' if p_val < 0.01 else 'Fail to reject'
    return [p_val, decision]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):
    means = data.groupby('Factory')[col].mean()
    return abs(means['Yorkville'] - means['Waco'])


def simulate_null(data, col='orange'):
    data = data.assign(Factory = np.random.permutation(data['Factory']))
    return diff_of_means(data, col)


def color_p_value(data, col='orange'):
    observed = diff_of_means(data, col)
    sims = np.array([simulate_null(data, col) for _ in range(1000)])
    return (sims >= observed).mean()


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def ordered_colors():
    return [('yellow', np.float64(0.0)),
    ('orange', np.float64(0.037)),
    ('red', np.float64(0.246)),
    ('green', np.float64(0.452)),
    ('purple', np.float64(0.984))]


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


    
def same_color_distribution():
    return (np.float64(0.007), 'Reject')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def perm_vs_hyp():
    return ['P', 'P', 'H', 'H', 'P']
