import streamlit as st
import pandas as pd
import plotly.express as px

def analyze_performance(df):
    """Displays student-wise performance analysis without showing missing values."""
    st.subheader("Performance Analysis")
    
    # Check if required columns exist
    required_columns = {'Student Name', 'Subject', 'Marks', 'Grade'}
    if not required_columns.issubset(df.columns):
        st.error("⚠️ Missing required columns in dataset!")
        return
    
    # Show dataset preview
    st.write("📋 **Data Preview:**")
    st.write(df.head())
    
    # Student-wise performance summary
    student_performance = df.groupby('Student Name')[['Marks']].mean().reset_index()
    student_performance.columns = ['Student Name', 'Average Marks']
    st.write("📊 **Student Performance Summary:**")
    st.write(student_performance)
    
    # Display subject-wise performance
    subject_performance = df.groupby('Subject')[['Marks']].mean().reset_index()
    subject_performance.columns = ['Subject', 'Average Marks']
    st.write("📖 **Subject Performance Summary:**")
    st.write(subject_performance)

def analyze_individual_performance(df):
    """Analyze performance of an individual student in a specific subject over multiple attempts."""
    st.subheader("🎓 Individual Student Performance")
    student = st.selectbox("📌 Select a Student", df['Student Name'].unique())
    subject = st.selectbox("📖 Select a Subject", df['Subject'].unique())
    
    student_data = df[(df['Student Name'] == student) & (df['Subject'] == subject)]
    
    if student_data.empty:
        st.warning("⚠️ No data available for this student in the selected subject.")
        return

    st.write(student_data[['Subject', 'Attempt', 'Marks', 'Grade']])
    
    fig = px.line(student_data, x='Attempt', y='Marks', markers=True, 
                  title=f"📈 Performance of {student} in {subject}")
    st.plotly_chart(fig)

def analyze_multiple_students(df):
    """Compare performance of multiple students in a specific subject over multiple attempts."""
    st.subheader("👥 Compare Multiple Students in a Subject")
    students = st.multiselect("📌 Select Students", df['Student Name'].unique())
    subject = st.selectbox("📖 Select a Subject", df['Subject'].unique())
    
    if students:
        student_data = df[(df['Student Name'].isin(students)) & (df['Subject'] == subject)]
        
        if student_data.empty:
            st.warning("⚠️ No data available for selected students in this subject.")
            return
        
        st.write(student_data[['Student Name', 'Subject', 'Attempt', 'Marks', 'Grade']])
        
        fig = px.line(student_data, x='Attempt', y='Marks', color='Student Name', markers=True, 
                      title=f"📊 Comparison of Student Performance in {subject}")
        st.plotly_chart(fig)

def plot_performance_graph(df):
    """Plots a performance trend graph for all students."""
    st.subheader("📈 Overall Performance Trend")

    # Ensure required columns exist
    required_columns = {'Attempt', 'Marks', 'Student Name'}
    if not required_columns.issubset(df.columns):
        st.error(f"⚠️ Missing required columns: {required_columns - set(df.columns)}")
        return

    fig = px.line(df, x='Attempt', y='Marks', color='Student Name', markers=True, 
                  title="📊 Overall Student Performance Trend")
    st.plotly_chart(fig)
