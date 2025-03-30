import sqlite3

# SQLite Database path
db_path = 'stock_data.db'

try:
    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Connected to SQLite database at {db_path}")
    
    # Query to check the data
    query = "SELECT COUNT(*) FROM stock_data"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Total records in stock_data table: {count}")
    
    if count > 0:
        # Get sample data
        sample_query = "SELECT timestamp, open, high, low, close, volume FROM stock_data LIMIT 5"
        cursor.execute(sample_query)
        rows = cursor.fetchall()
        
        print("\nSample data:")
        print("Timestamp | Open | High | Low | Close | Volume")
        print("-" * 70)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
        
        # Calculate average closing price
        avg_query = "SELECT AVG(close) FROM stock_data"
        cursor.execute(avg_query)
        avg_close = cursor.fetchone()[0]
        print(f"\nAverage closing price: ${avg_close:.2f}")
        
        # Find highest and lowest prices
        high_low_query = "SELECT MAX(high), MIN(low) FROM stock_data"
        cursor.execute(high_low_query)
        max_high, min_low = cursor.fetchone()
        print(f"Highest price: ${max_high:.2f}")
        print(f"Lowest price: ${min_low:.2f}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close connections
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("\nConnection closed.")
