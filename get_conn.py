import mysql.connector

def get_conn():
    print("🔌 Connecting to MySQL...")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="db"
        )

        print("✅ MySQL Connected Successfully")
        return conn

    except Exception as e:
        print("❌ DB Connection Failed:", e)
        return None