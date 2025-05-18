import psycopg2

conn = psycopg2.connect(
                host="156.214.12.136",
                port=26257,
                user="ali",
                database="search_engine",
                sslmode="disable"

            )

cursor = conn.cursor()
