import socket

HOST = "192.168.131.39"
PORT = 30000

x_start = 1
y_start = 1

x_ziel = 2
y_ziel = 2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server läuft auf {HOST}:{PORT}, wartet auf Verbindung...")

client_socket, client_address = server_socket.accept()
print(f"Verbindung von {client_address} angenommen.")

# Nachricht empfangen (z. B. "send")
data = client_socket.recv(1024).decode()
print(f"Empfangen: {data}")

# Wenn Client "send" schreibt, dann sende zwei Werte
if data.strip() == "send":
    msg = f'({x_start},{y_start},{x_ziel},{y_ziel})\n'
    client_socket.sendall(msg.encode())
    print(f"Gesendet: {msg.strip()}")

client_socket.close()
server_socket.close()
