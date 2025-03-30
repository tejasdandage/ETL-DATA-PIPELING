# Real-time Data Pipeline for Stock Market Analysis

## Overview
This project demonstrates a real-time data pipeline designed to ingest, process, and analyze stock market data. Using tools like Apache Kafka, SQLite/PostgreSQL, and Python, the pipeline captures stock data and stores it in a robust data architecture, enabling timely analysis and insights.

## Project Highlights
* **Data Ingestion**: Real-time stock data is fetched using APIs from Alpha Vantage and ingested into the pipeline.
* **Stream Processing**: In the full version, Apache Kafka acts as the streaming platform to handle data flow between producers and consumers.
* **Data Storage**: Data is stored in a database (SQLite for local testing, PostgreSQL for production), enabling efficient query execution and data retrieval.
* **Real-time Analysis**: The pipeline processes data on-the-fly, providing up-to-the-minute insights into stock performance.

## Project Versions

### Simple Local Version
A simplified version that runs entirely locally using:
* Python's built-in modules
* SQLite database
* Alpha Vantage API (demo key)

To run the simple version:
```bash
python simple_pipeline.py
```

### Full Version
The complete implementation using:
* Apache Kafka for streaming
* PostgreSQL for data storage
* Alpha Vantage API for data sourcing

## Technologies Used
* Python: Scripting for producer and consumer operations
* Apache Kafka: Streaming platform for real-time data handling (full version)
* SQLite: Lightweight database for local development
* PostgreSQL: Production database for the full implementation
* APIs (Alpha Vantage): Data source for stock market data

## Architecture
1. **Producer**: Fetches stock data from Alpha Vantage API and sends it to the message queue/Kafka
2. **Message Queue/Kafka**: Handles the flow of data between producer and consumer
3. **Consumer**: Reads from the queue and loads data into the database
4. **Database**: Stores the data for analysis and visualization
5. **Analysis**: SQL queries provide insights into the stock data

## Setup and Installation
See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed instructions on setting up and running the project locally.

## Future Enhancements
* Visualization dashboard using Plotly or Dash
* Support for multiple stock symbols
* Historical data analysis and trend prediction
* Real-time alerts for significant price movements

## Author
Tejas Dandage ([@tejasdandage](https://github.com/tejasdandage))

## License
MIT
