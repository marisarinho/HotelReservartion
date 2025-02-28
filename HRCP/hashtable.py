import threading

class HashTableReservas:
    def __init__(self):
        self.tabela = {}
        self.lock = threading.Lock()

    def inserir(self, id_quarto, nome_cliente):
        with self.lock:
            if id_quarto in self.tabela:
                return False  # Quarto já reservado
            self.tabela[id_quarto] = nome_cliente
            return True  # Reserva realizada

    def buscar(self, id_quarto):
        with self.lock:
            return self.tabela.get(id_quarto, None)

    def remover(self, id_quarto):
        with self.lock:
            if id_quarto in self.tabela:
                del self.tabela[id_quarto]
                return True
            return False
        
    def listar_todos(self):
        return self.tabela
