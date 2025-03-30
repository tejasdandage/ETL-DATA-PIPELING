from confluent_kafka import Producer
import requests
import json

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': 'your-kafka-bootstrap-server:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'YOUR_KAFKA_USERNAME',
    'sasl.password': 'YOUR_KAFKA_PASSWORD'
}
producer = Producer(**producer_config)

# Fetch stock data
URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=YOUR_API_KEY'
response = requests.get(URL)
data = response.json()

# Delivery report callback for produced messages
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Produce messages to the topic
topic = 'stock_data'
message_count = 0
max_messages = 100  # Maximum number of messages to send

try:
    for timestamp, values in data['Time Series (5min)'].items():
        if message_count >= max_messages:
            print("Reached maximum number of messages. Stopping producer.")
            break
        
        record_key = timestamp
        record_value = json.dumps(values)
        producer.produce(topic, key=record_key, value=record_value, callback=delivery_report)
        producer.poll(1)
        message_count += 1

except Exception as e:
    print(f'Failed to produce message: {e}')

producer.flush()
print(f"Producer completed. Sent {message_count} messages.")
