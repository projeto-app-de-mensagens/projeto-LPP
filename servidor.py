import socket
import threading
import json

REGISTRY_FILE = "registros.json"

def load_registry():
    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_registry(clients):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(clients, f, indent=4)

def handle_middleware(conn, addr):
    clients = load_registry()

    try:
        message = conn.recv(1024).decode()
        action, data = message.split("|", 1)

        if action == "REGISTER":
            identifier, client_ip, client_port = data.split(",")
            clients[identifier] = {"ip": client_ip, "port": int(client_port)}
            save_registry(clients)
            print(f"Cliente {identifier} registrado com IP {client_ip} e porta {client_port}.")
            conn.send("REGISTERED".encode())

        elif action == "LOOKUP":
            target_id = data
            if target_id in clients:
                client_ip = clients[target_id]["ip"]
                client_port = clients[target_id]["port"]
                response = f"{client_ip},{client_port}"
                conn.send(response.encode())
            else:
                conn.send("NOT_FOUND".encode())

    except Exception as e:
        print(f"Erro ao lidar com middleware {addr}: {e}")
    finally:
        conn.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen()
    print(f"Servidor iniciado em localhost:{port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_middleware, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    port = int(input("Digite a porta do servidor (5001 ou 5002): "))
    start_server(port)
