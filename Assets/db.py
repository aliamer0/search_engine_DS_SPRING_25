import mysql.connector

conn = mysql.connector.connect(
                host = "localhost",
                user = "ali430",
                password = "456430",
                database = "search_engine"
            )

cursor = conn.cursor()
