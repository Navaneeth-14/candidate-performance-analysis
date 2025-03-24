import pandas as pd

def improvement_recommendations(marks):
    if marks < 40:
        return "Focus on fundamentals, seek guidance."
    elif marks < 60:
        return "Revise key concepts, practice more problems."
    elif marks < 80:
        return "Improve speed and accuracy, aim for higher."
    else:
        return "Maintain performance, attempt advanced topics."

def apply_recommendations():
    df = pd.read_csv("synthetic_dataset.csv")
    df['Recommendation'] = df['Marks'].apply(improvement_recommendations)
    df.to_csv("dataset_with_recommendations.csv", index=False)
    return df  # Returning DataFrame for use in Streamlit

