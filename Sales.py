from Database import get_conn


class Sales:

    @staticmethod
    def create_table():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sales(
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL
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
    def insert_sale(customer_id, date, total_amount):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO sales (customer_id, date, total_amount) VALUES (%s, %s, %s)",
                (customer_id, date, total_amount)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_sale(sale_id, customer_id=None, date=None, total_amount=None):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
            sale = cur.fetchone()

            if not sale:
                print("SALE NOT FOUND")
                return

            update_fields = []
            values = []

            if customer_id:
                update_fields.append("customer_id = %s")
                values.append(customer_id)
            if date:
                update_fields.append("date = %s")
                values.append(date)
            if total_amount is not None:
                update_fields.append("total_amount = %s")
                values.append(total_amount)

            values.append(sale_id)
            query = f"UPDATE sales SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(query, values)

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_sale(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_sales():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales")
            return cur.fetchall()
        except Exception as e:
            print(e)
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_sale_by_id(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
            return cur.fetchone()
        except Exception as e:
            print(e)
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def generate_bill(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT total_amount FROM sales WHERE id = %s", (sale_id,))
            bill = cur.fetchone()
            return bill[0] if bill else 0
        except Exception as e:
            print(e)
            return 0
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def total_sale_by_date(start_date, end_date):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s",
                (start_date, end_date)
            )
            total = cur.fetchone()
            return total[0]
        except Exception as e:
            print(e)
            return 0
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_sales_by_customer(customer_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE customer_id = %s", (customer_id,))
            return cur.fetchall()
        except Exception as e:
            print(e)
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def sales_menu():
        while True:
            print("\n1. Create Table")
            print("2. Insert Sales")
            print("3. Update Sales")
            print("4. Delete Sales")
            print("5. View All Sales")
            print("6. View Sale by ID")
            print("7. Generate Bill")
            print("8. Total Sale by Date")
            print("9. Sales by Customer")
            print("0. Exit sales")

            choice = input("Enter your choice: ")

            if choice == "1":
                Sales.create_table()
                print("Sales table created successfully.")

            elif choice == "2":
                customer_id = int(input("Enter customer_id: "))
                date = input("Enter sales_date (YYYY-MM-DD): ")
                total_amount = float(input("Enter total_amount: "))
                Sales.insert_sale(customer_id, date, total_amount)

            elif choice == "3":
                sale_id = int(input("Enter sale ID: "))
                customer_id = input("New customer_id (leave blank to skip): ")
                date = input("New date (leave blank to skip): ")
                total_amount = input("New total_amount (leave blank to skip): ")

                Sales.update_sale(
                    sale_id,
                    customer_id if customer_id else None,
                    date if date else None,
                    float(total_amount) if total_amount else None
                )

            elif choice == "4":
                sale_id = int(input("Enter sale ID to delete: "))
                Sales.delete_sale(sale_id)

            elif choice == "5":
                print(Sales.view_sales())

            elif choice == "6":
                sale_id = int(input("Enter sale ID: "))
                print(Sales.view_sale_by_id(sale_id))

            elif choice == "7":
                sale_id = int(input("Enter sale ID: "))
                print("Bill:", Sales.generate_bill(sale_id))

            elif choice == "8":
                start = input("Start date (YYYY-MM-DD): ")
                end = input("End date (YYYY-MM-DD): ")
                print("Total Sales:", Sales.total_sale_by_date(start, end))

            elif choice == "9":
                customer_id = int(input("Enter customer ID: "))
                print(Sales.get_sales_by_customer(customer_id))

            elif choice == "0":
                break

            else:
                print("Invalid choice")
