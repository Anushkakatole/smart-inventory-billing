import streamlit as st
from Database import get_conn

class Customers:
    @staticmethod
    def create_table():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    contact VARCHAR(15) NOT NULL
                )
            """)
            conn.commit()
        except Exception as e:
            conn.rollback()
            st.error(f"Error creating table: {e}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def insert_customer(name, contact):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO customers (name, contact) VALUES (%s, %s)",
                (name, contact)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            st.error(f"Error inserting customer: {e}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_customer(customer_id, name=None, contact=None):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            customer = cur.fetchone()
            if not customer:
                st.warning("Customer not found")
                return

            if name:
                cur.execute("UPDATE customers SET name = %s WHERE id = %s", (name, customer_id))
            if contact:
                cur.execute("UPDATE customers SET contact = %s WHERE id = %s", (contact, customer_id))

            conn.commit()
        except Exception as e:
            conn.rollback()
            st.error(f"Error updating customer: {e}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_customer(customer_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            st.error(f"Error deleting customer: {e}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_customers():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM customers")
            return cur.fetchall()
        except Exception as e:
            st.error(f"Error fetching customers: {e}")
            return []
        finally:
            cur.close()
            conn.close()

# ---------------- Streamlit Interface ---------------- #

st.title("Customer Management System")

menu = st.sidebar.selectbox("Menu", ["Create Table", "Insert Customer", "Update Customer", "Delete Customer", "View All Customers"])

# 1. Create Table
if menu == "Create Table":
    if st.button("Create Customer Table"):
        Customers.create_table()
        st.success("Customer table created successfully!")

# 2. Insert Customer
elif menu == "Insert Customer":
    st.subheader("Insert Customer")
    name = st.text_input("Customer Name")
    contact = st.text_input("Customer Contact")
    if st.button("Insert"):
        if name and contact:
            Customers.insert_customer(name, contact)
            st.success("Customer inserted successfully!")
        else:
            st.warning("Please enter both name and contact")

# 3. Update Customer
elif menu == "Update Customer":
    st.subheader("Update Customer")
    customer_id = st.number_input("Customer ID to Update", min_value=1, step=1)
    new_name = st.text_input("New Name")
    new_contact = st.text_input("New Contact")
    if st.button("Update"):
        if new_name or new_contact:
            Customers.update_customer(customer_id, new_name if new_name else None, new_contact if new_contact else None)
            st.success("Customer updated successfully!")
        else:
            st.warning("Enter at least a new name or contact to update")

# 4. Delete Customer
elif menu == "Delete Customer":
    st.subheader("Delete Customer")
    customer_id = st.number_input("Customer ID to Delete", min_value=1, step=1)
    if st.button("Delete"):
        Customers.delete_customer(customer_id)
        st.success("Customer deleted successfully!")

# 5. View All Customers
elif menu == "View All Customers":
    st.subheader("All Customers")
    if st.button("Show Customers"):
        all_customers = Customers.get_all_customers()
        if all_customers:
            st.dataframe(all_customers, columns=["ID", "Name", "Contact"])
        else:
            st.info("No customers found.")
