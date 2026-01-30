import streamlit as st
import psycopg2

def connection():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"],
        sslmode="require"
    )

conn = connection()
