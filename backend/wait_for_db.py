import time
import socket
import os
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres():
    print("⏳ Waiting for PostgreSQL to be ready...")
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get("DB_NAME", "mollidays_db"),
                user=os.environ.get("DB_USER", "myo"),
                password=os.environ.get("DB_PASSWORD", "toor"),
                host=os.environ.get("DB_HOST", "db"),
                port=os.environ.get("DB_PORT", "5432"),
            )
            conn.close()
            print("✅ PostgreSQL is ready!")
            break
        except OperationalError:
            print("❌ PostgreSQL not ready yet, retrying in 1s...")
            time.sleep(1)

def wait_for_socket(host, port):
    print(f"⏳ Waiting for {host}:{port}...")
    while True:
        try:
            with socket.create_connection((host, port), timeout=3):
                print(f"✅ {host}:{port} is available!")
                return
        except OSError:
            print(f"❌ {host}:{port} not available, retrying in 2s...")
            time.sleep(2)

if __name__ == '__main__':
    wait_for_postgres()
    wait_for_socket("mongo", 27017)
