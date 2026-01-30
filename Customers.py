from Database import get_conn


class Customers:
    def __init__(self):
        pass

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
            print(e)
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
            print(e)
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
                print("CUSTOMER NOT FOUND")
                return

            if name:
                cur.execute(
                    "UPDATE customers SET name = %s WHERE id = %s",
                    (name, customer_id)
                )
            if contact:
                cur.execute(
                    "UPDATE customers SET contact = %s WHERE id = %s",
                    (contact, customer_id)
                )

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
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
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_customers():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM customers")
            customers = cur.fetchall()
            return customers
        except Exception as e:
            print(e)
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def customer_menu():
        while True:
            print("1. Create Table")
            print("2. Insert Customer")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. View All Customers")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                Customers.create_table()
                print("Customer table created successfully.")

            elif choice == "2":
                name = input("Enter customer name: ")
                contact = input("Enter customer contact: ")
                Customers.insert_customer(name, contact)
                print("Customer inserted successfully.")

            elif choice == "3":
                customer_id = int(input("Enter customer ID to update: "))
                name = input("Enter new name: ")
                contact = input("Enter new contact: ")
                Customers.update_customer(customer_id, name, contact)
                print("Customer updated successfully.")

            elif choice == "4":
                customer_id = int(input("Enter customer ID to delete: "))
                Customers.delete_customer(customer_id)
                print("Customer deleted successfully.")

            elif choice == "5":
                customers = Customers.get_all_customers()
                print(customers)

            elif choice == "0":
                print("Exiting ....")
                break

            else:
                print("Invalid choice. Please try again.")
