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
    props = pd.DataFrame(index = grades.index)
    for name in project_names:
        grade = grades[name].fillna(0)
        max_pts = grades[name + ' - Max Points']
        fr = name + "_free_response"
        if fr in grades.columns:
            grade = grade + grades[fr].fillna(0)
            max_pts = max_pts + grades[fr + ' - Max Points']
        props[name] = grade / max_pts
    return props.mean(axis=1)
    # project_names = get_assignment_names(grades)["project"]
    # totals = []
    # for idx in grades.index:
    #     got_total = 0
    #     possible = 0
    #     for name in project_names:
    #         grade = grades.loc[idx, name]
    #         max_pts = grades.loc[idx, name + " - Max Points"]
    #         if not pd.isna(grade):
    #             got_total += grade
    #         possible += max_pts
    #         fr = name + "_free_response"
    #         if fr in grades.columns:
    #             fr_grade = grades.loc[idx, fr]
    #             fr_possible = grades.loc[idx, fr + " - Max Points"]

    #             if not pd.isna(fr_grade):
    #                 got_total += fr_grade
    #             possible += fr_possible
    #     totals.append(got_total / possible)
    # return pd.Series(totals, index = grades.index)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    parts = col.str.split(":", expand=True).astype(float)
    hours = parts[0] + (parts[1] / 60) + (parts[2] / 3600)
    grace = 2
    one_wk = 24 * 7
    two_wk = 24 * 14

    multipliers = pd.Series(0.4, index = col.index)
    multipliers[hours <= two_wk] = 0.7
    multipliers[hours <= one_wk] = 0.9
    multipliers[hours <= grace] = 1.0

    return multipliers


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    labs = get_assignment_names(grades)['lab']
    df = pd.DataFrame(index = grades.index)
    for lab in labs:
        raw_score = grades[lab].fillna(0)
        max_pts = grades[lab + ' - Max Points']
        mult = lateness_penalty(grades[lab + ' - Lateness (H:M:S)'])

        df[lab] = (raw_score / max_pts) * mult
    return df


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    one_col = (processed.sum(axis=1) - processed.min(axis=1)) / (processed.shape[1] - 1)
    return one_col


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    def proportion(assignments):
        total = pd.DataFrame(index=grades.index)
        for name in assignments:
            total[name] = grades[name].fillna(0) / grades[name + " - Max Points"]
        return total.mean(axis=1)
    names = get_assignment_names(grades)
    labs = grades.pipe(process_labs).pipe(lab_total)
    proj = projects_total(grades)
    checkp = proportion(names['checkpoint'])
    disc = proportion(names['disc'])
    midterm = proportion(names['midterm'])
    final = proportion(names['final'])

    return (
        0.2 * labs
        + 0.3 * proj
        + 0.025 * checkp
        + 0.025 * disc
        + 0.15 * midterm
        + 0.3 * final
    )


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    grade = pd.Series('F', index = total.index)
    grade[total >= 0.6] = 'D'
    grade[total >= 0.7] = 'C'
    grade[total >= 0.8] = 'B'
    grade[total >= 0.9] = 'A'

    return grade

def letter_proportions(total):
    grade = final_grades(total)
    return grade.value_counts() / len(grade)


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    questions = final_breakdown[final_breakdown.columns[question_numbers]]
    earned = questions.fillna(0).sum(axis=1)
    possible = questions.max().sum()
    return pd.DataFrame({
        'PID': final_breakdown['PID'],
        'Raw Redemption Score': earned / possible
    })
    
def combine_grades(grades, raw_redemption_scores):
    lookup = raw_redemption_scores.set_index('PID')['Raw Redemption Score']
    return grades.assign(**{'Raw Redemption Score': grades['PID'].map(lookup)})


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    return (ser - ser.mean()) / ser.std(ddof=0)
    
def add_post_redemption(grades_combined):
    pre = grades_combined['Midterm'].fillna(0) / grades_combined['Midterm - Max Points']
    z_scores = z_score(pre)
    z_redemp = z_score(grades_combined['Raw Redemption Score'])
    redemption = z_redemp * pre.std(ddof=0) + pre.mean()
    post = redemption.where(z_redemp > z_scores, pre).clip(upper=1)
    return grades_combined.assign(**{
        'Midterm Score Pre-Redemption': pre,
        'Midterm Score Post-Redemption': post
    })


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    w_mt = add_post_redemption(grades_combined)
    midterm_gain = (w_mt['Midterm Score Post-Redemption']
                    - w_mt['Midterm Score Pre-Redemption'])
    return total_points(grades_combined) + 0.15 * midterm_gain
        
def proportion_improved(grades_combined):
    before = final_grades(total_points(grades_combined))
    after = final_grades(total_points_post_redemption(grades_combined))
    return (after < before).mean()


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    improved = (grades_analysis['Letter Grade Post-Redemption']
                < grades_analysis['Letter Grade Pre-Redemption'])
    return improved.groupby(grades_analysis['Section']).mean().idxmax()
    
def top_sections(grades_analysis, t, n):
    final = grades_analysis['Final'] / grades_analysis['Final - Max Points']
    higher = (final >= t).groupby(grades_analysis['Section']).sum()
    return np.array(higher[higher >= n].index)


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    ordered = grades_analysis.sort_values('Total Points Post-Redemption',
                        ascending=False, kind='mergesort')[['PID', 'Section']].copy()
    ordered['Section Rank'] = ordered.groupby('Section').cumcount() + 1
    return (ordered.pivot(index='Section Rank', columns = 'Section', values = 'PID').fillna(''))







# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    proportion = (pd.crosstab(grades_analysis['Letter Grade Post-Redemption'],
                              grades_analysis['Section'], normalize='columns')
                              .reindex(['A', 'B', 'C', 'D', 'F'])
                              .fillna(0))
    fig = px.imshow(proportion, color_continuous_scale='Blues', title='Distribution of Letter Grades by Section',
                    labels = {'x': 'Section', 'y': 'Letter Grade', 'color': 'Proportion'}, aspect='auto')
    return fig.update_layout(font_family='Georgia')
