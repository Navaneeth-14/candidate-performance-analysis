## 📂 Project Files Overview
This project is a **Student Performance Analysis Dashboard** built with **Streamlit**.  
It allows users to **upload student performance data**, analyze it using various methods, and generate reports.  

### 📝 1. `datagenerate.py` 📌 Generates synthetic student performance data.  
  🟦 Adds **randomized marks, attempts, subject codes, and grades** for each student.  
  🟦 Ensures students take **multiple attempts only if they score below 40**.  
  🟦 Assigns **grades based on marks**.  
  ⚠️ **Not included in the Streamlit app directly**—runs separately before uploading data.  

---

### 🖥️ 2. `streamlit.py` (Main App) 📌 This is the main Streamlit application file.  
  🟦 Provides a **sidebar menu** with different analysis features.  
  🟦 Allows **CSV/Excel upload** and stores data in `st.session_state`.  
  🟦 Implements **Performance Analysis** with **"Overall Subjects"** and **category filtering** (Weak, Average, Strong).  
  🟦 Provides **Graphical Analysis** (bar chart, line chart, scatter plot).  
  🟦 Supports **Pairing students** based on performance.  
  🟦 Generates **student performance reports (PDFs)**.  

---

### 📂 3. `data_preprocessing.py` 📌 Handles file upload and preprocessing of student data.  
  🟦 Reads **CSV or Excel files** and loads them into a Pandas DataFrame.  
  🟦 Ensures the **required columns (Student Name, Marks, Subject, etc.) exist**.  
  🟦 Cleans data (**removing missing values, formatting**).  

---

### 📊 4. `analysis.py` 📌 Performs detailed performance analysis.  
  🟦 Provides **student-wise, subject-wise, and multi-student comparisons**.  
  🟦 Displays **overall trends in performance**.  
  🟦 Generates **individual student performance graphs** (line charts).  
  🟦 Categorizes students as **Weak, Average, or Strong**.  

---

### 🤝 5. `pair.py` 📌 Pairs weak students with strong students for mentoring.  
  🟦 **Pairing by Subject:** Matches weak students with strong students **in the same subject**.  
  🟦 **Overall Pairing:** Matches students based on their **overall average performance**.  

---

### 📌 6. `recommend.py` 📌 Provides personalized recommendations for students.  
  🟦 Suggests **subjects/topics for improvement** based on performance trends.  
  🟦 Can integrate with **AI-based feedback** in the future.  

---

### 📄 7. `generate.py` 📌 Generates a PDF report summarizing student performance.  
  🟦 Includes **grades, marks trends, and improvement suggestions**.  
  🟦 Generates **student-specific insights in a structured format**.  
