from Database import conn
class Salesitem:
    
    @staticmethod
    def create_table():
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales_items(
                id SERIAL PRIMARY KEY,
                sales_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        """)
        conn.commit()
        cur.close()

        