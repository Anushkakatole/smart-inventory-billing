import streamlit as st
import psycopg2


def get_conn():
    """
    Creates and returns a NEW PostgreSQL connection.
    Safe for Streamlit Cloud + Supabase.
    """
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"],
        sslmode="require"
    )
