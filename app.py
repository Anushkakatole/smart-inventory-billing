import streamlit as st
import psycopg2
from datetime import date
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from Database import get_conn
from Customers import Customers
from Products import Products
from Sales import Sales
from Salesitem import Salesitem


# ---------- INIT TABLES ----------
def initialize_tables():
    conn = get_conn()
    cur = conn.cursor()
    try:
        Customers.create_table()
        Products.create_table()
        Sales.create_table()
        Salesitem.create_table()

        cur.execute("SELECT setval('customers_id_seq', COALESCE(MAX(id),1)) FROM customers")
        cur.execute("SELECT setval('products_id_seq', COALESCE(MAX(id),1)) FROM products")
        cur.execute("SELECT setval('sales_id_seq', COALESCE(MAX(id),1)) FROM sales")
        cur.execute("SELECT setval('sale_items_id_seq', COALESCE(MAX(id),1)) FROM sale_items")

        conn.commit()
        st.success("Database tables initialized successfully!")
    except Exception as e:
        conn.rollback()
        st.error(e)
    finally:
        cur.close()
        conn.close()


st.set_page_config(page_title="Smart Inventory and Billing System", layout="wide")
st.title("🏪 Smart Inventory and Billing System")

if 'tables_initialized' not in st.session_state:
    initialize_tables()
    st.session_state.tables_initialized = True


# ---------- SIDEBAR ----------
menu_option = st.sidebar.selectbox(
    "Choose an option:",
    ["Dashboard", "Customer Management", "Product Management", "Sales Management", "Analytics & Reports"]
)


# ---------- DASHBOARD ----------
if menu_option == "Dashboard":
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM customers")
        customers = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM products")
        products = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM sales")
        sales = cur.fetchone()[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers", customers)
        col2.metric("Total Products", products)
        col3.metric("Total Sales", sales)

    except Exception as e:
        conn.rollback()
        st.warning(e)
    finally:
        cur.close()
        conn.close()


# ---------- CUSTOMER MANAGEMENT ----------
elif menu_option == "Customer Management":
    action = st.radio("Select Action:", ["View All Customers", "Add New Customer"])

    if action == "View All Customers":
        try:
            for c in Customers.get_all_customers():
                st.write(f"ID: {c[0]}, Name: {c[1]}, Contact: {c[2]}")
        except Exception as e:
            st.error(e)

    if action == "Add New Customer":
        with st.form("add_customer"):
            name = st.text_input("Name")
            contact = st.text_input("Contact")
            submit = st.form_submit_button("Add")

            if submit:
                conn = get_conn()
                cur = conn.cursor()
                try:
                    Customers.insert_customer(name, contact)
                    conn.commit()
                    st.success("Customer added")
                except Exception as e:
                    conn.rollback()
                    st.error(e)
                finally:
                    cur.close()
                    conn.close()


# ---------- PRODUCT MANAGEMENT ----------
elif menu_option == "Product Management":
    action = st.radio("Select Action:", ["View All Products", "Add New Product"])

    if action == "View All Products":
        for p in Products.view_products():
            st.write(p)

    if action == "Add New Product":
        with st.form("add_product"):
            name = st.text_input("Name")
            desc = st.text_area("Description")
            price = st.number_input("Price", min_value=0.0)
            qty = st.number_input("Quantity", min_value=0)
            submit = st.form_submit_button("Add")

            if submit:
                conn = get_conn()
                cur = conn.cursor()
                try:
                    Products.insert_product(name, desc, price, qty)
                    conn.commit()
                    st.success("Product added")
                except Exception as e:
                    conn.rollback()
                    st.error(e)
                finally:
                    cur.close()
                    conn.close()


# ---------- SALES ----------
elif menu_option == "Sales Management":
    customers = Customers.get_all_customers()
    if customers:
        customer_id = st.selectbox(
            "Select Customer",
            [c[0] for c in customers]
        )

        if st.button("Create Sale"):
            conn = get_conn()
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO sales (customer_id, date, total_amount) VALUES (%s,%s,%s) RETURNING id",
                    (customer_id, date.today(), 0)
                )
                sale_id = cur.fetchone()[0]
                conn.commit()
                st.success(f"Sale created: {sale_id}")
                st.session_state.sale_id = sale_id
            except Exception as e:
                conn.rollback()
                st.error(e)
            finally:
                cur.close()
                conn.close()


# ---------- ANALYTICS ----------
elif menu_option == "Analytics & Reports":
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*), SUM(total_amount) FROM sales")
        count, total = cur.fetchone()
        st.metric("Total Sales", count)
        st.metric("Revenue", total or 0)
    except Exception as e:
        conn.rollback()
        st.error(e)
    finally:
        cur.close()
        conn.close()
