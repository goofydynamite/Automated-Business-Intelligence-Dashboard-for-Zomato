import psycopg2

# --- Database Connection Details ---
# It's better to use environment variables for this in a real project
DB_NAME = "zomato_db"
DB_USER = "postgres"
DB_PASSWORD = "your_postgres_password" # <-- IMPORTANT: Replace with your password!
DB_HOST = "localhost"
DB_PORT = "5432"

def run_sql_pipeline():
    """Connects to the DB and runs the SQL transformation script."""
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=12345,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        print("🐘 Database connection established.")

        # Path to your SQL script
        sql_file_path = 'sql/01_build_mart.sql'

        # Open and read the SQL file
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()

        # Execute the SQL script
        print(f"🚀 Executing SQL script: {sql_file_path}...")
        cur.execute(sql_script)
        conn.commit()
        print("✅ SQL pipeline executed successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
    run_sql_pipeline()