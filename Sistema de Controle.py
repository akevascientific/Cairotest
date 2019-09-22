'''
Higor Barreto Campos
'''

import time
import serial
import platform
from tkinter import *
from tkinter.ttk import *
from functools import partial
from inicequip import *
from listabomba import *

contador = 0
Sentido = []
RPM = []
Tempo = []
Unidade = []
checkvar1 = 0
portabomba = ""
a = []
repetir = False

#Funções

def donothing(): #apagar essa função
   pass
def cmdrepetir():
   global repetir
   repetir = not(repetir)
def equserial(cbequ, enequ): #ver se é necessáro
   global portabomba
   ser = [0]*4
   for i in range(4):
      ser[i] = seletorequip(cbequ[i].get(), enequ[i].get())
   portabomba = enequ[1].get()
def menuequ():
   janelaequ = Toplevel(janela)
   janelaequ.geometry("400x150")
   lbequ1 = Label(janelaequ, text = "Equipamento:")
   lbequ1.grid (row = 0,column = 0)
   lbequ2 = Label(janelaequ, text = "Modelo:")
   lbequ2.grid(row = 0, column = 1)
   lbequ3 = Label(janelaequ, text = "Porta:")
   lbequ3.grid (row = 0, column = 2)
   lbequ4 = Label(janelaequ, text = "PHmetro")
   lbequ4.grid(row = 1)
   lbequ5 = Label(janelaequ, text = "Bomba Peristáltica")
   lbequ5.grid (row = 2)
   lbequ6 = Label(janelaequ, text = "Bomba Infusora 1")
   lbequ6.grid(row = 3)
   lbequ7 = Label(janelaequ, text = "Bomba Infusora 2")
   lbequ7.grid (row = 4)
   cbequ = [0]*4
   enequ = [0]*4
   cbequ[0] = Combobox(janelaequ, width = 20, values = ("Hanna\ Hi\ 221"), state = "readonly")
   cbequ[0].grid(row = 1, column = 1)
   cbequ[1] = Combobox(janelaequ, width = 20, values = ("MasterFlex\ 7550-30"), state = "readonly")
   cbequ[1].grid(row = 2, column = 1)
   cbequ[2] = Combobox(janelaequ, width = 20, values = (), state = "readonly")
   cbequ[2].grid(row = 3, column = 1)
   cbequ[3] = Combobox(janelaequ, width = 20, values = (), state = "readonly")
   cbequ[3].grid(row = 4, column = 1)
   sistema = platform.system()
   if sistema == "Windows":
       port='COM'
   else:
       port='/dev/ttyUSB'
   enequ[0] = Entry(janelaequ, width = 15)
   enequ[0].insert(0,port)
   enequ[0].grid(row = 1, column = 2)
   enequ[1] = Entry(janelaequ, width = 15)
   enequ[1].insert(0,port)
   enequ[1].grid(row = 2, column = 2)
   enequ[2] = Entry(janelaequ, width = 15)
   enequ[2].insert(0,port)
   enequ[2].grid(row = 3, column = 2)
   enequ[3] = Entry (janelaequ, width = 15)
   enequ[3].insert(0,port)
   enequ[3].grid (row = 4, column = 2)
   btequ1 = Button(janelaequ, text = "Configurar", width = 15)
   btequ1["command"] = partial(equserial, cbequ, enequ)
   btequ1.grid (row = 5, column = 1)
   #chegar se a porta é COM#, /dev/ttyUSB# ou /dev/ttyS#
def enclista(cbenc1, spenc1, enenc1, cbenc2):
   global contador
   Sentido.append(cbenc1.get())
   RPM.append(int(spenc1.get()))
   Tempo.append(float(enenc1.get()))
   Unidade.append(cbenc2.get())
   frenc1 = Frame(janelaenc)
   frenc1.grid(row = 3, column = 0, columnspan = 7)
   scrollbar = Scrollbar(frenc1)
   scrollbar.pack( side = RIGHT, fill=Y )
   mylist = Listbox(frenc1, yscrollcommand = scrollbar.set)
   a.append("{0}{1} RPM por {2} {3}".format(Sentido[contador],RPM[contador], Tempo[contador], Unidade[contador]))
   for i in a:
      mylist.insert(END, i) # verificar isso, parei aqui <<<<<<<<<
   mylist.pack( side = LEFT, fill = BOTH )
   scrollbar.config( command = mylist.yview() )
   contador += 1
   #Fazer gráfico
def menuenc():
   global janelaenc
   janelaenc = Toplevel(janela)
   janelaenc.geometry("450x400")
   menubarenc = Menu(janelaenc)
   configenc = Menu(janelaenc, tearoff=0)
   configenc.add_command(label = "Salvar", command = donothing) #add comando
   configenc.add_command(label = "Salvar como...", command = donothing) #add comando
   configenc.add_command(label = "Abrir", command = donothing) #add comando
   menubarenc.add_cascade(label = "Opções", menu = configenc)
   janelaenc.config(menu = menubarenc)
   lbenc1 = Label(janelaenc, text = "Sentido:")
   lbenc1.grid(row = 0,column = 0)
   lbenc2 = Label(janelaenc, text = "RPM*:")
   lbenc2.grid(row = 0,column = 2)
   lbenc3 = Label(janelaenc, text = "Tempo**:")
   lbenc3.grid(row = 0,column = 4)
   lbenc4 = Label(janelaenc, text = "*RPM<10 será considerado como pausa")
   lbenc4.grid(row = 1,column = 0, columnspan = 6, sticky = "W")
   lbenc4 = Label(janelaenc, text = "**Valor mínimo de 0.05s")
   lbenc4.grid(row = 2,column = 0, columnspan = 6, sticky = "W")
   cbenc1 = Combobox(janelaenc, width = 2, values = ("+", "-"), state = "readonly") #CC and ACC
   cbenc1.current(0)
   cbenc1.grid(row = 0, column = 1)
   spenc1 = Spinbox(janelaenc, width = 4, from_ = 0, to = 600) #validar
   spenc1.grid(row = 0, column = 3)
   enenc1 = Entry(janelaenc, width = 7)
   enenc1.insert(0,0.0)
   enenc1.grid(row = 0, column = 5)
   cbenc2 = Combobox(janelaenc, width = 9, values = ("segundos", "minutos", "horas"), state = "readonly")
   cbenc2.current(0)
   cbenc2.grid(row = 0, column = 6)
   btenc1 = Button(janelaenc, text = "Listar", width = 8)
   btenc1["command"] = partial(enclista, cbenc1, spenc1,enenc1, cbenc2)
   btenc1.grid (row = 0, column = 7)
   chenc1 = Checkbutton(janelaenc, text = "Repetir", variable = checkvar1, command = cmdrepetir, width = 10)
   chenc1.grid (row = 4, column = 7)
   btenc1 = Button(janelaenc, text = "Inciar", width = 8)
   print (repetir) # repetir sempre aparece false, só atualiza se abre ou fecha a janela, arrumar essa parte aqui <<<
   btenc1["command"] = partial(listabomba, portabomba, RPM, Tempo, Sentido, Unidade, repetir) #mudar
   btenc1.grid (row = 5, column = 3)
        
#Janela Principal
janela = Tk()
janela.title("Eva Scientific")
janela.geometry("500x750")
janela.style = Style()
janela.style.theme_use('vista')

#Menu
menubar = Menu(janela)
configmenu = Menu(menubar, tearoff=0)
configmenu.add_command(label = "Equipamentos", command = menuequ)
configmenu.add_command(label = "Enviar Comandos", command = menuenc)
configmenu.add_command(label = "Manual", command = donothing)
menubar.add_cascade(label = "Configurações", menu = configmenu)
janela.config(menu = menubar)

janela.mainloop()
