import socket
import time
import threading

def send_messages(client_id, message_count, metrics):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))  # Menghubungkan client ke server (localhost:12345)

    for i in range(message_count):
        message = f"Pesan {i+1} dari client {client_id}"
        
        # Mencatat waktu pengiriman pesan
        start_time = time.time()
        client.send(message.encode())  # Mengirim pesan ke server

        # Menerima balasan dari server
        response = client.recv(1024).decode()
        end_time = time.time()  # Waktu setelah menerima balasan dari server
        
        # Menghitung latency
        latency = end_time - start_time
        metrics['total_latency'] += latency
        metrics['total_messages'] += 1
        print(f"[Client {client_id}] Balasan dari server: {response} | Latency: {latency:.2f} detik")

    client.close()

def start_clients(client_count, message_count, metrics):
    threads = []
    for i in range(client_count):
        thread = threading.Thread(target=send_messages, args=(i + 1, message_count, metrics))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    # Hitung dan tampilkan metrik setelah semua client selesai
    average_latency = metrics['total_latency'] / metrics['total_messages'] if metrics['total_messages'] > 0 else 0
    print(f"\nRata-rata Latency: {average_latency:.2f} detik")
    print(f"Total Pesan yang Diproses: {metrics['total_messages']}")

if __name__ == "__main__":
    # Metrik untuk menghitung total latency dan total messages
    metrics = {'total_latency': 0, 'total_messages': 0}

    client_count = 10  # Jumlah client yang akan diujikan
    message_count = 5  # Jumlah pesan yang akan dikirim per client

    start_clients(client_count, message_count, metrics)
