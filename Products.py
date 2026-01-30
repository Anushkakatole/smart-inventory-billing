from Database import get_conn


class Products:

    @staticmethod
    def create_table():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    quantity INT NOT NULL
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
    def insert_product(name, description, price, quantity):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
                (name, description, price, quantity)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_products(product_id, name=None, description=None, price=None, quantity=None):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cur.fetchone()

            if not product:
                print("PRODUCT NOT FOUND")
                return

            update_fields = []
            values = []

            if name:
                update_fields.append("name = %s")
                values.append(name)
            if description:
                update_fields.append("description = %s")
                values.append(description)
            if price is not None:
                update_fields.append("price = %s")
                values.append(price)
            if quantity is not None:
                update_fields.append("quantity = %s")
                values.append(quantity)

            values.append(product_id)
            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(query, values)

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_product(product_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_product_id(product_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return cur.fetchone()
        except Exception as e:
            print(e)
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_products():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products")
            return cur.fetchall()
        except Exception as e:
            print(e)
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def product_menu():
        while True:
            print("\n1. Create Table")
            print("2. Insert Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. View Product by ID")
            print("6. View All Products")
            print("0. Exit Products")

            choice = input("Enter your choice: ")

            if choice == "1":
                Products.create_table()
                print("Product table created successfully.")

            elif choice == "2":
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Products.insert_product(name, description, price, quantity)
                print("Product inserted successfully.")

            elif choice == "3":
                product_id = int(input("Enter product ID to update: "))
                name = input("Enter new name (leave blank to skip): ")
                description = input("Enter new description (leave blank to skip): ")
                price = input("Enter new price (leave blank to skip): ")
                quantity = input("Enter new quantity (leave blank to skip): ")

                Products.update_products(
                    product_id,
                    name if name else None,
                    description if description else None,
                    float(price) if price else None,
                    int(quantity) if quantity else None
                )
                print("Product updated successfully.")

            elif choice == "4":
                product_id = int(input("Enter product ID to delete: "))
                Products.delete_product(product_id)
                print("Product deleted successfully.")

            elif choice == "5":
                product_id = int(input("Enter product ID to view: "))
                product = Products.view_product_id(product_id)
                print(product)

            elif choice == "6":
                products = Products.view_products()
                for p in products:
                    print(p)

            elif choice == "0":
                print("Exiting ....")
                break

            else:
                print("Invalid choice. Please try again.")
