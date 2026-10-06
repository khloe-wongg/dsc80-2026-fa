# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    names = {
        "lab" : [],
        "project" : [],
        "midterm" : [],
        "final" : [],
        "disc" : [],
        "checkpoint" : []
    }
    for col in grades.columns:
        assignment = col.split(" - ")[0]
        if assignment.startswith("lab"):
            if assignment not in names["lab"]:
                names["lab"].append(assignment)
        elif assignment.startswith("project"):
            if "checkpoint" in assignment:
                if assignment not in names["checkpoint"]:
                    names["checkpoint"].append(assignment)
            elif "free_response" in assignment:
                continue
            elif assignment not in names["project"]:
                names["project"].append(assignment)
        elif assignment.startswith("discussion"):
            if assignment not in names["disc"]:
                names["disc"].append(assignment)
        elif assignment == "Midterm":
            if assignment not in names["midterm"]:
                names["midterm"].append(assignment)
        elif assignment == "Final":
            if assignment not in names["final"]:
                names["final"].append(assignment)
    return names


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    project_names = get_assignment_names(grades)["project"]
    totals = []
    for idx in grades.index:
        got_total = 0
        possible = 0
        for name in project_names:
            grade = grades.loc[idx, name]
            max_pts = grades.loc[idx, name + " - Max Points"]
            if not pd.isna(grade):
                got_total += grade
            possible += max_pts
            fr = name + "_free_response"
            if fr in grades.columns:
                fr_grade = grades.loc[idx, fr]
                fr_possible = grades.loc[idx, fr + " - Max Points"]

                if not pd.isna(fr_grade):
                    got_total += fr_grade
                possible += fr_possible
        totals.append(got_total / possible)
    return pd.Series(totals, index = grades.index)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    ...


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    ...


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    ...

def letter_proportions(total):
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    ...
    
def combine_grades(grades, raw_redemption_scores):
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    ...
    
def add_post_redemption(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    ...
        
def proportion_improved(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    ...
    
def top_sections(grades_analysis, t, n):
    ...


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    ...







# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    ...
