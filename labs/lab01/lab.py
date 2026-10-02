# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    if len(nums) == 0:
        return False
    mean = sum(nums) / len(nums)
    median = 0
    sorted_nums = sorted(nums)
    if len(sorted_nums) % 2 == 0:
        median = (sorted_nums[len(sorted_nums) // 2 - 1] + sorted_nums[len(sorted_nums) // 2]) / 2
    else:
        median = sorted_nums[len(sorted_nums) // 2]
    return mean >= median


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    st = ""
    while n > 0:
        st += s[:n]
        n -= 1
    return st


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    max_num = max(ints) + n
    width = len(str(max_num))
    lst = []
    for i in ints:
        exploded = range(i - n, i + n + 1)
        lst.append(" ".join([str(num).zfill(width) for num in exploded]))
    return lst


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    s = fh.read()
    lst = s.splitlines()
    return "".join([line[-1] for line in lst if len(line) > 0])


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    arr = np.array([])
    for i in range(len(A)):
        arr = np.append(arr, np.sqrt(i)+A[i])
    return arr

def where_square(A):
    arr = np.array([])
    for i in range(len(A)):
        if np.sqrt(A[i]) % 1 == 0:
            arr = np.append(arr, True)
        else:
            arr = np.append(arr, False)
    return arr.astype(bool)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    rows, cols = matrix.shape
    lst = []
    for i in range(rows):
        total = 0
        for j in range(cols):
            total += matrix[i][j]
        mean = total / rows
        if mean > cutoff:
            column = []
            for i in range(rows):
                column.append(matrix[i][j])
            lst.append(column)
    return np.array(lst).T


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    means = np.mean(matrix, axis=0)
    return matrix[:, means > cutoff]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    return np.round(A[1:] / A[:-1] - 1, 2)

def with_leftover(A):
    leftover = np.cumsum(20 % A)
    possible = leftover >= A
    if np.any(possible):
        return np.argmax(possible)
    return -1


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    num_players = salary.shape[0]
    num_teams = salary["Team"].nunique()
    total_salary = salary["Salary"].sum()
    highest_salary = salary["Salary"].max()
    avg_los = salary[salary["Team"] == "Los Angeles Lakers"]["Salary"].mean()

    sorted_salaries = salary.sort_values("Salary")
    fifth = sorted_salaries.iloc[4]
    fifth_lowest = fifth["Player"] + ", " + fifth["Team"]

    names = salary["Player"]
    names = names.where(~names.str.endswith(("Jr.", "Sr.", "I", "II", "III", "IV", "V")), names.str.rsplit(" ", n=1).str[0])
    last_names = names.str.split().str[-1]
    duplicates = last_names.duplicated().any()

    sorted_sal = salary.sort_values("Salary", ascending=False)
    highest = sorted_sal.iloc[0]
    total_highest = salary[salary["Team"] == highest["Team"]]["Salary"].sum()

    return pd.Series({
        "num_players": num_players,
        "num_teams": num_teams,
        "total_salary": total_salary,
        "highest_salary": highest_salary,
        "avg_los": avg_los,
        "fifth_lowest": fifth_lowest,
        "duplicates": duplicates,
        "total_highest": total_highest
    })


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    rows = []
    with open(fp, "r") as f:
        next(f)
        for line in f:
            line = line.strip().replace('"', '')
            parts = [x for x in line.split(",") if x != ""]

            first = parts[0]
            last = parts[1]
            weight = float(parts[2])
            height = float(parts[3])
            geo =  parts[4] + "," + parts[5]
            rows.append([first, last, weight, height, geo])
    return pd.DataFrame(rows, 
                        columns=["first", "last", "weight", "height", "geo"])
