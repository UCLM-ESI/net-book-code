import socket
import signal

def int_handler(sig, frame):
    print("\nSIGINT recibido. Cerrando socket y saliendo...")
    sock.close()
    exit(0)

def handle(conn):
    data = bytes()
    while not data.endswith(b'\n'):
        data += conn.recv(1024)

    print(f"Se ha recibido el mensaje '{data}'")
    conn.sendall(b"Enviaste {len(data)} bytes")
    conn.close()

sock = socket.socket()
sock.bind(('', 2000))
sock.listen(5)
signal.signal(signal.SIGINT, int_handler)

while True:
    try:
        conn, client = sock.accept()
        handle(conn)
    except OSError:
        break
