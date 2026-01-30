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
            print("Product table created successfully.")
        except Exception as e:
            conn.rollback()
            print("Error creating table:", e)
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
            print("Product inserted successfully.")
        except Exception as e:
            conn.rollback()
            print("Error inserting product:", e)
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

            if not update_fields:
                print("Nothing to update.")
                return

            values.append(product_id)
            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(query, values)
            conn.commit()
            print("Product updated successfully.")
        except Exception as e:
            conn.rollback()
            print("Error updating product:", e)
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
            print("Product deleted successfully.")
        except Exception as e:
            conn.rollback()
            print("Error deleting product:", e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_product_id(product_id):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cur.fetchone()
            if product:
                print("Product:", product)
            else:
                print("Product not found.")
        except Exception as e:
            print("Error fetching product:", e)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def view_products():
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
            if products:
                print("\nAll Products:")
                for p in products:
                    print(p)
            else:
                print("No products found.")
        except Exception as e:
            print("Error fetching products:", e)
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

            elif choice == "2":
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Products.insert_product(name, description, price, quantity)

            elif choice == "3":
                product_id = int(input("Enter product ID to update: "))
                name = input("Enter new name (leave blank to skip): ")
                description = input("Enter new description (leave blank to skip): ")
                price = input("Enter new price (leave blank to skip): ")
                quantity = input("Enter new quantity (leave blank to skip): ")

                Products.update_products(
                    product_id,
                    name=name if name else None,
                    description=description if description else None,
                    price=float(price) if price else None,
                    quantity=int(quantity) if quantity else None
                )

            elif choice == "4":
                product_id = int(input("Enter product ID to delete: "))
                Products.delete_product(product_id)

            elif choice == "5":
                product_id = int(input("Enter product ID to view: "))
                Products.view_product_id(product_id)

            elif choice == "6":
                Products.view_products()

            elif choice == "0":
                print("Exiting ....")
                break

            else:
                print("Invalid choice. Please try again.")
