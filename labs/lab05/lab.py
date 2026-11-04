# lab.py


from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ['NMAR', 'MD', 'MAR', 'MAR', 'MAR']


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ['MAR', 'MAR', 'MAR', 'NMAR', 'MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------

def _load_payment_ages():
    payments = pd.read_csv(Path('data') / 'payment.csv')
    birth_year = pd.to_datetime(
        payments['date_of_birth'], format='%d-%b-%Y', errors='coerce'
    ).dt.year
    ages = 2024 - birth_year
    is_missing = payments['credit_card_number'].isna()
    return ages, is_missing
 
 
def first_round():
    ages, is_missing = _load_payment_ages()
    ages_arr = ages.to_numpy(dtype=float)
    miss_arr = is_missing.to_numpy()
 
    def abs_diff_means(labels):
        return abs(np.nanmean(ages_arr[labels]) - np.nanmean(ages_arr[~labels]))
    observed = abs_diff_means(miss_arr)
    n_reps = 1000
    simulated = np.array([
        abs_diff_means(np.random.permutation(miss_arr))
        for _ in range(n_reps)
    ])
    pval = float((simulated >= observed).mean())
    return [pval, 'R' if pval < 0.05 else 'NR']
 
 
def second_round():
    ages, is_missing = _load_payment_ages()
    valid = ages.notna()
    ages, is_missing = ages[valid], is_missing[valid]
    pval = float(stats.ks_2samp(ages[is_missing], ages[~is_missing]).pvalue)
    reject = pval < 0.05
    return [pval, 'R' if reject else 'NR', 'D' if reject else 'ND']


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    pvals = {}
    for col in heights.columns:
        if col.startswith('child_'):
            is_missing = heights[col].isna()
            fathers = heights['father']
            pvals[col] = stats.ks_2samp(
                fathers[is_missing], fathers[~is_missing]
            ).pvalue
    return pd.Series(pvals)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    quartiles = pd.qcut(new_heights['father'], 4)
    group_means = new_heights.groupby(quartiles, observed=True)['child'].transform('mean')
    return new_heights['child'].fillna(group_means)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    observed = child.dropna()
    counts, edges = np.histogram(observed, bins=10)
    probs = counts / counts.sum()
    chosen = np.random.choice(len(counts), size=N, p=probs)
    return np.random.uniform(edges[chosen], edges[chosen + 1])


def impute_height_quant(child):
    missing = child.isna()
    imputed = quantitative_distribution(child, int(missing.sum()))
    filled = child.copy()
    filled[missing] = imputed
    return filled


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    return [1, 2, 2, 1], ["https://discord.com/robots.txt", "https://www.nytimes.com/robots.txt"]
