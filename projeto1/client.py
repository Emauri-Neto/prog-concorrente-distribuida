import socket
import time

class Client:
    def __init__(self, host='localhost', port=4444):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.socket.connect((self.host, self.port))
                break
            except ConnectionRefusedError:
                print("Conexão recusada. Tentando novamente em 1 segundo...")
                retry_count += 1
                time.sleep(1)
        
        print(f"conectado ao servidor {self.host}:{self.port}")
        while True:
            cmd = input("Digite o comando que deseja realizar: \n 1. Entrar \n 2. Sair \n 3. Fechar conexao \n").strip().lower()

            if not cmd:
                continue

            self.socket.send(cmd.encode())

            if cmd == "quit" or cmd == "3":
                res = self.socket.recv(1024).decode()
                print(f"Resposta do servidor: {res}")
                break

            res = self.socket.recv(1024).decode()
            print(f"Resposta do servidor: {res}")


if __name__ == '__main__':
    client = Client()
    client.run()