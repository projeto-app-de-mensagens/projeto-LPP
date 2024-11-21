import socket
import threading

# Função para registrar o cliente no middleware
def register_on_middleware(middleware_ip, middleware_port, identifier, udp_port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((middleware_ip, middleware_port))
        client.send(f"REGISTER|{identifier},{socket.gethostbyname(socket.gethostname())},{udp_port}".encode())
        response = client.recv(1024).decode()
        client.close()
        return response
    except ConnectionRefusedError:
        return "ERRO: Middleware indisponível."

# Função para enviar uma mensagem UDP para outro cliente
def send_udp_message(ip, port, message):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(message.encode(), (ip, port))
        print(f"Mensagem enviada para {ip}:{port}")
    except Exception as e:
        print(f"Erro ao enviar mensagem UDP: {e}")

# Função para escutar mensagens UDP
def start_udp_listener(udp_port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", udp_port))  # Escuta em todas as interfaces
    print(f"Escutando mensagens UDP na porta {udp_port}...")

    while True:
        try:
            message, addr = udp_socket.recvfrom(1024)
            print(f"Mensagem recebida de {addr}: {message.decode()}")
        except Exception as e:
            print(f"Erro ao receber mensagem UDP: {e}")

# Interface principal do cliente
def client_interface(middleware_ip, middleware_port, identifier, udp_port):
    response = register_on_middleware(middleware_ip, middleware_port, identifier, udp_port)
    if response == "REGISTERED":
        print("Registrado com sucesso no middleware.")
    elif response.startswith("ERRO"):
        print(response)
        return
    else:
        print("Falha ao registrar no middleware.")
        return

    while True:
        print("\nEscolha uma opção:")
        print("1. Enviar mensagem para outro cliente (UDP)")
        print("2. Sair")

        option = input("Opção: ")

        if option == "1":
            target_id = input("Digite o identificador do cliente destinatário: ")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((middleware_ip, middleware_port))
            client.send(f"LOOKUP|{target_id}".encode())
            response = client.recv(1024).decode()
            client.close()

            if response == "NOT_FOUND":
                print("Cliente destinatário não encontrado.")
            else:
                target_ip, target_port = response.split(",")
                message = input("Digite a mensagem a ser enviada: ")
                send_udp_message(target_ip, int(target_port), message)

        elif option == "2":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Inicializar o cliente
if __name__ == "__main__":
    middleware_ip = input("Digite o IP do middleware (localhost para local): ") or "localhost"
    middleware_port = int(input("Digite a porta do middleware (5000 por padrão): ") or 5000)
    identifier = input("Digite seu identificador: ")
    udp_port = int(input("Digite sua porta UDP para receber mensagens: "))

    threading.Thread(target=start_udp_listener, args=(udp_port,), daemon=True).start()
    client_interface(middleware_ip, middleware_port, identifier, udp_port)
