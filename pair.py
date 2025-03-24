import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment

def pair_students_by_subject(df):
    """Pairs weak students with strong performers for knowledge sharing within the same subject."""
    pairs = []
    
    for subject in df['Subject'].unique():
        poor = df[(df['Subject'] == subject) & (df['Grade'].isin(['E', 'F']))]
        strong = df[(df['Subject'] == subject) & (df['Grade'].isin(['A', 'S']))]

        if not poor.empty and not strong.empty:
            cost_matrix = np.zeros((len(poor), len(strong)))
            for i, (_, p) in enumerate(poor.iterrows()):
                for j, (_, s) in enumerate(strong.iterrows()):
                    cost_matrix[i, j] = -abs(p['Marks'] - s['Marks'])

            row_ind, col_ind = linear_sum_assignment(cost_matrix)

            for r, c in zip(row_ind, col_ind):
                pairs.append({
                    'Subject': subject,
                    'Weak Student': poor.iloc[r]['Student Name'],
                    'Weak Student Marks': poor.iloc[r]['Marks'],
                    'Strong Student': strong.iloc[c]['Student Name'],
                    'Strong Student Marks': strong.iloc[c]['Marks']
                })
    
    return pd.DataFrame(pairs)

def pair_students_overall(df):
    """Pairs weak students with strong performers based on overall performance across all subjects."""
    avg_marks = df.groupby('Student Name')['Marks'].mean().reset_index()
    avg_marks['Performance'] = pd.qcut(avg_marks['Marks'], q=3, labels=["Weak", "Medium", "Strong"])
    
    weak_students = avg_marks[avg_marks['Performance'] == "Weak"]
    strong_students = avg_marks[avg_marks['Performance'] == "Strong"]
    
    pairs = []
    if not weak_students.empty and not strong_students.empty:
        cost_matrix = np.zeros((len(weak_students), len(strong_students)))
        for i, (_, w) in enumerate(weak_students.iterrows()):
            for j, (_, s) in enumerate(strong_students.iterrows()):
                cost_matrix[i, j] = -abs(w['Marks'] - s['Marks'])
        
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        for r, c in zip(row_ind, col_ind):
            pairs.append({
                'Weak Student': weak_students.iloc[r]['Student Name'],
                'Weak Student Avg Marks': weak_students.iloc[r]['Marks'],
                'Strong Student': strong_students.iloc[c]['Student Name'],
                'Strong Student Avg Marks': strong_students.iloc[c]['Marks']
            })
    
    return pd.DataFrame(pairs)
