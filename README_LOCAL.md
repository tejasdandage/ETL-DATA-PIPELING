# Real-time Data Pipeline for Stock Market Analysis (Local Version)

This is a simplified local version of the stock market data pipeline that doesn't require external services like Kafka or PostgreSQL. Instead, it uses Python's built-in modules and SQLite for a complete local experience.

## Overview

This project demonstrates a data pipeline that:
1. Fetches real-time stock data from Alpha Vantage API
2. Passes it through a message queue (simulating Kafka)
3. Stores it in a SQLite database (replacing PostgreSQL)
4. Provides analysis capabilities

## Prerequisites

- Python 3.x
- Internet connection (for Alpha Vantage API)

## Setup Instructions

1. Make sure you're in the project directory
2. Activate the virtual environment:
   ```
   .\venv\Scripts\activate
   ```
3. Install required packages:
   ```
   pip install requests
   ```

## Running the Pipeline

You can run the entire pipeline with a single command:

```
python run_pipeline.py
```

This will:
1. Start the consumer (which connects to SQLite)
2. Start the producer (which fetches data from Alpha Vantage)
3. Process all messages through the queue
4. Check and display the results

## Components

### Producer (producer.py)
- Fetches stock data from Alpha Vantage API
- Sends data to the message queue

### Message Queue (message_queue.py)
- In-memory queue that simulates Kafka
- Handles communication between producer and consumer

### Consumer (consumer.py)
- Reads messages from the queue
- Stores data in SQLite database

### Data Checker (check_data.py)
- Queries the SQLite database
- Displays statistics and sample data

## Data Analysis

After running the pipeline, the data is stored in `stock_data.db` (SQLite database). You can:

1. View basic statistics with `python check_data.py`
2. Use any SQLite client to perform more complex queries
3. Export the data for visualization in tools like Excel or Python plotting libraries

## Notes

- This uses the Alpha Vantage demo API key, which has limited functionality
- For a production setup, you would need your own Alpha Vantage API key
- The local setup is designed for learning and testing, not for production use
