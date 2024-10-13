import socket
import threading
import time

# Fungsi untuk menangani setiap client
def handle_client(client_socket, address, metrics):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Koneksi dari {address}")
    
    try:
        while True:
            # Menerima pesan dari client
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Pesan dari {address}: {message}")

            # Mencatat waktu penerimaan pesan
            start_response_time = time.time()

            # Menyiapkan balasan ke client
            response = f"Pesan Anda '{message}' sudah diterima!"
            client_socket.send(response.encode())

            # Mencatat waktu pengiriman balasan
            end_response_time = time.time()
            response_time = end_response_time - start_response_time
            
            # Mengupdate metrik
            metrics['total_response_time'] += response_time
            metrics['total_messages'] += 1
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Balasan dikirim ke {address} dengan response time: {response_time:.2f} detik")

    except ConnectionResetError:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Client {address} terputus tiba-tiba.")
    finally:
        client_socket.close()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Koneksi ditutup dengan {address}")

# Fungsi untuk memulai server
def start_server(metrics):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))  # Menggunakan localhost dan port 12345
    server.listen(5)  # Server mendengarkan hingga 5 client pada saat bersamaan
    print("Server berjalan... Menunggu koneksi dari client...")

    while True:
        client_socket, addr = server.accept()  # Menerima koneksi dari client
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Koneksi baru dari {addr}")
        
        # Membuat thread baru untuk setiap client yang terhubung
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, metrics))
        client_thread.start()  # Memulai thread baru

if __name__ == "__main__":
    # Metrik untuk menghitung total response time dan total messages
    metrics = {'total_response_time': 0, 'total_messages': 0}
    start_server(metrics)
