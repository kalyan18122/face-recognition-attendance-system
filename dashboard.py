import streamlit as st
import pandas as pd
import os

st.title("AI Face Recognition Attendance Dashboard")

file = "Attendance.csv"

if not os.path.exists(file):
    st.warning("Attendance.csv not found")
else:

    df = pd.read_csv(file, on_bad_lines="skip")

    # Fix column names
    df.columns = [c.strip() for c in df.columns]

    st.subheader("Attendance Records")
    st.dataframe(df)

    # Check if Name column exists
    if "Name" in df.columns:

        st.subheader("Total Records")
        st.write(len(df))

        st.subheader("Students Present")

        students = df["Name"].value_counts()
        st.bar_chart(students)

        st.subheader("Latest Attendance")
        st.write(df.tail(5))

    else:
        st.error("Column 'Name' not found in Attendance.csv")
        st.write("Detected Columns:", df.columns)