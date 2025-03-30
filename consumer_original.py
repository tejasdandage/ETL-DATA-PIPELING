from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import psycopg2

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'your-kafka-bootstrap-server:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'YOUR_KAFKA_USERNAME',
    'sasl.password': 'YOUR_KAFKA_PASSWORD',
    'group.id': 'your-group-id',
    'auto.offset.reset': 'earliest'
}

# Initialize Kafka Consumer
consumer = Consumer(**consumer_config)

# Subscribe to the topic
topic = 'stock_data'
consumer.subscribe([topic])

# PostgreSQL Connection Details
db_config = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your-database-host',
    'port': 5432
}

# Connect to PostgreSQL Database
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to PostgreSQL database.")
except Exception as e:
    print(f"Failed to connect to PostgreSQL: {e}")
    exit(1)

# Create the table if it doesn't exist
create_table = """
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    timestamp VARCHAR(50),
    open NUMERIC(10,4),
    high NUMERIC(10,4),
    low NUMERIC(10,4),
    close NUMERIC(10,4),
    volume INTEGER
);
"""
cursor.execute(create_table)
conn.commit()

# Function to insert data into PostgreSQL
def insert_data(timestamp, data):
    """Inserts stock data into the PostgreSQL database."""
    try:
        # Convert string values to numeric
        open_price = float(data.get('1. open', 0))
        high_price = float(data.get('2. high', 0))
        low_price = float(data.get('3. low', 0))
        close_price = float(data.get('4. close', 0))
        volume = int(data.get('5. volume', 0))
        
        # Insert data into the table
        insert_query = """
        INSERT INTO stock_data (timestamp, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (timestamp, open_price, high_price, low_price, close_price, volume))
        conn.commit()
        print(f"Inserted data for timestamp: {timestamp}")
    except Exception as e:
        print(f"Failed to insert data: {e}")
        conn.rollback()

# Consumer Loop
try:
    while True:
        # Poll Kafka for messages
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition {msg.partition()}")
            else:
                print(f"Error: {msg.error()}")
        else:
            # Process received message
            timestamp = msg.key().decode('utf-8')
            value = json.loads(msg.value().decode('utf-8'))
            print(f"Received message: timestamp={timestamp}")
            
            # Insert data into PostgreSQL
            insert_data(timestamp, value)

except KeyboardInterrupt:
    print("Consumer stopped by user")

finally:
    # Close connections
    consumer.close()
    cursor.close()
    conn.close()
    print("Connections closed.")
