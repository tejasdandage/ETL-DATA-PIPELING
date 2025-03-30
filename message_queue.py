import queue
import threading
import time

# Global message queue to replace Kafka
message_queue = queue.Queue()

# Flag to signal when producer is done
producer_done = threading.Event()

def produce_message(key, value):
    """Add a message to the queue"""
    message_queue.put((key, value))
    return True

def consume_message(timeout=1.0):
    """Get a message from the queue"""
    try:
        return message_queue.get(block=True, timeout=timeout)
    except queue.Empty:
        return None

def signal_producer_done():
    """Signal that the producer has finished"""
    producer_done.set()

def is_producer_done():
    """Check if the producer has signaled it's done"""
    return producer_done.is_set() and message_queue.empty()

def reset():
    """Reset the queue and flags for a new run"""
    # Clear the queue
    while not message_queue.empty():
        try:
            message_queue.get_nowait()
        except queue.Empty:
            break
    # Reset the producer done flag
    producer_done.clear()
