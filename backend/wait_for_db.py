import time
import psycopg2
from psycopg2 import OperationalError

print("⏳ Waiting for PostgreSQL to be ready...")

while True:
    try:
        conn = psycopg2.connect(
            dbname="mollidays_db",
            user="myo",
            password="toor",
            host="db",
            port="5432",
        )
        conn.close()
        print("✅ PostgreSQL is ready!")
        break
    except OperationalError:
        print("❌ PostgreSQL not ready yet, waiting 1s...")
        time.sleep(1)
