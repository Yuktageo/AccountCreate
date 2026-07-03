import sqlite3
import mysql.connector

SQLITE_DB = "a2a.sqlite"
MYSQL_TABLE = "tasks"   # change this to your A2A table name

mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="your_mysql_db",
)

sqlite_conn = sqlite3.connect(SQLITE_DB)

sqlite_cursor = sqlite_conn.cursor()
mysql_cursor = mysql_conn.cursor()

# Read data from SQLite
sqlite_cursor.execute(f"SELECT * FROM {MYSQL_TABLE}")
rows = sqlite_cursor.fetchall()

# Get SQLite column names
columns = [desc[0] for desc in sqlite_cursor.description]

columns_sql = ", ".join([f"`{col}`" for col in columns])
placeholders = ", ".join(["%s"] * len(columns))

insert_sql = f"""
INSERT INTO `{MYSQL_TABLE}` ({columns_sql})
VALUES ({placeholders})
"""

if rows:
    mysql_cursor.executemany(insert_sql, rows)
    mysql_conn.commit()

print(f"Migrated {len(rows)} rows into {MYSQL_TABLE}")

sqlite_cursor.close()
sqlite_conn.close()

mysql_cursor.close()
mysql_conn.close()