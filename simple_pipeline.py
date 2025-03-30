import requests
import json
import sqlite3
import time
from datetime import datetime

# ===== CONFIGURATION =====
API_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
DB_PATH = 'stock_data.db'
MAX_RECORDS = 100

# ===== DATABASE SETUP =====
def setup_database():
    print("Setting up database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table
    create_table = """
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    );
    """
    
    cursor.execute(create_table)
    conn.commit()
    print("Database setup complete.")
    
    return conn, cursor

# ===== FETCH DATA =====
def fetch_stock_data():
    print(f"Fetching stock data from {API_URL}")
    response = requests.get(API_URL)
    data = response.json()
    
    if 'Time Series (5min)' not in data:
        print(f"Error: Expected data format not found. Response: {data}")
        return None
    
    print(f"Successfully fetched data with {len(data['Time Series (5min)'])} records")
    return data['Time Series (5min)']

# ===== PROCESS AND STORE DATA =====
def process_data(time_series, cursor, conn):
    records_processed = 0
    
    for timestamp, values in time_series.items():
        if records_processed >= MAX_RECORDS:
            break
            
        try:
            # Convert string values to numeric
            open_price = float(values.get('1. open', 0))
            high_price = float(values.get('2. high', 0))
            low_price = float(values.get('3. low', 0))
            close_price = float(values.get('4. close', 0))
            volume = int(values.get('5. volume', 0))
            
            # Insert data
            insert_query = """
            INSERT INTO stock_data (timestamp, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(insert_query, (timestamp, open_price, high_price, low_price, close_price, volume))
            conn.commit()
            
            print(f"Processed record {records_processed+1}: {timestamp}")
            records_processed += 1
            
        except Exception as e:
            print(f"Error processing record {timestamp}: {e}")
    
    return records_processed

# ===== ANALYZE DATA =====
def analyze_data(cursor):
    print("\n===== DATA ANALYSIS =====\n")
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM stock_data")
    count = cursor.fetchone()[0]
    print(f"Total records: {count}")
    
    if count == 0:
        return
    
    # Get price statistics
    cursor.execute("SELECT AVG(open), AVG(close), MAX(high), MIN(low) FROM stock_data")
    avg_open, avg_close, max_high, min_low = cursor.fetchone()
    
    print(f"Average opening price: ${avg_open:.2f}")
    print(f"Average closing price: ${avg_close:.2f}")
    print(f"Highest price: ${max_high:.2f}")
    print(f"Lowest price: ${min_low:.2f}")
    
    # Get sample data
    cursor.execute("SELECT timestamp, open, high, low, close, volume FROM stock_data LIMIT 5")
    rows = cursor.fetchall()
    
    print("\nSample data:")
    print("Timestamp | Open | High | Low | Close | Volume")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")

# ===== MAIN FUNCTION =====
def run_pipeline():
    print("\n===== STARTING STOCK MARKET DATA PIPELINE =====\n")
    
    start_time = time.time()
    
    # Setup database
    try:
        conn, cursor = setup_database()
    except Exception as e:
        print(f"Database setup failed: {e}")
        return
    
    # Clear existing data
    try:
        cursor.execute("DELETE FROM stock_data")
        conn.commit()
        print("Cleared existing data.")
    except Exception as e:
        print(f"Failed to clear data: {e}")
    
    # Fetch data
    try:
        time_series = fetch_stock_data()
        if not time_series:
            print("No data to process. Exiting.")
            return
    except Exception as e:
        print(f"Data fetch failed: {e}")
        return
    
    # Process data
    try:
        records_processed = process_data(time_series, cursor, conn)
        print(f"\nSuccessfully processed {records_processed} records.")
    except Exception as e:
        print(f"Data processing failed: {e}")
        return
    
    # Analyze data
    try:
        analyze_data(cursor)
    except Exception as e:
        print(f"Data analysis failed: {e}")
    
    # Cleanup
    cursor.close()
    conn.close()
    
    end_time = time.time()
    print(f"\n===== PIPELINE COMPLETED IN {end_time - start_time:.2f} SECONDS =====\n")

if __name__ == "__main__":
    run_pipeline()
