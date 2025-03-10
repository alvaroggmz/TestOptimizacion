########################################################################
##                                                                    ##
## Funciones.py                                                       ##
##                                                                    ##
## Funciones usadas por el programa principal                         ##
## la aplicación se representa como una clase.                        ##
##                                                                    ##
## Version de Python: 3.x                                             ##
##                                                                    ##
#########################################################################
 
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import serial
import io
import time
from tkinter import *
from tkinter.filedialog import *
import Conexiones


''' Muestra en una pantalla las conexiones serie'''
def ventana():
    hijastra = Toplevel()
    ## Establece el tamaño para la ventana.
    hijastra.geometry("400x325+20+50")
    hijastra.config(bg="ivory3")
    #hijastra.config(bg="snow3")
    hijastra.title("ESCANEO DE PUERTO SERIE")
    
    
    cuadro1 = LabelFrame(hijastra, text = "Puertos Serie",bg="ivory3",
                             font= "Helvetica").place(height=250, width=300,
                                                       x=50 , y=20)
    text = Label(hijastra, text="Lista de puertos series disponibles:",
                 bg="ivory3").place(x=80, y=40)
    labels = []
    label2 = []
     #-- Escanear num_port posibles puertos serie
    for i in range(8): 
        sys.stdout.flush()
        labels.append(Label(hijastra,bg="ivory3",text="COM"+str(i)+":"))
        labels[i].place(x=125, y= 65+25*i)
        
        try:
             #-- Abrir puerto serie
            s = serial.Serial(i)
            label2.append(Label(hijastra,text="Disponible"))
            label2[i].place(x=175, y= 65+25*i)
            #-- Cerrar puerto
            s.close()
       #-- Si hay un error se ignora      
        except:
            label2.append(Label(hijastra,text="NO"))
            label2[i].place(x=175, y= 65+25*i)
            
        boton = Button(hijastra,text="Volver",
                       command= lambda :hijastra.destroy())
        boton.place(height=30, width=80, x=150,y=280)

def enviar(var1):
    if var1 == 0:
        result = messagebox. showinfo("Información", message="Selecione opcion",icon='info')
    elif var1 == 1:  
        #puntos
        direccion = askopenfilename()
        file = open(direccion, "r")
        '''
        for linea in file:
            print (linea)
            #enviar linea al robot
        infor = file.read()
        texto='\rRN 1,208'\r'
        '''
        file.close()
    elif var1 == 2: 
        #programa
          #puntos
        direccion = askopenfilename()
        file = open(direccion, "r")
        '''
        for linea in file:
            print (linea)
            #enviar linea al robot
        infor = file.read()
        texto='\rRN 1,208'\r'
        '''
      
def borrar_listbox(listbox):
    listbox.delete(0,END)   
 
#activa el envio de archivos o programas tras borrar la mem del controlador   
def colocar_scrollbar(listbox,scrollbar):
    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack( fill=BOTH)    

def on_button(root):
     result = messagebox.askyesno("Confirm Exit", message="¿Estás seguro que deseas salir?",icon='warning')
     if result is True:
         root.destroy()

            
def Posicion(var1,var2,ventana,varpinza,coordenadas):
    txtrb1 = Label(ventana, text = "Establecer Posición actual como "+str(var1)+"  ").place(y=200,x=70)
    txtrb2 = Label(ventana,text="Borrar las posiciones comprendidas entre "+str(var1) +" y "+str(var2)+"  ").place (y=235,x=70)
    txtrb3 = Label(ventana, text="Mostrar las coordenadas de la Posición "+str(var1)+"  ").place (y=270,x=70)
    txtrb4 = Label(ventana, text="Intercambiar las coordenadas de las Posiciones "+str(var1)+" y "+str(var2)+"  ").place (y=305,x=70)
    txtrb5 = Label(ventana, text="Copiar las coordenadas de la Posición "+str(var1)+" en la Posición " +str(var2)+"  ").place (y=340,x=70)
    botonmov = Button (ventana, text= " Mover hasta la Posición "+str(var1)+" ",
                       command = lambda : Conexiones.pos_mov(varpinza,var1,coordenadas),
                       activebackground="Ivory4",
                       bg="Ivory3").place(height=25, width=200,x=600, y=50)
                       
                       