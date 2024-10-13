# Client-Server-Communication-Architecture-Model
Implementasi Analisis Komunikasi Peer-to-Peer dalam Sistem Terdistribusi
Azzam Amar Ma'ruf (320220401002)
Bainul Dwi Tri Putra (320220401003)

Berikut penjelasan mendetail tentang cara kerja kode server, client, dan pencatatan log dalam sistem terdistribusi dengan arsitektur **client-server**. Sistem ini memungkinkan komunikasi antara beberapa **client** dan **server**, di mana setiap komunikasi dicatat dalam log. 

### 1. **Arsitektur Client-Server**
Dalam arsitektur client-server:
- **Server**: Sebuah program atau perangkat yang menyediakan layanan (seperti menerima permintaan, memprosesnya, dan mengirimkan respon) kepada banyak client. Dalam kode yang dibuat, server mendengarkan permintaan dari beberapa client sekaligus.
- **Client**: Sebuah program atau perangkat yang mengirimkan permintaan ke server untuk memproses sesuatu (misalnya, pesan atau data). Setelah server memproses permintaan, server mengirimkan respon kembali ke client.

Sistem ini **terdistribusi** karena client dan server bisa berjalan di komputer atau perangkat yang berbeda, meskipun pada kasus tertentu, mereka bisa dijalankan pada perangkat yang sama (loopback connection).

### 2. **Kode Server** dan Cara Kerjanya

Kode server bertugas untuk:
- Menunggu koneksi dari client.
- Menerima pesan dari client.
- Membalas pesan client.
- Mengelola beberapa koneksi secara bersamaan menggunakan multithreading.

#### Bagian Kunci Kode Server:
1. **Socket Creation**:
   Server menggunakan **socket** untuk berkomunikasi. Socket pada server akan mendengarkan koneksi yang masuk dari client pada alamat IP dan port tertentu.

   ```python
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.bind((host, port))  # Bind server ke alamat dan port tertentu
   server_socket.listen(5)  # Dengarkan koneksi masuk
   ```

2. **Multithreading**:
   Server menggunakan multithreading untuk menangani banyak client sekaligus. Setiap kali client terkoneksi, server akan membuat thread baru untuk menangani komunikasi dengan client tersebut secara paralel.

   ```python
   client_thread = threading.Thread(target=handle_client, args=(client_socket,))
   client_thread.start()
   ```

3. **Handling Client**:
   Server menjalankan fungsi `handle_client()` untuk menerima pesan dari client dan mengirimkan balasan kembali. Setiap thread menangani satu client secara mandiri, memungkinkan banyak client untuk terhubung ke server secara bersamaan.

   ```python
   def handle_client(client_socket):
       while True:
           message = client_socket.recv(1024).decode()
           if not message:
               break
           # Balas pesan
           client_socket.send(f"Server received: {message}".encode())
   ```

4. **Logging**:
   Setiap kali server menerima koneksi atau pesan dari client, peristiwa ini dicatat dalam log dengan waktu yang tepat (timestamp). Misalnya:
   - **Log Koneksi Client**: Dicatat saat client terhubung.
   - **Log Pesan yang Diterima**: Dicatat saat server menerima pesan dari client.

   ```python
   log_event("Connection", timestamp, f"Client {client_address} connected")
   log_event("Message Received", timestamp, message)
   ```

#### Alur Kerja Server:
1. Server mendengarkan di port yang ditentukan untuk menerima koneksi dari client.
2. Ketika client terhubung, server menerima pesan dari client.
3. Server membalas pesan tersebut, mencatat waktu koneksi dan pesan dalam log.
4. Server terus mendengarkan pesan baru dari client atau client lain.

### 3. **Kode Client** dan Cara Kerjanya

Kode client bertugas untuk:
- Membuat koneksi ke server.
- Mengirim pesan ke server.
- Menerima balasan dari server.
- Mencatat waktu pengiriman pesan dalam log di sisi client.

#### Bagian Kunci Kode Client:
1. **Socket Creation**:
   Client juga menggunakan **socket** untuk berkomunikasi dengan server. Client harus tahu alamat IP dan port server agar bisa mengirim pesan.

   ```python
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client_socket.connect((host, port))  # Terhubung ke server
   ```

2. **Sending Messages**:
   Setelah terkoneksi, client bisa mengirim pesan ke server. Pesan ini dikirim sebagai string yang di-*encode* menjadi byte karena socket bekerja dengan data berbasis byte.

   ```python
   client_socket.send(message.encode())
   ```

3. **Receiving Responses**:
   Client menerima balasan dari server setelah pesan dikirim. Balasan tersebut dikirim kembali dalam bentuk byte dan harus di-*decode* menjadi string agar bisa dibaca.

   ```python
   response = client_socket.recv(1024).decode()
   ```

4. **Logging**:
   Client juga mencatat log waktu pengiriman pesan dan waktu menerima balasan dari server untuk memantau **latency** (waktu tunda) komunikasi antara client dan server.

   ```python
   log_message_sent(message)  # Mencatat waktu pengiriman pesan
   log_message_received(response)  # Mencatat waktu penerimaan balasan
   ```

#### Alur Kerja Client:
1. Client membuat koneksi ke server menggunakan socket.
2. Client mengirim pesan ke server.
3. Server menerima pesan dan mengirimkan balasan.
4. Client menerima balasan dari server.
5. Client mencatat waktu pengiriman dan penerimaan pesan dalam file log.

### 4. **Kode Pencatatan Log (Logging System)**

Pencatatan log sangat penting dalam sistem terdistribusi karena membantu menganalisis performa sistem. Dalam sistem ini, pencatatan dilakukan di dua tempat:
- **Server** mencatat koneksi client dan pesan yang diterima dari client.
- **Client** mencatat pesan yang dikirim ke server dan balasan yang diterima dari server.

#### Bagian Kunci Logging:
1. **`log_event()`**: 
   Fungsi ini menulis semua peristiwa ke file log (`log.txt`). Setiap event yang terjadi dicatat dengan format:
   ```
   [Event_Type]: [Timestamp] - [Message]
   ```
   Di mana:
   - **Event_Type**: Jenis peristiwa, seperti koneksi atau pengiriman pesan.
   - **Timestamp**: Waktu saat peristiwa terjadi.
   - **Message**: Deskripsi peristiwa.

2. **Waktu yang Dicatat**:
   - Waktu pengiriman pesan dari client.
   - Waktu penerimaan balasan dari server.
   - Waktu koneksi pertama kali dibuat.
   
   Fungsi `time.strftime()` digunakan untuk mencatat waktu dengan format `YYYY-MM-DD HH:MM:SS`.

3. **Contoh Isi Log**:
   File log yang dihasilkan bisa berisi data seperti:
   ```
   Connection: 2024-10-13 14:35:24 - Client connected
   Message Sent: 2024-10-13 14:35:45 - Hello, Server!
   Message Received: 2024-10-13 14:35:46 - Hello, Client!
   ```

#### Alur Pencatatan Log:
1. Setiap kali client terhubung atau pesan dikirim/dibalas, waktu peristiwa dicatat oleh fungsi `log_event()`.
2. Log dicatat baik di sisi server maupun di sisi client.
3. Log ini membantu memantau latensi, respon, throughput, dan performa sistem.

### 5. **Performa Sistem Terdistribusi**
Dalam konteks **analisis performa**:
- **Latensi** adalah waktu tunda antara pengiriman pesan oleh client dan penerimaan balasan dari server. Dicatat di client.
- **Throughput** adalah jumlah pesan yang diproses oleh server dalam jangka waktu tertentu.
- **Respon** mengacu pada kecepatan server membalas setiap pesan client.

Server yang menggunakan multithreading dapat menangani banyak client dalam waktu yang bersamaan. Dengan pencatatan log di setiap peristiwa, kita bisa mengukur:
- Berapa lama waktu yang dibutuhkan client untuk menerima balasan.
- Berapa banyak pesan yang diproses oleh server dalam rentang waktu tertentu.
- Apakah ada perbedaan signifikan dalam performa saat server menangani banyak client.

### Kesimpulan
Dalam arsitektur client-server ini:
- **Server** menerima dan membalas pesan dari beberapa client secara bersamaan menggunakan multithreading.
- **Client** mengirim pesan ke server dan menerima balasan.
- **Sistem logging** mencatat setiap peristiwa komunikasi (seperti koneksi, pengiriman, dan penerimaan pesan) di server dan client. Ini memungkinkan pemantauan latensi, respon, dan throughput dalam sistem terdistribusi.
