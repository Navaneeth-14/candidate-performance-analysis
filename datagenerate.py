import pandas as pd
import random

def generate_synthetic_dataset(input_file, output_file):
    """Generates a synthetic dataset based on an uploaded student name list and saves it to a new file."""
    df = pd.read_csv("E:/namelist.csv")  # Load uploaded file
    df.columns = df.columns.str.strip()  # Remove extra spaces from column names
    
    print("Columns in Uploaded File:", df.columns.tolist())  # Debugging step
    
    column_mapping = {
    "NAME": "Name",
    "STUDENT ID": "Student ID",
    "ID": "Student ID",
    "FULL NAME": "Name",
    "Sl. No.": "Student ID",  # Fix here
    "MAIL": "Email"
}
    df.rename(columns=column_mapping, inplace=True)

    
    if "Name" not in df.columns or "Student ID" not in df.columns:
        raise ValueError("Uploaded file must contain 'Name' and 'Student ID' columns.")
    
    subjects = {
        'Mathematics': 'MATH101',
        'Python': 'PY102',
        'Machine Learning': 'ML103',
        'English': 'GP104',
        'Database': 'CS105'
    }
    
    synthetic_data = []
    
    for _, row in df.iterrows():
        student_name = row['Name']
        student_id = row['Student ID']
        for subject, subject_code in subjects.items():
            attempt = 1
            marks = random.randint(30, 100)  # Ensure marks are between 30 and 100
            
            while attempt <= 3:
                grade = assign_grade(marks)
                synthetic_data.append({
                    'Student ID': student_id,
                    'Student Name': student_name,
                    'Subject': subject,
                    'Subject Code': subject_code,
                    'Attempt': attempt,
                    'Marks': marks,
                    'Grade': grade
                })
                
                if marks >= 35:
                    break  # No need for further attempts
                
                # Increase marks slightly for re-attempts (max 100)
                marks = min(100, marks + random.randint(5, 15))
                attempt += 1
    
    synthetic_df = pd.DataFrame(synthetic_data)
    synthetic_df.to_csv(output_file, index=False)
    print(f"Synthetic dataset saved to {output_file}")

def assign_grade(marks):
    """Assigns a grade based on marks."""
    if marks >= 85:
        return 'S'
    elif marks >= 75:
        return 'A'
    elif marks >= 65:
        return 'B'
    elif marks >= 55:
        return 'C'
    elif marks >= 45:
        return 'D'
    elif marks >= 35:
        return 'E'
    else:
        return 'F'

if __name__ == "__main__":
    input_file = "students.csv"  # Replace with your actual file name
    output_file = "synthetic_dataset.csv"
    generate_synthetic_dataset(input_file, output_file)