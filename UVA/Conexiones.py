########################################################################
##                                                                    ##
## Conexiones.py                                                      ##
##                                                                    ##
## funciones usadas por el programa principal para                    ##
##  conectarnos al robot                                              ##
##                                                                    ##
## Version de Python: 3.x                                             ##
##                                                                    ##
########################################################################
 
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import serial
import io
import time
from tkinter import *
from tkinter.filedialog import *
import Grafico
import Funciones





#Funcion que inicia la conexion
def iniciar_comunicacion():
    try:
        ser=serial.Serial(
                      port = 0, #port = "COM1"
                      baudrate = 4800,
                      bytesize = serial.SEVENBITS,
                      parity = serial.PARITY_EVEN,
                      stopbits = serial.STOPBITS_ONE,
                      rtscts=True, 
                      dsrdtr=True,
                      #timeout=1
                      )
        if ser.isOpen():
            ser.flushInput() ## vacia bufer entrada
            ser.flushOutput()##vacia bufer salida
        return ser
    except serial.SerialException:
        result = messagebox.showerror("Error al establecer conexión:", 
                                      message="-Compruebe que el robot está correctamente conectado al puerto\n"+
                                      "-Compruebe que el robot está encendido\n"+
                                      "-Compruebe que el interruptor del teaching box ON/OFF está en OFF\n"+
                                      "-Compruebe que  los interruptores ST1 Y ST2 están en su posición inferior ")
        return 0
        print ("error al abrir puerto serie: ")
        #Mensaje que nos indique error  
        
def finalizar_comunicacion(ser,ventana):
    time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
    while True : 
            ## CUANDO CAMBIE LA CONDICION  A VERDADERO SALE DEL BOUCLE
            estado=ser.getCTS()
            if estado == True : ##o false
                break;    
            
    #Compruebo si hay error:
    ser.write(b'\rER\r')  
    time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
    while True : 
            ## CUANDO CAMBIE LA CONDICION  A VERDADERO SALE DEL BOUCLE
            estado=ser.getCTS()
            if estado == True : ##o false
                break; 
    error = ser.read(ser.inWaiting())
    errortipo = error.decode("utf-8")
    errorcom = int(errortipo)
    if errorcom == 0:#significa que no hay error y procedo
        print ("No error")
        ser.write(b'\rWH\r') #pido coordenadas
        time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
        while True : 
            ## CUANDO CAMBIE LA CONDICION  A VERDADERO SALE DEL BOUCLE
            estado=ser.getCTS()
            if estado == True : ##o false
                break;   
    #obtenemos coordenadas#
        recibi = ser.read(ser.inWaiting())
        recibir = recibi.decode("utf-8")
        dato=recibir.split(',')
        coordenadas(dato,ventana)#llamo a la funcion para escribir las coordenadas en el programa
    if errorcom == 1:
        print("Error tipo 1")
        result = messagebox.showerror("Error tipo 1:", 
                                      message="-Error de Hardware")
    if errorcom == 2:
        print("Error tipo 2")
        result = messagebox.showerror("Error tipo 2:", 
                                      message="-Error de software:\n"
                                      +"Al pulsar aceptar se reseteará automáticamente")
        ser.write(b'\rRS\r')
        finalizar_comunicacion_simple(ser)
    if ser.isOpen():
        ser.close() 
      
def finalizar_comunicacion_simple(ser): 
    time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
    while True : 
        estado=ser.getCTS()
        if estado == True : #Cuando llega a la posicion, sale del boucle
            break;    
    if ser.isOpen():
        ser.close() 
            
#funcion que introduce las coordenadas
def coordenadas(dato,ventana):

    text1 = Label(ventana, text=dato[0], background="White").place(height=20, 
                                                                         width=50, x=160, y=648)
    text2 = Label(ventana, text=dato[1], background="White").place(height=20, 
                                                                         width=50,x=315, y=648)
    text3 = Label(ventana, text=dato[2], background="White").place(height=20, 
                                                                         width=50,x=475, y=648)
    text4 = Label(ventana, text=dato[3], background="White").place(height=20, 
                                                                         width=50,x=655, y=648)
    text5 = Label(ventana, text=dato[4], background="White").place(x=820, y=648)
    
def conex_com1():
#funcion COM1 que establece la conexion:
    result = messagebox. showinfo("Información", message="Asegurese de que no existe peligro de choque",icon='warning')
    espera=Toplevel()
    
    conexion = iniciar_comunicacion()
    if conexion != 0:
    #app=Grafico.VentanaHija() #no estoy muy seguro de esto
        conexion.write(b'\rNT\r')
        finalizar_comunicacion_simple(conexion)
        espera.withdraw()
        Grafico.VentanaHija()
        print("Fin")
   
#punto home
def home(pantalla):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        conexion.write(b'\rNT\r')
        finalizar_comunicacion(conexion,pantalla)
       
  
#origen coordenadas
def origen_coord(pantalla):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        conexion.write(b'\rOG\r')
        finalizar_comunicacion(conexion,pantalla)
#resetea el robot
def reset():
    conexion = iniciar_comunicacion()
    if conexion != 0:
        conexion.write(b'\rRS\r')
        finalizar_comunicacion_simple(conexion)
    
#sale del programa
def salir(ventana):
    result = messagebox.askyesno("Confirm Exit", message="¿Estás seguro que deseas salir?",icon='warning')
    if result is True:
        ventana.destroy()
    
def b_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ ' + str(avance) + ', 0, 0, 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def b_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ -' + str(avance) + ', 0, 0, 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def s_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, +' + str(avance) + ', 0, 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def s_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, -' + str(avance) + ', 0, 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)

def e_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, 0, +' + str(avance) + ', 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def e_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, 0, -' + str(avance) + ', 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def p_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, 0, 0, +' + str(avance) + ', 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def p_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, 0, 0, -' + str(avance) + ', 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def r_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, 0, 0, 0, +' + str(avance) + '\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def r_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ 0, 0, 0, 0, -' + str(avance) + '\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def pos_rel(pantalla,var1,var2,var3,var4,var5):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rMJ '+str(var1)+', '+str(var2)+', '+str(var3)+', '+str(var4)+', '+str(var5) + '\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def x_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rDW ' +str(avance) +', 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def x_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rDW -' +str(avance) +', 0, 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def y_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rDW  0,' +str(avance)+', 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)

def y_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rDW  0 -,' +str(avance)+', 0\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)

def z_mas(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rDW  0 , 0,' +str(avance)+'\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)

def z_menos(pantalla,avance):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto='\rDW  0 , 0, -' +str(avance)+'\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
        
def velocidad(vardesplz,radiobutton):
    if radiobutton ==0:
        result = messagebox. showinfo("Información", message="Debe selecionar una velocidad",icon='info')
    elif radiobutton == 1:
        #Rapido
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto='\rSP '+str(vardesplz)+', H\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion_simple(conexion)
    elif radiobutton == 2:
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto='\rSP '+str(vardesplz)+', L\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion_simple(conexion)      

def abrir_pinza(pantalla,var1,var2,var3):
    result = establecer_fuerza(var1,var2,var3)
    if result ==1:
        conexion = iniciar_comunicacion()
        conexion.write(b'\rGO\r')
        finalizar_comunicacion(conexion,pantalla)
    
    
def cerrar_pinza(pantalla,var1,var2,var3):
    result = establecer_fuerza(var1,var2,var3)
    if result ==1:
        conexion = iniciar_comunicacion()
        conexion.write(b'\rGC\r')
        finalizar_comunicacion(conexion,pantalla)

def establecer_fuerza(var1,var2,var3):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        
        texto='\rGP' +str(var1)+', ' +str(var2)+', ' +str(var3)+'\r'
        conexion.write(str.encode(texto)) 
        finalizar_comunicacion_simple(conexion)
        return 1
    else:
        return 0

def ejecutar_accion(pantalla,radiobutton,posa,posb):
    if radiobutton ==0:
        result = messagebox.showinfo("Información", message="Debe selecionar una opción",icon='info')
    elif radiobutton == 1:
        #establecer posicion
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto='\rHE ' +str(posa)+'\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion_simple(conexion)  
    elif radiobutton == 2:
        #borrar posiciones
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto='\rPC ' +str(posa)+', '+str(posb)+'\r'
            conexion.write(str.encode(texto))
    elif radiobutton ==3:
        #mostrar coordenadas
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto = '\rPR '+str(posa)+'\r'
            conexion.write(str.encode(texto))
            time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
            while True : 
                estado=conexion.getCTS()
                if estado == True : ##Cuando llega a la posicion, sale del boucle    
                    break; 
            recibi = conexion.read(conexion.inWaiting())
            print(recibi)
            recibir = recibi.decode("utf-8")
            dato=recibir.split(',')
            print(recibir)
            print(dato)
            coordenadas(dato,pantalla) 
            if conexion.isOpen():
                conexion.close() 
    elif radiobutton == 4:
        #intercambiar coordenadas
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto = '\rPX '+str(posa)+', '+str(posb)+'\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion_simple(conexion)
    elif radiobutton == 5:
        #copiar coordenadas
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto = '\rPL '+str(posa)+', '+str(posb)+'\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion_simple(conexion)
        
def pos_mov(var1,posa,pantalla):
    if var1 ==0:
        result = messagebox. showinfo("Información", message="Selecione posicion pinza",icon='info')
    elif var1 == 1:
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto = '\rMO  '+str(posa)+','+'O\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion(conexion,pantalla)
    elif var1 == 2:
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto = '\rMO  '+str(posa)+','+'C\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion(conexion,pantalla)
        
def pos_sigui(posa,pantalla):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto = '\rIP\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
        
def pos_ant(posa,pantalla):
    conexion = iniciar_comunicacion()
    if conexion != 0:
        texto = '\rDP\r'
        conexion.write(str.encode(texto))
        finalizar_comunicacion(conexion,pantalla)
    
def borrar_mem(pantalla,listbox):
    result = messagebox.askyesno("Confirmar Borrar Memoria",
                                  message="¿Estás seguro que deseas borrar la memoria del Controlador?",
                                  icon='warning')
    if result is True:
        conexion = iniciar_comunicacion()
        if conexion != 0:
            texto = '\rNW\r'
            conexion.write(str.encode(texto))
            finalizar_comunicacion(conexion,pantalla)
            varenv = IntVar()
            botonenv = Button (pantalla, text= "Enviar",
                               bg="Ivory3",activebackground="Ivory4",
                               command = lambda : enviar(0,listbox)).place(height=35, width=80,x=50, y=475)   
            rbenv = Radiobutton(pantalla, text= "Enviar puntos al robot",
                                    command = lambda: act_varrec(varenv.get(),pantalla,listbox),
                                    value=1,variable = varenv).place(x=140, y=480)
            rbenv2 = Radiobutton(pantalla, text= "Enviar programa al robot" ,
                                     command = lambda: act_varrec(varenv.get(),pantalla,listbox),
                                     value=2, variable = varenv).place(x=300, y=480)
                           
def act_varrec(var,pantalla,listbox):
    botonenv = Button (pantalla, text= "Enviar",
                           bg="Ivory3",activebackground="Ivory4",
                           command = lambda : enviar(var,listbox)).place(height=35, width=80,x=50, y=475)  
    print("hecho")
    print(var)
                           
def recibir(var1,listbox):
    if var1 == 0:
        result = messagebox. showinfo("Información", message="Selecione opcion",icon='info')
        
    if var1 == 1:
         #puntos
        direccion = askopenfilename(filetypes=(("Archivos de puntos CRD",".crd"),
                                                ("All files", "*.*")))
        
        a=1
        text= ""
        for i in range(10):
            ser = iniciar_comunicacion() 
            if ser != 0:
                texto='\rPR  '+str(a)+'\r'
                ser.write(str.encode(texto))
                time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
                while True : 
                    ## CUANDO CAMBIE LA CONDICION  A VERDADERO SALE DEL BOUCLE
                    estado=ser.getCTS()
                    if estado == True : ##o false
                        break;   
                recibi = ser.read(ser.inWaiting())
                recibir = recibi.decode("utf-8")
                
                if recibir[0]== "0" and recibir[2]== "0" and recibir[4]== "0"  and recibir[6]== "0"  and recibir[8]== "0":
                    linea = " "
                else: 
                    linea = "PD "+str(a)+", "+ recibir;
                    listbox.insert(END, linea)
                    text += linea + '\n'
                if ser.isOpen():
                    ser.close() 
                a=a+1#fin for
        print(text)
        file=open(direccion, "w")
            #recibir del robot en una variable y la escribimos dentro de un archivo
        file.write(text)
            #para cerrar el archivo
        file.close() 
    if var1 == 2:
        print("Recibir programa")
        direccion = askopenfilename(filetypes=(("Archivos de programas",".pgm"),
                                                ("All files", "*.*")))
        a=1
        text= ""
        for i in range(10):
            ser = iniciar_comunicacion() 
            if ser != 0:
                texto='\rLR  '+str(a)+'\r'
                ser.write(str.encode(texto))
                time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
                while True : 
                    ## CUANDO CAMBIE LA CONDICION  A VERDADERO SALE DEL BOUCLE
                    estado=ser.getCTS()
                    if estado == True : ##o false
                        break;   
                recibi = ser.read(ser.inWaiting())
                recibir = recibi.decode("utf-8")
                if recibir[0]== "0" and recibir[2]== "0" and recibir[4]== "0"  and recibir[6]== "0"  and recibir[8]== "0":
                    linea = " "
                else: 
                    linea = str(a)+" "+ recibir;
                    text += linea + '\n'
                if ser.isOpen():
                    ser.close() 
                a=a+1#fin for
        print(text)
        
        file=open(direccion, "w")
            #recibir del robot en una variable y la escribimos dentro de un archivo
        file.write(text)
            #para cerrar el archivo
        file.close() 
'''   
def enviar(var1,lista):
    if var1 == 0:
        result = messagebox. showinfo("Información", message="Selecione opcion",icon='info')
    if var1 == 1:  
        #puntos
        print("enviar1")
        direccion = askopenfilename()
        file = open(direccion, "r")
        
        for linea in file:
            print (linea)
            lista.insert(END, linea)
            #enviar linea al robot
        infor = file.read()
        print("FIN, NUEVAL LINEA \n")
        print(infor)
        #texto='\rRN 1,208'\r'
    
        file.close()
    if var1 == 2: 
        #programa
          #puntos
        print("enviar1")
        direccion = askopenfilename()
        file = open(direccion, "r")
        
        for linea in file:
            print (linea)
            #enviar linea al robot
        infor = file.read()
        texto='\rRN 1,208'\r'
        '''
      
    
 

def Posicion():
    print("Funcion posición")
    try:
        ser=serial.Serial(
                      port = 0, #port = "COM1"
                      baudrate = 4800,
                      bytesize = serial.SEVENBITS,
                      parity = serial.PARITY_EVEN,
                      stopbits = serial.STOPBITS_ONE,
                      rtscts=True, 
                      dsrdtr=True,
                      #timeout=1
                      )
        
        
        if ser.isOpen():
            ser.flushInput() ## vacia bufer entrada
            ser.flushOutput()##vacia bufer salida
        print (ser.name)
        print("CTS inicial=",ser.getCTS())
        print("DSR inicial=",ser.getDSR())
       
        #CTS NOS INDICA SI ESTÁ LIBRE PARA ENVIAR
       # ser.setRTS(True) #listo para enviar no hace falta
        #enviar informacion
        ser.write(b'\rWH\r')
        time.sleep(0.1) ##doi un tiempo a que se estabilice CTS
        while True : 
            ## CUANDO CAMBIE LA CONDICION  A VERDADERO SALE DEL BOUCLE
            estado=ser.getCTS()
            if estado == True : ##o false
                break;
     
        recibi = ser.read(ser.inWaiting())
        recibir = recibi.decode("utf-8")
        dato=recibir.split(',')
        print(dato)
            
    except serial.SerialException:
        print ("error al abrir puerto serie: ")
