import streamlit as st
import pandas as pd
import plotly.express as px
from data_preprocessing import load_data
from recommend import apply_recommendations
from pair import pair_students_by_subject, pair_students_overall
from generate import generate_report
from analysis import analyze_performance, plot_performance_graph, analyze_individual_performance

def main():
    st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
    
    st.sidebar.title("📊 Select an Option")
    
    # Sidebar Buttons
    if st.sidebar.button("📂 Upload File"):
        st.session_state["choice"] = "Upload File"
    if st.sidebar.button("📑 Performance Analysis"):
        st.session_state["choice"] = "Performance Analysis"
    if st.sidebar.button("📈 Graphical Analysis"):
        st.session_state["choice"] = "Graphical Analysis"
    if st.sidebar.button("🤝 Pair Students by Subject"):
        st.session_state["choice"] = "Pair Students by Subject"
    if st.sidebar.button("🔗 Pair Students Overall"):
        st.session_state["choice"] = "Pair Students Overall"
    if st.sidebar.button("📄 Report Generation"):
        st.session_state["choice"] = "Report Generation"
    
    # Default selection
    choice = st.session_state.get("choice", "Upload File")
    
    if choice == "Upload File":
        st.title("📂 Upload Performance Report")
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            st.session_state["df"] = df
            st.write("📋 Data Preview:", df.head())
            st.success("✅ File uploaded and processed successfully!")
    
    elif choice == "Performance Analysis" and "df" in st.session_state:
        df = st.session_state["df"]
        st.title("📑 Student Performance Analysis")

        # Add "Overall Subjects" option to subject selection
        subject_options = ["Overall Subjects"] + list(df['Subject'].unique())
        subject_filter = st.selectbox("📖 Select Subject", subject_options)

        if subject_filter == "Overall Subjects":
            # Compute overall average marks per student
            overall_avg = df.groupby("Student Name")["Marks"].mean().reset_index()
            overall_avg.columns = ["Student Name", "Average Marks"]
            
            # Categorize students based on overall average marks
            overall_avg["Performance Category"] = pd.cut(
                overall_avg["Average Marks"],
                bins=[0, 40, 70, 100],  # Customize thresholds if needed
                labels=["Weak", "Average", "Strong"]
            )

            # Allow user to filter students based on their category
            performance_category = st.selectbox("📌 Select Performance Category", ["Weak", "Average", "Strong"])
            selected_students = overall_avg[overall_avg["Performance Category"] == performance_category]

            # Filter dataset to only include selected students
            filtered_df = df[df["Student Name"].isin(selected_students["Student Name"])]

            st.write(f"📊 **{performance_category} Performing Students (Overall):**")
            st.dataframe(selected_students)

        else:
            # Filter the dataset for the selected subject
            filtered_df = df[df['Subject'] == subject_filter]

            # Performance category selection (based on subject marks)
            performance_category = st.selectbox("📌 Select Performance Category", ["Weak", "Average", "Strong"])
            if performance_category == "Weak":
                filtered_df = filtered_df[filtered_df['Grade'].isin(['E', 'F'])]
            elif performance_category == "Average":
                filtered_df = filtered_df[filtered_df['Grade'].isin(['C', 'D'])]
            elif performance_category == "Strong":
                filtered_df = filtered_df[filtered_df['Grade'].isin(['A', 'S', 'B'])]

        st.write("📊 Filtered Performance Data:")
        if not filtered_df.empty:
            st.dataframe(filtered_df)

        # Find student with max and min marks within selected subject or overall
        if not df.empty:
            if subject_filter == "Overall Subjects":
                max_student = df.loc[df['Marks'].idxmax()]
                min_student = df.loc[df['Marks'].idxmin()]
                st.write(f"🏆 **Highest Scorer Overall:** {max_student['Student Name']} ({max_student['Marks']} marks in {max_student['Subject']})")
                st.write(f"⚠️ **Lowest Scorer Overall:** {min_student['Student Name']} ({min_student['Marks']} marks in {min_student['Subject']})")
            else:
                subject_df = df[df['Subject'] == subject_filter]
                if not subject_df.empty:
                    max_student = subject_df.loc[subject_df['Marks'].idxmax()]
                    min_student = subject_df.loc[subject_df['Marks'].idxmin()]
                    st.write(f"🏆 **Highest Scorer in {subject_filter}:** {max_student['Student Name']} ({max_student['Marks']} marks)")
                    st.write(f"⚠️ **Lowest Scorer in {subject_filter}:** {min_student['Student Name']} ({min_student['Marks']} marks)")

        analyze_performance(filtered_df)  
    
    elif choice == "Graphical Analysis" and "df" in st.session_state:
        df = st.session_state["df"]
        st.title("📈 Graphical Analysis of Performance")
        
        student_selection = st.selectbox("🎓 Select a Student for Analysis", df['Student Name'].unique())
        student_df = df[df['Student Name'] == student_selection]
        
        st.subheader(f"📊 Performance of {student_selection} Across Subjects")
        
        # Bar Chart
        bar_fig = px.bar(student_df, x='Subject', y='Marks', title=f"📊 Marks of {student_selection} in Different Subjects", color='Subject')
        st.plotly_chart(bar_fig)
        
        # Line Chart
        line_fig = px.line(student_df, x='Subject', y='Marks', title=f"📉 Performance Trend of {student_selection}", markers=True)
        st.plotly_chart(line_fig)
        
        # Scatter Plot
        scatter_fig = px.scatter(student_df, x='Subject', y='Marks', title=f"📍 Marks Distribution for {student_selection}", color='Subject', size='Marks')
        st.plotly_chart(scatter_fig)
    
    elif choice == "Pair Students by Subject" and "df" in st.session_state:
        df = st.session_state["df"]
        st.title("🤝 Pair Weak Students with Strong Performers by Subject")
        subject_selection = st.selectbox("📖 Select a Subject", df['Subject'].unique())
        subject_df = df[df['Subject'] == subject_selection]
        pairs = pair_students_by_subject(subject_df)
        st.dataframe(pairs)
    
    elif choice == "Pair Students Overall" and "df" in st.session_state:
        df = st.session_state["df"]
        st.title("🔗 Pair Weak Students with Strong Performers Overall")
        pairs = pair_students_overall(df)
        st.dataframe(pairs)
    
    elif choice == "Report Generation" and "df" in st.session_state:
        df = st.session_state["df"]
        st.title("📄 Generate Student Reports")
        student = st.selectbox("🎓 Select a Student", df['Student Name'].unique())

        if st.button("📥 Generate PDF Report"):
            report_path = generate_report(student, df)

            with open(report_path, "rb") as file:
                st.download_button(
                    label="📥 Download Report",
                    data=file,
                    file_name=f"{student}_report.pdf",
                    mime="application/pdf"
                )
    else:
        st.warning("⚠️ Please upload a file first.")

if __name__ == "__main__":
    main()
