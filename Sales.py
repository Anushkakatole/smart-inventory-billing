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
            print("Sales table created successfully.")
        except Exception as e:
            conn.rollback()
            print("Error creating table:", e)
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
            print("Sale inserted successfully.")
        except Exception as e:
            conn.rollback()
            print("Error inserting sale:", e)
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

            if not update_fields:
                print("Nothing to update.")
                return

            values.append(sale_id)
            query = f"UPDATE sales SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(query, values)
            conn.commit()
            print("Sale updated successfully.")
        except Exception as e:
            conn.rollback()
            print("Error updating sale:", e)
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
            print("Sale deleted successfully.")
        except Exception as e:
            conn.rollback()
            print("Error deleting sale:", e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_sales():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales")
            sales = cur.fetchall()
            if sales:
                print("\nAll Sales:")
                for s in sales:
                    print(s)
            else:
                print("No sales found.")
        except Exception as e:
            print("Error fetching sales:", e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_sale_by_id(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
            sale = cur.fetchone()
            if sale:
                print("Sale:", sale)
            else:
                print("Sale not found.")
        except Exception as e:
            print("Error fetching sale:", e)
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
            if bill:
                print(f"Bill for Sale ID {sale_id}: {bill[0]}")
                return bill[0]
            else:
                print("Sale not found.")
                return 0
        except Exception as e:
            print("Error generating bill:", e)
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
            total = cur.fetchone()[0]
            total = total if total is not None else 0
            print(f"Total sales from {start_date} to {end_date}: {total}")
            return total
        except Exception as e:
            print("Error calculating total sales:", e)
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
            sales = cur.fetchall()
            if sales:
                print(f"Sales for Customer ID {customer_id}:")
                for s in sales:
                    print(s)
            else:
                print("No sales found for this customer.")
            return sales
        except Exception as e:
            print("Error fetching sales by customer:", e)
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def sales_menu():
        while True:
            print("\n1. Create Table")
            print("2. Insert Sale")
            print("3. Update Sale")
            print("4. Delete Sale")
            print("5. View All Sales")
            print("6. View Sale by ID")
            print("7. Generate Bill")
            print("8. Total Sale by Date")
            print("9. Sales by Customer")
            print("0. Exit Sales")

            choice = input("Enter your choice: ")

            if choice == "1":
                Sales.create_table()
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
                    customer_id=int(customer_id) if customer_id else None,
                    date=date if date else None,
                    total_amount=float(total_amount) if total_amount else None
                )
            elif choice == "4":
                sale_id = int(input("Enter sale ID to delete: "))
                Sales.delete_sale(sale_id)
            elif choice == "5":
                Sales.view_sales()
            elif choice == "6":
                sale_id = int(input("Enter sale ID: "))
                Sales.view_sale_by_id(sale_id)
            elif choice == "7":
                sale_id = int(input("Enter sale ID: "))
                Sales.generate_bill(sale_id)
            elif choice == "8":
                start = input("Start date (YYYY-MM-DD): ")
                end = input("End date (YYYY-MM-DD): ")
                Sales.total_sale_by_date(start, end)
            elif choice == "9":
                customer_id = int(input("Enter customer ID: "))
                Sales.get_sales_by_customer(customer_id)
            elif choice == "0":
                print("Exiting Sales menu.")
                break
            else:
                print("Invalid choice. Please try again.")
