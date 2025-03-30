# Local Setup for Real-time Data Pipeline

This document provides instructions for running the stock market data pipeline locally using Docker.

## Prerequisites

- Docker and Docker Compose installed on your machine
- Python 3.x
- pip (Python package manager)

## Setup Instructions

### 1. Start the Docker containers

Run the following command to start Kafka and PostgreSQL containers:

```bash
docker-compose up -d
```

This will start:
- Zookeeper (required by Kafka)
- Kafka broker on localhost:9092
- PostgreSQL database on localhost:5432

### 2. Install Python dependencies

```bash
pip install confluent-kafka requests psycopg2-binary
```

### 3. Run the consumer

Open a terminal and run:

```bash
python consumer.py
```

The consumer will connect to Kafka and PostgreSQL, create the necessary table, and wait for messages.

### 4. Run the producer

Open another terminal and run:

```bash
python producer.py
```

The producer will fetch stock data from Alpha Vantage API and send it to Kafka.

### 5. Check the data

After running the producer and consumer, you can check the data in PostgreSQL by running:

```bash
python check_data.py
```

## Stopping the Environment

To stop the Docker containers, run:

```bash
docker-compose down
```

## Architecture

1. **Producer**: Fetches stock data from Alpha Vantage API and sends it to Kafka
2. **Kafka**: Acts as the message broker
3. **Consumer**: Reads messages from Kafka and stores them in PostgreSQL
4. **PostgreSQL**: Stores the stock data for analysis

## Notes

- This setup uses the Alpha Vantage demo API key, which has limited functionality
- For a production setup, you would need your own Alpha Vantage API key
- The local setup doesn't include authentication for Kafka and PostgreSQL for simplicity
