"""
Mudança realizada em 10/07:
Coloquei a numeração da bomba somente quando o serial não estiver aberto,
para que se chamar a função outra vez, ela não refaça isso.
"""
from configserial import *
import time

def seletorequip(maquina, porta):
    if maquina == "MasterFlex 7550-30":
        masterflex775030(porta)

def masterflex775030(porta):
    ser1 = configserial(porta,4800,7,"Odd",1)
    if ser1.is_open == False:
        ser1.open()
        ser1.write("\x05".encode("ascii"))
        time.sleep(1)
        ser1.write("\x02P01\x0d".encode("ascii"))
    return ser1

#def adicionar mais equipamentos aqui
