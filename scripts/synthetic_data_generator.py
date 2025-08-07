"""
Generates synthetic student data for training the retention model.
"""
import numpy as np
import pandas as pd

def generate_synthetic_data(n_samples=1000, random_state=42):
    np.random.seed(random_state)
    
    # Core academic features
    current_gpa = np.random.uniform(0.0, 4.0, n_samples)
    attendance_rate = np.random.uniform(0.5, 1.0, n_samples)
    total_credits = np.random.randint(0, 18, n_samples)
    gpa_trend = np.random.normal(0.0, 0.2, n_samples)

    # Additional behavioral / demographic features
    study_hours_per_week = np.random.normal(15, 5, n_samples).clip(0)
    family_income = np.random.normal(50000, 15000, n_samples).clip(0)
    first_generation = np.random.binomial(1, 0.3, n_samples)
    distance_from_home = np.random.normal(50, 30, n_samples).clip(0)
    part_time_job = np.random.binomial(1, 0.5, n_samples)
    previous_semester_gpa = np.clip(current_gpa - gpa_trend + np.random.normal(0,0.3,n_samples), 0, 4)
    age = np.random.randint(18, 30, n_samples)
    high_school_gpa = np.random.uniform(2.0, 4.0, n_samples)
    sat_score = np.random.uniform(800, 1600, n_samples)
    extracurricular_activities = np.random.poisson(2, n_samples)
    financial_aid = np.random.binomial(1, 0.6, n_samples)

    # Assemble DataFrame
    df = pd.DataFrame({
        'current_gpa': current_gpa,
        'attendance_rate': attendance_rate,
        'total_credits': total_credits,
        'gpa_trend': gpa_trend,
        'study_hours_per_week': study_hours_per_week,
        'family_income': family_income,
        'first_generation': first_generation,
        'distance_from_home': distance_from_home,
        'part_time_job': part_time_job,
        'previous_semester_gpa': previous_semester_gpa,
        'age': age,
        'high_school_gpa': high_school_gpa,
        'sat_score': sat_score,
        'extracurricular_activities': extracurricular_activities,
        'financial_aid': financial_aid
    })

    # Create target using simple heuristic
    risk_score = (
        (4.0 - df['current_gpa']) * 0.4 +
        (1.0 - df['attendance_rate']) * 0.3 +
        (1 - np.tanh(df['gpa_trend'])) * 0.1 +
        (1 - np.tanh(df['study_hours_per_week']/20)) * 0.1 +
        (df['first_generation'] * 0.1)
    )
    risk_score = np.clip(risk_score, 0, 1)
    
    # Binary label: dropout if risk_score > threshold
    target = (risk_score > 0.5).astype(int)

    df['dropout'] = target
    return df
