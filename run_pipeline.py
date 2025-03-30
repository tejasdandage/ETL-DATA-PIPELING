import subprocess
import time
import os
import sys

def run_pipeline():
    print("\n===== STARTING STOCK MARKET DATA PIPELINE =====\n")
    
    # Check if SQLite database exists and delete it to start fresh
    if os.path.exists('stock_data.db'):
        print("Removing existing database to start fresh...")
        os.remove('stock_data.db')
    
    # Start the consumer in a separate process
    print("\n1. Starting consumer...")
    consumer_process = subprocess.Popen([sys.executable, 'consumer.py'], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
    
    # Give the consumer time to initialize
    time.sleep(2)
    
    # Start the producer
    print("\n2. Starting producer...")
    producer_process = subprocess.Popen([sys.executable, 'producer.py'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
    
    # Wait for producer to finish
    producer_stdout, producer_stderr = producer_process.communicate()
    print("\n3. Producer completed.")
    
    # Give consumer time to process all messages
    print("\n4. Waiting for consumer to process all messages...")
    time.sleep(5)
    
    # Terminate consumer (it should exit on its own, but just in case)
    consumer_process.terminate()
    consumer_stdout, consumer_stderr = consumer_process.communicate()
    
    # Check the data
    print("\n5. Checking the data...")
    check_process = subprocess.run([sys.executable, 'check_data.py'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
    
    print(check_process.stdout)
    
    if check_process.stderr:
        print("Errors during data check:")
        print(check_process.stderr)
    
    print("\n===== PIPELINE EXECUTION COMPLETED =====\n")
    
    # Print logs automatically
    print("\n===== PRODUCER LOGS =====\n")
    print(producer_stdout)
    if producer_stderr:
        print("\n===== PRODUCER ERRORS =====\n")
        print(producer_stderr)
        
    print("\n===== CONSUMER LOGS =====\n")
    print(consumer_stdout)
    if consumer_stderr:
        print("\n===== CONSUMER ERRORS =====\n")
        print(consumer_stderr)

if __name__ == "__main__":
    run_pipeline()
