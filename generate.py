import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        """Set up the PDF header."""
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "Student Performance Report", ln=True, align="C")
        self.ln(10)

    def add_student_info(self, student_name, overall_performance):
        """Add student name and overall performance to the PDF."""
        self.set_font("Arial", "B", 12)
        self.cell(200, 10, f"Student Name: {student_name}", ln=True)
        self.cell(200, 10, f"Overall Performance: {overall_performance}", ln=True)
        self.ln(10)

    def add_table(self, df):
        """Add subject-wise marks table to the PDF."""
        self.set_font("Arial", "B", 10)
        col_widths = [60, 30, 30, 50]  # Subject, Marks, Grade, Remarks

        # Table header
        headers = ["Subject", "Marks", "Grade", "Remarks"]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1, align="C")
        self.ln()

        # Table rows
        self.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            self.cell(col_widths[0], 10, row["Subject"], border=1)
            self.cell(col_widths[1], 10, str(row["Marks"]), border=1, align="C")
            self.cell(col_widths[2], 10, row["Grade"], border=1, align="C")
            self.cell(col_widths[3], 10, get_remarks(row["Marks"]), border=1, align="C")
            self.ln()

        self.ln(10)  # Space before graph

    def add_graph(self, img_path):
        """Insert the performance graph below the table."""
        self.image(img_path, x=15, w=180, h=80)
        self.ln(10)

def get_remarks(marks):
    """Generate remarks based on marks."""
    if marks >= 90:
        return "Excellent"
    elif marks >= 75:
        return "Great job!"
    elif marks >= 50:
        return "Keep improving."
    else:
        return "Needs effort."

def generate_report(student_name, df):
    """Generates a detailed PDF report for a student's performance across subjects."""
    student_df = df[df["Student Name"] == student_name]

    # Calculate overall performance
    avg_marks = student_df["Marks"].mean()
    if avg_marks >= 75:
        overall_performance = "Strong"
    elif avg_marks >= 50:
        overall_performance = "Average"
    else:
        overall_performance = "Weak"

    # Generate Bar Chart
    plt.figure(figsize=(6, 4))
    plt.bar(student_df["Subject"], student_df["Marks"], color="skyblue")
    plt.xlabel("Subjects")
    plt.ylabel("Marks")
    plt.title(f"Performance of {student_name}")
    plt.xticks(rotation=45)

    img_path = f"{student_name}_graph.png"
    plt.savefig(img_path, bbox_inches="tight")
    plt.close()

    # Create PDF
    pdf = PDF()
    pdf.add_page()
    pdf.add_student_info(student_name, overall_performance)
    pdf.add_table(student_df)
    pdf.add_graph(img_path)

    # Save Report
    pdf_path = f"{student_name}_report.pdf"
    pdf.output(pdf_path)
    os.remove(img_path)  # Clean up the graph image after saving

    return pdf_path
