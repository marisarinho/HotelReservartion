#pasta destinada a praticar


from time import sleep
from threading import Thread

def funcao1():
    for i in range(1,11):
        print("executando programa")
        sleep(1)

def funcao2():
    for i in range(1,11):
        print("executando programa 2 ")
        sleep(0.8)

t1 = Thread(target=funcao1)
t1.start()

t2 = Thread(target=funcao2)
t2.start()

