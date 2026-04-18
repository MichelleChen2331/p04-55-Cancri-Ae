# 55-Cancri-Ae (Michelle Chen, Natalie Kieger, Ethan Cheung, Thamidur Rahman)
import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import pandas as pd
import requests
from urllib.parse import urlencode

DB_FILE="data.db"

def fetch_and_store():
    """Call NASA API once and save results to database."""

    sql = """
        SELECT pl_name, disc_year, discoverymethod, pl_orbper, pl_orbsmax, pl_rade, pl_masse
        FROM pscomppars
        WHERE disc_year IS NOT NULL
        AND pl_orbper IS NOT NULL
        AND pl_orbsmax IS NOT NULL
        AND pl_rade IS NOT NULL
        AND pl_masse IS NOT NULL

    """
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urlencode({
        "query": sql,
        "format": "json"
         })
    df = pd.DataFrame(requests.get(url, timeout=15).json())

    conn = sqlite3.connect(DB_FILE)
    df.to_sql("planets", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Stored {len(df)} planets in SQLite.")

def load_planets():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM planets", conn)
    conn.close()
    return df

if __name__ == "__main__":
    fetch_and_store()
