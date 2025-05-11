import psycopg2

conn = psycopg2.connect(
                host="197.53.138.226",
                port=26257,
                user="ali",
                database="search_engine",
                sslmode="disable"

            )

cursor = conn.cursor()
