import argparse
import re
import sqlite3
import mysql.connector


def quote_identifier(name: str) -> str:
    if not re.match(r"^[A-Za-z0-9_]+$", name):
        raise ValueError(f"Unsafe table/column name: {name}")
    return f"`{name}`"


def get_sqlite_tables(sqlite_cursor):
    sqlite_cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)
    return [row[0] for row in sqlite_cursor.fetchall()]


def get_sqlite_columns(sqlite_cursor, table):
    sqlite_cursor.execute(f"PRAGMA table_info({quote_identifier(table)})")
    return [row[1] for row in sqlite_cursor.fetchall()]


def get_mysql_columns(mysql_cursor, table):
    mysql_cursor.execute(f"DESCRIBE {quote_identifier(table)}")
    return [row[0] for row in mysql_cursor.fetchall()]


def reset_auto_increment_if_needed(mysql_cursor, mysql_conn, table):
    try:
        mysql_cursor.execute(f"SHOW COLUMNS FROM {quote_identifier(table)} LIKE 'id'")
        row = mysql_cursor.fetchone()

        if not row:
            return

        # row format: Field, Type, Null, Key, Default, Extra
        extra = row[5] or ""

        if "auto_increment" not in extra.lower():
            return

        mysql_cursor.execute(f"SELECT MAX(`id`) FROM {quote_identifier(table)}")
        max_id = mysql_cursor.fetchone()[0]

        if max_id is not None:
            next_id = int(max_id) + 1
            mysql_cursor.execute(
                f"ALTER TABLE {quote_identifier(table)} AUTO_INCREMENT = {next_id}"
            )
            mysql_conn.commit()
            print(f"Reset AUTO_INCREMENT for {table} to {next_id}")

    except Exception as e:
        print(f"Skipping AUTO_INCREMENT reset for {table}: {e}")


def migrate_table(sqlite_cursor, mysql_cursor, mysql_conn, table, insert_ignore=False, batch_size=1000):
    print(f"\nMigrating table: {table}")

    sqlite_columns = get_sqlite_columns(sqlite_cursor, table)
    mysql_columns = get_mysql_columns(mysql_cursor, table)

    if not sqlite_columns:
        print(f"Skipping {table}: table not found in SQLite")
        return

    common_columns = [col for col in sqlite_columns if col in mysql_columns]

    if not common_columns:
        print(f"Skipping {table}: no matching columns between SQLite and MySQL")
        return

    missing_in_mysql = [col for col in sqlite_columns if col not in mysql_columns]
    if missing_in_mysql:
        print(f"Warning: columns missing in MySQL for {table}: {missing_in_mysql}")

    columns_sql = ", ".join(quote_identifier(col) for col in common_columns)
    placeholders = ", ".join(["%s"] * len(common_columns))

    insert_type = "INSERT IGNORE" if insert_ignore else "INSERT"

    insert_sql = f"""
        {insert_type} INTO {quote_identifier(table)} ({columns_sql})
        VALUES ({placeholders})
    """

    select_sql = f"""
        SELECT {columns_sql}
        FROM {quote_identifier(table)}
    """

    sqlite_cursor.execute(select_sql)

    total = 0

    while True:
        rows = sqlite_cursor.fetchmany(batch_size)

        if not rows:
            break

        mysql_cursor.executemany(insert_sql, rows)
        mysql_conn.commit()

        total += len(rows)
        print(f"Inserted {total} rows into {table}")

    reset_auto_increment_if_needed(mysql_cursor, mysql_conn, table)

    print(f"Done: {table}, total rows migrated: {total}")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate data from SQLite to already-created MySQL tables."
    )

    parser.add_argument("--sqlite-db", required=True, help="Path to SQLite DB file")
    parser.add_argument("--mysql-host", default="localhost")
    parser.add_argument("--mysql-port", type=int, default=3306)
    parser.add_argument("--mysql-user", required=True)
    parser.add_argument("--mysql-password", required=True)
    parser.add_argument("--mysql-db", required=True)
    parser.add_argument("--table", help="Single table name to migrate")
    parser.add_argument("--all-tables", action="store_true", help="Migrate all SQLite tables")
    parser.add_argument("--insert-ignore", action="store_true", help="Skip duplicate rows")
    parser.add_argument("--batch-size", type=int, default=1000)

    args = parser.parse_args()

    if not args.table and not args.all_tables:
        raise ValueError("Provide either --table TABLE_NAME or --all-tables")

    sqlite_conn = sqlite3.connect(args.sqlite_db)
    sqlite_cursor = sqlite_conn.cursor()

    mysql_conn = mysql.connector.connect(
        host=args.mysql_host,
        port=args.mysql_port,
        user=args.mysql_user,
        password=args.mysql_password,
        database=args.mysql_db,
    )
    mysql_cursor = mysql_conn.cursor()

    try:
        if args.all_tables:
            tables = get_sqlite_tables(sqlite_cursor)
        else:
            tables = [args.table]

        for table in tables:
            migrate_table(
                sqlite_cursor=sqlite_cursor,
                mysql_cursor=mysql_cursor,
                mysql_conn=mysql_conn,
                table=table,
                insert_ignore=args.insert_ignore,
                batch_size=args.batch_size,
            )

    finally:
        sqlite_cursor.close()
        sqlite_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

    print("\nMigration completed.")


if __name__ == "__main__":
    main()