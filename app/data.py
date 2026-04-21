# 55-Cancri-Ae (Michelle Chen, Natalie Kieger, Ethan Cheung, Thamidur Rahman)
import sqlite3                      # enable control of an sqlite database
import pandas as pd
import os

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "planets.csv")
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")

def load_csv():
    if not os.path.exists(DB_FILE):
        df = pd.read_csv(CSV_FILE)
        conn = sqlite3.connect(DB_FILE)
        df.to_sql("planets", conn, if_exists="replace", index=False)
        conn.close()
        print(f"Loaded {len(df)} planets into SQLite.")

def load_planets():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM planets", conn)
    conn.close()
    return df

load_csv()