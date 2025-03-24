def load_data(file):
    import pandas as pd
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file, engine='openpyxl')
    else:
        return None

    # Standardize column names
    df.columns = df.columns.str.strip()  # Remove extra spaces
    column_mapping = {
        "S.NO": "Student ID",
        "ENROLL NO": "Enroll No",
        "NAME": "Student Name",
        "EMAIL ID": "Email"
    }

    df.rename(columns=column_mapping, inplace=True)
    return df
