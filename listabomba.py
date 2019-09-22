from inicequip import *
from threading import Timer
import time

def listabomba(porta, RPM, Tempo, Sentido, Unidade, Repetir):
    ser1 = masterflex775030(porta)#verificar isso
    ser1.write("\x02P01Z\x0d".encode("ascii"))#ver se é necessário chmar configserial
    x = 0
    Revolucao = [0]*len(RPM)
    for i in range(len(RPM)):
        if Unidade[i] == "segundos":
            Tempo[i] = Tempo[i]/60
        elif Unidade[i] == "horas":
            Tempo[i] = Tempo[i]*60
        Revolucao[i] = RPM[i]*Tempo[i]
    funportempo(RPM, Tempo, Sentido, Revolucao, Repetir, x, ser1)
                      
def funportempo(RPM, Tempo, Sentido, Revolucao, Repetir, x, ser1):
    if x < len(RPM):
        if RPM[x] >= 10:
            texto = "\x02P01S{0}{1}V{2}G\x0d".format(Sentido[x], RPM[x], round(Revolucao[x],2))
            ser1.write(texto.encode("ascii"))
        else:
            ser1.write("\x02P01H\x0d".encode("ascii"))
        t = Timer(Tempo[x]*60,funportempo,(RPM, Tempo, Sentido, Revolucao, Repetir, x+1,ser1))
        t.start()
    else:
        if Repetir == True:
            x = 0
            funportempo(RPM, Tempo, Sentido, Revolucao, Repetir, x, ser1)
        else:
            ser1.write("\x02P01H\x0d".encode("ascii"))
            
