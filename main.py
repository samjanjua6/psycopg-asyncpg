import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="Testing",
    user="postgres",
    password=12345,
    port=5433
)

print("Database connection established successfully.")

cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50))"""
)

cursor.execute(
    """INSERT INTO users (name, email) VALUES (%s, %s)""",
    ("John Doe", "john.doe@example.com")
)

cursor.execute("""SELECT * FROM users""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.commit()

connection.close()

print("Table created successfully.")