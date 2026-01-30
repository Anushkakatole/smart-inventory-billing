import streamlit as st
import psycopg2

def connection():
    conn = psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )
    return conn

conn = connection()
