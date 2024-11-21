import socket
import threading

# IP e portas dos servidores
SERVERS = [("localhost", 5001), ("localhost", 5002)]
current_server_index = 0  # Índice para alternar entre os servidores

# Função para encaminhar a mensagem ao servidor atual
def forward_to_server(message):
    global current_server_index
    attempts = len(SERVERS)  # Tentativas para alternar entre servidores
    response = None

    while attempts > 0:
        server_ip, server_port = SERVERS[current_server_index]
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((server_ip, server_port))
            server.send(message.encode())
            response = server.recv(1024).decode()
            server.close()
            print(f"Resposta do servidor {server_ip}:{server_port} - {response}")
            return response
        except ConnectionRefusedError:
            print(f"ERRO: Servidor {server_ip}:{server_port} indisponível.")
            # Alternar para o próximo servidor em caso de falha
            current_server_index = (current_server_index + 1) % len(SERVERS)
            attempts -= 1

    return "ERRO: Nenhum servidor disponível."

# Função para lidar com as conexões dos clientes no middleware
def handle_middleware(conn, addr):
    try:
        message = conn.recv(1024).decode()
        action, data = message.split("|", 1)

        if action in ["REGISTER", "LOOKUP"]:
            response = forward_to_server(message)
            conn.send(response.encode())
        else:
            conn.send("AÇÃO_INVÁLIDA".encode())
    except Exception as e:
        print(f"Erro ao lidar com middleware {addr}: {e}")
    finally:
        conn.close()

# Função para iniciar o servidor middleware
def start_middleware(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen()
    print(f"Middleware iniciado em localhost:{port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_middleware, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    port = int(input("Digite a porta do middleware (5000 por padrão): ") or 5000)
    start_middleware(port)
