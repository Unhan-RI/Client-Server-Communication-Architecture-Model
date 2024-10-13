import time

def log_event(event_type, timestamp, message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{event_type}: {timestamp} - {message}\n")

def log_connection():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_event("Connection", timestamp, "Client connected")

def log_message_sent(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_event("Message Sent", timestamp, message)

def log_message_received(response):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_event("Message Received", timestamp, response)