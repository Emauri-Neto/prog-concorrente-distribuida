import socket
import threading

# Meu teclado eh padrao americano, entao todas as frases estao sem acento. :( 

class Server:
    def __init__(self, host='localhost', port=4444, capacity=5):
        self.host = host
        self.port = port
        self.capacity = capacity

        self.semaphore = threading.Semaphore(capacity)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        print(f"Server running on {self.host}:{self.port}")

    def client_handler(self, client, addr):
        print(f"Cliente conectado: {addr}")

        inside = False

        try:
            while True:
                data = client.recv(1024).decode().strip().lower()
                if not data:
                    break
                print(f"Recebido do {addr}: {data}")

                command = data
                if data.isdigit():
                    if data == "1":
                        command = "entrar"
                    elif data == "2":
                        command = "sair"
                    elif data == "3":
                        command = "quit"

                if command == "entrar":
                    if inside:
                        response = "Voce ja esta na sala."
                        print(f"{addr}: tentativa de entrar ja estando dentro.")
                    else:
                        if self.semaphore.acquire(blocking=False):
                            inside = True
                            response = "Entrada autorizada. Bem-vindo a sala!"
                            print(f"{addr} entrou na sala. Vagas restantes: {self.semaphore._value}")
                        else:
                            response = "Sala cheia. Tente novamente mais tarde."
                            print(f"{addr}: tentativa de entrar falhou - sala cheia.")

                elif command == "sair":
                    if inside:
                        self.semaphore.release()
                        inside = False
                        response = "Voce saiu da sala. Ate logo!"
                        print(f"{addr} saiu da sala. Vagas disponiveis: {self.semaphore._value}")
                    else:
                        response = "Voce nao esta na sala."
                        print(f"{addr}: tentou sair mas nao estava na sala.")

                elif command == "quit":
                    response = "Desconectando..."
                    client.send(response.encode())
                    print(f"{addr} desconectado.")
                    break

                else:
                    response = "Comando invalido. Use 'entrar' (1), 'sair' (2) ou 'quit' (3)."
                    print(f"{addr}: comando invalido: {command}")

                client.send(response.encode())

        except Exception as e:
            print(f"Erro inesperado com o cliente {addr}: {e}")

        finally:
            client.close()

            if inside:
                self.semaphore.release()
                print(f"Desconectando cliente {addr}. Vagas liberadas: {self.semaphore._value}")

    def run(self):
        print("Servidor aguardando conexoes...")
        while True:
            client, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.client_handler, args=(client, addr))
            client_thread.daemon = True
            client_thread.start()

if __name__ == '__main__':
    server = Server()
    server.run()
