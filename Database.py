import psycopg2

def connection():
    conn = psycopg2.connect(
        host = "localhost",
        database = "ecommerce",
        user = "postgres",
        password = "10anu0107",
        port= "5432",
    )

    if conn:
        print(">>>>>>>>> Connection stabilished <<<<<<<<<")
    else:
        print(">>>>>>>>> Connection failed <<<<<<<<<")
    return conn

conn = connection()