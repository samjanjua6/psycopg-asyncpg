import asyncio
import os

import asyncpg


# Keep connection settings in one place so the script is easy to adapt.
# You can set these environment variables before running the script, or let
# the defaults point to your local PostgreSQL instance.
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = int(os.environ.get("POSTGRES_PORT", "5433"))
DB_NAME = os.environ.get("POSTGRES_DB", "Testing")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "12345")


async def main() -> None:
    # asyncpg works with coroutines, so we create the connection with await.
    connection = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    try:
        print("Database connection established successfully.")

        # execute() runs SQL that does not return rows.
        # IF NOT EXISTS makes the script safe to run more than once.
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                email VARCHAR(50)
            )
            """
        )

        print("Table created successfully.")

        # This is an example insert so you can see how asyncpg sends parameters.
        # Use $1, $2, etc. instead of f-strings to avoid SQL injection.
        await connection.execute(
            "INSERT INTO users(name, email) VALUES($1, $2)",
            "Alice",
            "alice@example.com",
        )

        print("Sample row inserted successfully.")

        # fetch() returns rows when your query produces results.
        rows = await connection.fetch("SELECT id, name, email FROM users ORDER BY id DESC LIMIT 5")

        print("Latest rows:")
        for row in rows:
            print(dict(row))
    finally:
        # Always close the connection so the event loop can shut down cleanly.
        await connection.close()


if __name__ == "__main__":
    # asyncio.run() starts the event loop and runs the coroutine to completion.
    asyncio.run(main())
