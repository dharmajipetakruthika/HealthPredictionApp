import streamlit as st
import sqlite3
import pickle
import pandas as pd
from datetime import date

# Load ML model
with open("health_model.pkl", "rb") as file:
    model = pickle.load(file)

# Database connection
conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")
conn.commit()

st.title("Health Prediction Application")

# Input Fields
name = st.text_input("Full Name")

dob = st.date_input(
    "Date of Birth",
    min_value=date(1900, 1, 1),
    max_value=date.today()
)

email = st.text_input("Email Address")

glucose = st.number_input("Glucose", min_value=0.0)

haemoglobin = st.number_input("Haemoglobin", min_value=0.0)

cholesterol = st.number_input("Cholesterol", min_value=0.0)

# Predict and Save
if st.button("Predict and Save"):

    prediction = model.predict(
        [[glucose, haemoglobin, cholesterol]]
    )[0]

    cursor.execute(
        """
        INSERT INTO patients
        (name,dob,email,glucose,haemoglobin,cholesterol,remarks)
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            name,
            str(dob),
            email,
            glucose,
            haemoglobin,
            cholesterol,
            str(prediction)
        )
    )

    conn.commit()

    st.success("Record Saved Successfully")
    st.write("Prediction:", prediction)

# Show Records
st.subheader("Patient Records")

df = pd.read_sql_query(
    "SELECT * FROM patients",
    conn
)

st.dataframe(df)

# Delete Section
st.subheader("Delete Patient")

patient_id = st.number_input(
    "Enter Patient ID to Delete",
    min_value=1,
    step=1,
    key="delete_id"
)

if st.button("Delete Patient"):
    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )

    conn.commit()

    st.success("Patient Deleted Successfully")
    st.rerun()

# Update Section
st.subheader("Update Patient")

update_id = st.number_input(
    "Enter Patient ID to Update",
    min_value=1,
    step=1,
    key="update_id"
)

new_glucose = st.number_input(
    "New Glucose",
    min_value=0.0,
    key="new_glucose"
)

new_haemoglobin = st.number_input(
    "New Haemoglobin",
    min_value=0.0,
    key="new_haemoglobin"
)

new_cholesterol = st.number_input(
    "New Cholesterol",
    min_value=0.0,
    key="new_cholesterol"
)

if st.button("Update Patient"):

    cursor.execute(
        """
        UPDATE patients
        SET glucose=?,
            haemoglobin=?,
            cholesterol=?
        WHERE id=?
        """,
        (
            new_glucose,
            new_haemoglobin,
            new_cholesterol,
            update_id
        )
    )

    conn.commit()
    st.success("Patient Updated Successfully")
    st.rerun()