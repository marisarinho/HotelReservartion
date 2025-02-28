from listaEnc import Lista
import socket

def cliente():
    host = socket.gethostname()
    porta = 10000
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, porta))

    lista_reservas = Lista()

    while True:
        print("\nOpções:")
        print("""
                CHECK <numeroDoQuarto>
                RESERVE <numeroDoQuarto> <nome>
                CANCEL <numeroDoQuarto>
                LIST
                QUIT
        """)
        opcao = input("> ").strip().upper()
        comandos = opcao.split()

        if not comandos:
            print("Comando inválido. Tente novamente.")
            continue

        cliente_socket.send(f"HRCP {opcao}".encode())
        resposta = cliente_socket.recv(1024).decode()
        print(f"[Servidor]: {resposta}")

        if comandos[0] == "RESERVE" and resposta.startswith("20 OK"):
            lista_reservas.append(comandos[1])  # Adiciona o quarto na lista local

        elif comandos[0] == "CANCEL" and resposta.startswith("20 OK"):
            lista_reservas.remover(comandos[1])  # Remove o quarto da lista local

        elif comandos[0] == "QUIT":
            cliente_socket.close()
            break

if __name__ == '__main__':
    cliente()
