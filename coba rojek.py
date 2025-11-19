import psycopg2
import pandas as pd

def connectDB():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "NOIDAJA",
            dbname = "bekerja",
        )
        cur = conn.cursor()
        print("Koneksi Berhasil")
        return conn, cur
    except Exception:
        print("Koneksi gagal, coba lagi")
        return None

connectDB()