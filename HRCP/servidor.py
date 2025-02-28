from hashTable import HashTableReservas
import socket
from threading import Thread

# Criando os quartos disponíveis
quartos_disponiveis = {

    f"{i:03d}" for i in range(1, 4)
} | {
    f"{i}0{j}" for i in range(1, 5) for j in range(1, 4)
}

reservas = HashTableReservas()

def lidar_com_cliente(conexao, endereco):
    print(f"Cliente conectado: {endereco}")

    while True:
        try:
            mensagem = conexao.recv(1024).decode()
            if not mensagem:
                break

            comando = mensagem.split()
            resposta = "40 ERRO Comando inválido"  # Padrão de erro

            if comando[0] == "HRCP":
                if comando[1] == "CHECK":
                    id_quarto = comando[2]
                    if id_quarto in quartos_disponiveis and not reservas.buscar(id_quarto):
                        resposta = f"20 OK DISPONIVEL {id_quarto}"
                    else:
                        resposta = f"40 ERRO RESERVADO {id_quarto}"

                elif comando[1] == "RESERVE":
                    id_quarto = comando[2]
                    nome_cliente = comando[3]

                    if id_quarto in quartos_disponiveis:
                        if reservas.inserir(id_quarto, nome_cliente):
                            resposta = f"20 OK Reservation Done"
                        else:
                            resposta = f"40 ERRO Could not reserve"
                    else:
                        resposta = "40 ERRO Invalid room number"

                elif comando[1] == "CANCEL":
                    id_quarto = comando[2]

                    if reservas.remover(id_quarto):
                        resposta = f"20 OK Reservation Canceled"
                    else:
                        resposta = f"40 ERRO Reservation Not Found"

                elif comando[1] == "LIST":
                    todas_reservas = reservas.listar_todos()
                    resposta = "20 OK LISTA " + " | ".join(f"{k}: {v}" for k, v in todas_reservas.items()) if todas_reservas else "40 ERRO No Reservations Found"

            conexao.send(resposta.encode())

        except Exception as e:
            print(f"Erro: {e}")
            conexao.close()
            break

def servidor():
    host = socket.gethostname()
    porta = 10000

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, porta))
    servidor_socket.listen(5)

    print(f"Servidor rodando em {host}:{porta}")

    while True:
        conexao, endereco = servidor_socket.accept()
        thread_cliente = Thread(target=lidar_com_cliente, args=(conexao, endereco))
        thread_cliente.start()

if __name__ == '__main__':
    servidor()
