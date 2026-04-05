import mysql.connector

def get_conn(database=None):
    print("🔌 Connecting to MySQL...")

    try:
        conn_params = {
            "host": "localhost",
            "user": "root",
            "password": "YOUR_PASSWORD_HERE"
        }
        
        # Add database if provided
        if database:
            conn_params["database"] = database
            print(f"📁 Connecting to database: {database}")
        
        conn = mysql.connector.connect(**conn_params)

        print("✅ MySQL Connected Successfully")
        return conn

    except Exception as e:
        print("❌ DB Connection Failed:", e)
        return None