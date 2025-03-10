########################################################################
##                                                                     ##
## Programa VENTANA PRINCIPAL                                          ##
##                                                                     ##
## Este programa sigue el patrón de mejores prácticas ya que           ##
## la aplicación se representa como una clase.                         ##
##                                                                     ##
## Version de Python: 3.x                                              ##
##                                                                     ##
#########################################################################
 
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import serial
import io
import time

import Funciones  #importa donde tenemos todas las funciones gráficas
import Conexiones #importa archivo donde tenemos las funciones de conexión con el robot


def espera():
    progreso= Toplevel()
    progreso.title("Espera...")
    progreso.geometry("200x25+475+300")
    progreso.grab_set()
    progreso.transient()
    progreso.resizable(0,0)
    progreso.protocol("WM_DELETE_WINDOW", "onexit")

    pb = ttk.Progressbar(progreso, orient='horizontal', mode='indeterminate')
    pb.start(40)
    pb.pack(fill='x')
    

   
class Mi_Aplicacion(Frame):
    '''clase que inicia la conexion con el robot: Esta clase nos permite representar la ventana principal del programa. ''' 
    def __init__(self, master=None):
    
        ##Asigno tamaño y título a la ventana principal
        self.peq = master
        self.peq.geometry("50x50+500+350")
        self.peq.withdraw()
        ##Asigno tamaño y título a la ventana menu
        self.root = Toplevel()
        self.root.title("Robot Mitsubisi")
        self.root.geometry("650x700+200+0")
        self.root.config(bg="snow3")
        #self.root.protocol("WM_DELETE_WINDOW", "onexit")
        ## Invoca al constructor del master
        Frame.__init__(self, self.root)  
        self.crea_widgets()

    def crea_widgets(self):
        """Crea los widgets en el frame correspondiente al objeto"""
           
        titulo = Label(self.root,bg="snow3",font= "Helvetica",
                       text="BIENVENIDO: \nPrograma de Control Remoto del robot"
                        "Mitsubishi MOveMaster EX RV-M1 ")
        titulo.pack(ipady=10)
        marco = Frame(self.root, bd=5, relief="groove", highlightcolor="yellow")
        marco.pack()
        self.fondo = PhotoImage(file="movemaster.gif")
        imagen = Label (marco,image=self.fondo).pack()
        
        titulo3 = Label(self.root,font= "Helvetica", 
                      text= " Ver conexiones disponibles:",bg="snow3")
        titulo3.pack(ipady=5)
        boton1 = Button (self.root,bg="khaki",text="Ver",command = Funciones.ventana)
        boton1.pack(ipadx=20,ipady=5)
        titulo2 = Label(self.root, bg="snow3", font= "Helvetica",
                        text='Elija un puerto de conexión:').pack()
        var = IntVar()
        r1 = Radiobutton(self.root, bg="snow3", text="COM0",
                         indicatoron=0,activebackground="snow3",
                         variable=var, value=1, command=Conexiones.conex_com1 ).pack()
        r2 = Radiobutton(self.root,bg="snow3", text="COM1", 
                         state="disabled",
                        indicatoron=0,
                         activebackground="snow3",
                         variable=var, value=2).pack()
        r3 = Radiobutton(self.root,bg="snow3", text="COM2",
                        indicatoron=0,
                         activebackground="snow3",
                         state="disabled",
                         variable=var, value=3).pack()
        r4 = Radiobutton(self.root,bg="snow3", text="COM3",
                         indicatoron=0,
                         state="disabled",
                         activebackground="snow3",
                         variable=var, value=4).pack()
     
        titulo4 = Label(self.root,font= "Helvetica", 
                      text= " Salir del programa:",bg="snow3")
        titulo4.pack(ipady=5)
        boton2 = Button(self.root,text="salir",bg="tomato2",
                        command = lambda: Funciones.on_button(root))
        boton2.pack(ipadx=10, ipady=3)
        
        espacio = Label(self.root, bg="snow3", ).pack()
        autor = Label(self.root, bg="snow3", font= "Helvetica", 
                     text='Autor: Rubén Poncelas Bodelón').pack()
                     
                     
class VentanaHija():
    
    def __init__(self):
        #Creamos la ventana hija,establecemos el tamaño sin dejar de modificarlo
        #tomamos el foco y deshabilitamos el resto de ventanas 
        self.hija = Toplevel()
        self.hija.geometry('1024x725+0+0')
        self.hija.title("Software")
        #self.hija.grab_set()
        #self.hija.transient()
        self.hija.resizable(0,0) 
        #Añadimos pestañas
        self.notebook = ttk.Notebook(self.hija)
        self.notebook.pack(fill="both", expand='yes')
        self.frame1 = ttk.Frame(self.notebook,height=600, width=1024)
        self.frame2 = ttk.Frame (self.notebook,height=600, width=1024)
        self.notebook.add(self.frame1,text='CONTROL DEL ROBOT')
        self.notebook.add(self.frame2, text='POSICIONES Y PROGRAMAS')
        #Texto y Cuadros de Coordenadas de posición
        self.marco = LabelFrame(self.hija, text="Coordenadas actuales:",
                                font= "Helvetica",padx=0,pady=0)

        self.marco.place(height=95, width=1024, x=5, y=600)  
        self.text1 = Label(self.hija, text= "Eje X :").place(x=100, y=645)  
        self.text2 = Label(self.hija, text= "Eje Y :").place(x=250, y=645)  
        self.text3 = Label(self.hija, text= "Eje Z :").place(x=410, y=645)  
        self.text4 = Label(self.hija, text= "Incl. Pinza :").place(x=570, y=645)
        self.text5 = Label(self.hija, text= "Giro Pinza :").place(x=740, y=645)   
        
        self.marcot1 = Frame(self.hija, bd=1, relief="groove", background="White")
        self.marcot2 = Frame(self.hija, bd=1, relief="groove", background="White")
        self.marcot3 = Frame(self.hija, bd=1, relief="groove", background="White")
        self.marcot4 = Frame(self.hija, bd=1, relief="groove", background="White")
        self.marcot5 = Frame(self.hija, bd=1, relief="groove", background="White")
        self.marcot1.place(height=25, width=70, x=150, y=645) 
        self.marcot2.place(height=25, width=70, x=300, y=645) 
        self.marcot3.place(height=25, width=70, x=460, y=645)
        self.marcot4.place( height=25, width=70,x=645, y=645)
        self.marcot5.place(height=25, width=70, x=815, y=645) 
        #Botones Inicio,Reset, Home, Salir
        binicio = Button(self.hija,text="HOME",activebackground="Ivory4",
                         command = lambda: Conexiones.home(self.hija),
                         bg="Ivory3").place(height=90, width=90,x=920, y=100)
        
        bhome = Button(self.hija, text="Origen", activebackground="Ivory4",
                       command = lambda: Conexiones.origen_coord(self.hija),
                       bg="Ivory3").place(height=90, width=90, x=920, y=225)
        breset = Button(self.hija, text="RESET", activebackground="Ivory4",
                        command = Conexiones.reset,
                        bg="Ivory3").place(height=90, width=90,x=920, y=350)
        bsalir = Button(self.hija, text="SALIR", activebackground="tomato3",
                        command = lambda: Conexiones.salir(self.hija),
                        bg="tomato2").place(height=90, width=90,x=920, y=475)
                        
        dato = ["+51","-88.3","+737.1","+10.9","+179.9"]                
        text1 = Label(self.hija, text=dato[0], background="White").place(height=20, 
                                                                         width=50, x=160, y=648)
        text2 = Label(self.hija, text=dato[1], background="White").place(height=20, 
                                                                         width=50,x=315, y=648)
        text3 = Label(self.hija, text=dato[2], background="White").place(height=20, 
                                                                         width=50,x=475, y=648)
        text4 = Label(self.hija, text=dato[3], background="White").place(height=20, 
                                                                         width=50,x=655, y=648)
        text5 = Label(self.hija, text=dato[4], background="White").place(height=20, 
                                                                         width=50,x=820, y=648)
     #funciones para crear las pestañas
        self.pestana2(self.frame2,self.hija)
        self.pestana1(self.frame1,self.hija)
        
    def pestana1(self,pestania,coordenadas):
        '''funcion que crea los elementos de la pestaña1'''
        #Creo los cuadros gráficos
        cuadro1 = LabelFrame(pestania, text = "Movimiento Articulaciones",
                             font= "Helvetica").place(height=280, width=275,
                                                       x=5 , y=10)  
        cuadro2 = LabelFrame(pestania, text="Movimiento Cartesiano",
                             font= "Helvetica",).place(height=200, width=275, 
                                                       x=5, y=290)
        cuadro3 = LabelFrame(pestania).place(height=75, width=275, x=5, y=500) 
        cuadro4 = LabelFrame(pestania, text="Movimiento relativo", 
                             font= "Helvetica").place(height=85, width=630,
                                                       x=285, y=490)  
        cuadro5 = LabelFrame(pestania, text="Movimientos de la pinza", 
                             font= "Helvetica").place(height=200, width=300,
                                                       x=615, y=290)  
        cuadro6 = LabelFrame(pestania, text="Velocidad Robot", 
                             font= "Helvetica").place(height=280, width=300,
                                                       x=615 , y=10)
        #cuadro1  Movimiento Articulaciones:Inserto elementos en este cuadro
        bbmas = Button(pestania, text="B+", bg="Ivory3",
                       command = lambda: Conexiones.b_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                        height=40, width=40,
                                                         y=40 ,x=20)
        bbmenos = Button(pestania, text="B-", bg="Ivory3",
                         command = lambda: Conexiones.b_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40,
                                                           y=40, x=70)
        labelb = Label(pestania,
                       text="Movimiento de la Cintura").place(bordermode=OUTSIDE,
                                                              height=30, width=160,
                                                               y=40, x=110) 
        bsmas = Button(pestania, text="S+", bg="Ivory3",
                       command = lambda: Conexiones.s_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                        height=40, width=40, 
                                                        y=90 , x=20)
        bsmenos = Button(pestania, text="S-", bg="Ivory3",
                         command = lambda: Conexiones.s_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40,
                                                           y=90, x=70)
        labels = Label(pestania,
                       text="Movimiento del Hombro").place(bordermode=OUTSIDE, 
                                                           height=30, width=160,
                                                            y=90, x=110)  
        bemas = Button(pestania,text="E+",bg="Ivory3",
                       command = lambda: Conexiones.e_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                        height=40, width=40,
                                                         y=140, x=20)
        bemenos = Button(pestania, text="E-", bg="Ivory3",
                         command = lambda: Conexiones.e_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40,
                                                           y=140 , x=70)
        labele = Label(pestania,
                       text="Movimiento del Codo").place(bordermode=OUTSIDE, 
                                                         height=30, width=160, 
                                                         y=140, x=110) 
        
        bpmas = Button(pestania, text="P+", bg="Ivory3",
                       command = lambda: Conexiones.p_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                        height=40, width=40,
                                                         y=190 , x=20)
        bpmenos = Button(pestania, text="P-", bg="Ivory3",
                         command = lambda: Conexiones.p_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40, 
                                                          y=190, x=70)
        labelp = Label(pestania,
                       text="Inclinación de la Pinza").place(bordermode=OUTSIDE, 
                                                             height=30, width=160,
                                                              y=190, x=110)  
        brmas = Button(pestania, text="R+", bg="Ivory3",
                       command = lambda: Conexiones.r_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE,
                                                         height=40, width=40, 
                                                         y=240, x=20)
        brmenos = Button(pestania,text="R-",bg="Ivory3",
                         command = lambda: Conexiones.r_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40, 
                                                          y=240, x=70)
        labelr = Label(pestania,text="Rotación Pinza").place(bordermode=OUTSIDE, 
                                                             height=30, width=160,
                                                              y=240, x=110) 
        #cuadro2 Movimiento Cartesiano:Inserto elementos en este cuadro
        bxmas = Button(pestania,text="X+",bg="Ivory3",
                       command = lambda: Conexiones.x_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE,
                                                        height=40, width=40, 
                                                        y=325, x=20)
        bxmenos = Button(pestania,text="X-",bg="Ivory3",
                         command = lambda: Conexiones.x_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40, 
                                                          y=325, x=70)
        labelx = Label(pestania,text="Eje abscisas").place(bordermode=OUTSIDE, 
                                                           height=30, width=160, 
                                                           y=325, x=110)
        
        bymas = Button(pestania,text="Y+",bg="Ivory3",
                       command = lambda: Conexiones.y_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                        height=40, width=40, 
                                                        y=375 , x=20)
        bymenos = Button(pestania,text="Y-",bg="Ivory3",
                         command = lambda: Conexiones.y_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                          height=40, width=40,
                                                           y=375, x=70)
        labely = Label(pestania,text="Eje ordenadas").place(bordermode=OUTSIDE, 
                                                            height=30, width=160, 
                                                            y=375, x=110)
        bzmas = Button(pestania,text="Z+",bg="Ivory3",
                       command = lambda: Conexiones.z_mas(coordenadas,w1.get()),
                       activebackground="Ivory4").place(bordermode=OUTSIDE, 
                                                        height=40, width=40, 
                                                        y=425 , x=20)
        bzmenos = Button(pestania,text="Z-",bg="Ivory3",
                         command = lambda: Conexiones.z_menos(coordenadas,w1.get()),
                         activebackground="Ivory4").place(bordermode=OUTSIDE, height=40,
                                                           width=40, y=425 , x=70)
        labelz = Label(pestania,text="Eje de cotas").place(bordermode=OUTSIDE,
                                                            height=30, width=160, 
                                                            y=425, x=110)
        #cuadro3 Avance: Inserto elementos en este cuadro
        vavance = IntVar()
        txt = Label(pestania,text="Avance:").place(x=10,y=525)
        savance = Spinbox(pestania, from_=0, to=50 ,  wrap = True,increment=5,
                          buttonbackground="Ivory3", 
                          textvariable=vavance)
        savance.place(bordermode=OUTSIDE,height=20, width=40,x=100, y=525)
                          
        w1 = Scale(pestania, orient= HORIZONTAL,variable = vavance,
                   from_ = 0, to = 50, 
                   activebackground="Ivory3")
        w1.set(15)
        w1.place(bordermode=OUTSIDE, x=150, y=505)     
        #cuadro4 Movimiento Relativo
        varrela = StringVar()
        varrela.set("0") 
        varrelb = StringVar()
        varrelb.set("0") 
        varrelc = StringVar()
        varrelc.set("0") 
        varreld = StringVar()
        varreld.set("0") 
        varrele = StringVar()
        varrele.set("0") 
        bmover = Button(pestania, text="Mover",activebackground="Ivory4" ,
                        command = lambda: Conexiones.pos_rel(coordenadas,ar.get(),br.get(),cr.get(),dr.get(),er.get()),
                        bg="Ivory3")
        bmover.place(bordermode=OUTSIDE,height=60, width=60,x=330, y=510)
        ar = Spinbox(pestania, from_=-60, to=60 , textvariable=varrela,
                     wrap = True, increment=5,buttonbackground="Ivory3")
        ar.place(bordermode=OUTSIDE, height=30,width=60,x=450, y=535)
        textar = Label (pestania,text = "Cintura").place( x=455, y=510)
        br = Spinbox(pestania, from_=-60, to=60 ,textvariable=varrelb,
                      wrap = True, increment=5 , buttonbackground="Ivory3")
        br.place(bordermode=OUTSIDE, height=30,width=60,x=530, y=535)
        textbr = Label (pestania,text = "Hombro").place( x=545, y=510)
        cr = Spinbox(pestania, from_=-60, to=60, wrap = True, increment=5 ,
                     buttonbackground="Ivory3",textvariable=varrelc)
        cr.place(bordermode=OUTSIDE, height=30,width=60,x=610, y=535)
        textcr = Label (pestania,text = "Codo").place( x=620, y=510)
        dr = Spinbox(pestania, from_=-60, to=60, wrap = True, increment=5 ,
                     buttonbackground="Ivory3",textvariable=varreld)
        dr.place(bordermode=OUTSIDE,height=30, width=60,x=690, y=535)
        textdr = Label (pestania,text = "Inc.Pinza").place( x=690, y=510)
        er = Spinbox(pestania, from_=-60, to=60, wrap = True, increment=5, 
                     buttonbackground="Ivory3",textvariable=varrele)
        
        er.place(bordermode=OUTSIDE,height=30, width=60,x=770, y=535)
        
        texter = Label (pestania,text = "Giro Pinza").place( x=770, y=510)
     
        #cuadro5 Movimiento de la pinza
        tdesplaz = Label(pestania,
                         text="Velocidad de desplazamiento").place(bordermode=OUTSIDE,
                                                                    y=50, x=625)
        sdesplaz = Spinbox(pestania, from_=0, to=9 , wrap = True,
                           buttonbackground="Ivory3")
        sdesplaz.place(bordermode=OUTSIDE, height=20, width=40,x=800 ,y=50)
        
        ttiem = Label(pestania,
                      text="Tiempo de Aceleración/Deceleración:").place(bordermode=OUTSIDE, y=100, x=625)
        varbutton = IntVar()
        rbutton1 = Radiobutton(pestania, text="Rápido(H)", 
                               variable=varbutton, value=1)
        rbutton1.place(y=125,x=740)
        rbutton2 = Radiobutton(pestania, text="Lento (L)", 
                               variable=varbutton, value=2)
        rbutton2.place(y=150,x=740)
        bvel = Button(pestania,text="Establecer Velocidad",
                      command = lambda: Conexiones.velocidad(sdesplaz.get(),varbutton.get()),
                      activebackground="Ivory4",
                      bg="Ivory3").place(bordermode=OUTSIDE,height=40,
                                          width=150,y=200, x=700)
        #cuadro6 Velocidad del Robot: Insertamos los elementos
        bopen = Button(pestania,text="Abrir Pinza",
                       activebackground="Ivory4",
                       command = lambda: Conexiones.abrir_pinza(coordenadas,sinicial.get(),sretencion.get(),stiempo.get()),
                       bg="Ivory3").place(bordermode=OUTSIDE,
                                          height=40, width=100,y=325, x=650)
        bclose = Button(pestania,text="Cerrar pinza",
                        activebackground="Ivory4",
                        command = lambda: Conexiones.cerrar_pinza(coordenadas,sinicial.get(),sretencion.get(),stiempo.get()),
                        bg="Ivory3").place(bordermode=OUTSIDE, 
                                           height=40, width=100, y=325, x=765)
        sinicial= Spinbox(pestania, from_=0, to=15 ,
                           wrap = True,buttonbackground="Ivory3")
        sinicial.place(bordermode=OUTSIDE,height=20, width=40,x=825, y=375)
        tinicial = Label(pestania,text="Fuerza de Agarre Inicial").place(bordermode=OUTSIDE,
                                                                          y=375, x=650)
        sretencion= Spinbox(pestania, from_=0, to=15 , 
                            wrap = True,buttonbackground="Ivory3")
        sretencion.place(bordermode=OUTSIDE,height=20, width=40,x=825, y=410)
        tretencion = Label(pestania,text="Fuerza de Agarre de Retención").place(bordermode=OUTSIDE,
                                                                                 y=410, x=650)
        stiempo= Spinbox(pestania, from_=0, to=50 ,wrap = True, buttonbackground="Ivory3")
        stiempo.place(bordermode=OUTSIDE,height=20, width=40,x=825, y=445)
        ttiempo = Label(pestania,
                        text="Tiempo de retención ").place(bordermode=OUTSIDE, y=445, x=650)
        #Imagen
        photo = PhotoImage (file = "RobotP.GIF")
        image=Label(pestania,image=photo).place(x=280, y=20)
        mainloop()
        

    def pestana2(self,ventana,coordenadas):
        '''Funcion que crea los elementos de la ventana'''
        #cuadros 
        cuadro1 = LabelFrame(ventana,text = "Posiciones Empleadas",
                             font= "Helvetica").place(height=150, width=450,
                                                       x=5 , y=10)  
        cuadro2 = LabelFrame(ventana,text="Control de posiciones",
                             font= "Helvetica").place(height=275, width=450,
                                                       x=5, y=160)
        cuadro3 = LabelFrame(ventana,text="Opciones correspondientes al programa",
                             font= "Helvetica").place(height=135, width=905, 
                                                      x=5, y=435)  
        cuadro4 = LabelFrame(ventana,text="Movimientos del robot",
                             font= "Helvetica").place(height=210, width=450,
                                                       x=460 , y=10)  
        cuadro5 = LabelFrame(ventana,text="Código archivo",
                             font= "Helvetica").place(height=215, width=450,
                                                       x=460, y=220 )
        #cuadro 1 Posiciones Empleadas
        vars1 = IntVar()
        vars2 = IntVar()

        sposa = Spinbox(ventana, from_=1, to=29 , wrap = True, 
                       textvariable= vars1,buttonbackground="Ivory3", 
                       command = lambda: Funciones.Posicion(vars1.get(),vars2.get(),ventana,varpinza.get(),coordenadas))
        sposa.place(bordermode=OUTSIDE, height=30, width=80,x=200, y=50)
        tposa = Label(ventana,text="Posicion A").place(bordermode=OUTSIDE, y=50, x=25)
        scalea = Scale(ventana,variable=vars1,orient= HORIZONTAL,
                       activebackground="Ivory3", from_ = 1 , to = 29, 
                       command = lambda x: Funciones.Posicion(vars1.get(),vars2.get(),ventana,varpinza.get(),coordenadas))
        scalea.place(bordermode=OUTSIDE, x=305, y=35)
        sposb= Spinbox(ventana, from_=1, to=29 , wrap = True ,
                       buttonbackground="Ivory3", textvariable= vars2 , 
                       command = lambda: Funciones.Posicion(vars1.get(),vars2.get(),ventana,varpinza.get(),coordenadas))
        sposb.place(bordermode=OUTSIDE, height=30, width=80,x=200, y=100)
        tposb = Label(ventana,text="Posicion B").place(bordermode=OUTSIDE, y=100, x=25)
        scaleb = Scale(ventana,variable=vars2,orient= HORIZONTAL,
                       activebackground="Ivory3", from_ = 1 , to = 29, 
                       command = lambda x: Funciones.Posicion(vars1.get(),vars2.get(),ventana,varpinza.get(),coordenadas))
        scaleb.place(bordermode=OUTSIDE, x=305, y=85)
       

        #cuadro 2 Control de Posiciones
        varbutton = IntVar()
        rbutton1 = Radiobutton(ventana, variable=varbutton,
                                value=1).place(y=200,x=50)
        txtrb1 =  Label(ventana, 
                        text = "Establecer Posición actual como "+str(vars1.get())).place (y=200,x=70)
        
        rbutton2 = Radiobutton(ventana,  variable=varbutton,
                                value=2).place(y=235,x=50)
        txtrb2 =  Label(ventana,
                        text="Borrar las Posiciones comprendidas entre "+str(vars1.get()) +" y "+str(vars2.get()))
        txtrb2.place(y=235,x=70)
        
        rbutton3 = Radiobutton(ventana, variable=varbutton, 
                               value=3).place(y=270,x=50)
        txtrb3 =  Label(ventana, 
                        text="Mostrar las coordenadas de la Posición "+str(vars1.get()))
        txtrb3.place (y=270,x=70)
        rbutton4 = Radiobutton(ventana,
                               variable=varbutton, value=4).place(y=305,x=50)
        txtrb4 =  Label(ventana, 
                        text="Intercambiar las coordenadas de las Posiciones "+str(vars1.get())+" y "+str(vars2.get()))
        txtrb4.place (y=305,x=70)
        
        rbutton5 = Radiobutton(ventana, variable=varbutton, 
                               value=5).place(y=340,x=50)
        txtrb5 =  Label(ventana, 
                        text="Copiar las coordenadas de la Posición "+str(vars1.get())+" en la posición " +str(vars2.get()))
        txtrb5.place (y=340,x=70)
        
        botonacep = Button (ventana, text= "Ejecutar acción",bg="Ivory3",
                            command = lambda: Conexiones.ejecutar_accion(coordenadas,varbutton.get(),scalea.get(),scaleb.get()),
                            activebackground="Ivory4").place(height=35, 
                                                                   width=170, x=120, y=380)
         #cuadro 3 Opciones correspondientes al programa
         

        varenv = IntVar()
        botonenv = Button (ventana, text= "Enviar",bg="Ivory3",state=DISABLED,
                           activebackground="Ivory4",
                           command = lambda : Conexiones.enviar(varenv)).place(height=35,
                                                           width=80,x=50, y=475)
        marcoenv = Frame (ventana, bd=2 , 
                          relief = "groove").place(height=35, width=350,
                                                   x=130, y=476)
        rbenv = Radiobutton(ventana, text= "Enviar puntos al robot",state=DISABLED,
                            value=1,variable = varenv).place(x=140, y=480)
        rbenv2 = Radiobutton(ventana, text= "Enviar programa al robot" ,state=DISABLED,
                             value=2, variable = varenv).place(x=300, y=480)
        
        varrec = IntVar()
        botonrec = Button (ventana, text= "Recibir",bg="Ivory3",
                           activebackground="Ivory4",
                           command = lambda : Conexiones.recibir(varrec.get(),list1)).place(height=35, width=80,
                                                               x=50, y=515)
        marcorec = Frame (ventana, bd=2 , relief = "groove").place(height=35, width=350,
                                                                   x=130, y=516)
        rbrec = Radiobutton(ventana, text= "Recibir puntos del robot",
                            variable = varrec,value=1).place(x=140, y=520)
        rbrec2 = Radiobutton(ventana, text= "Recibir programa del robot" ,
                             variable = varrec,value=2).place(x=300, y=520)
        botonenv1 = Button (ventana, text= "Ejecutar \n código \n Archivo",bg="Ivory3",
                            activebackground="Ivory4").place( height=80, width=80,
                                                                    x=660, y=475)
        botonenv2 = Button (ventana, text= "  Borrar \n memoria \ncontrolador",bg="orange red",
                            activebackground="orange red3",
                           command= lambda : Conexiones.borrar_mem(ventana,list1)).place(height=80, width=80,
                                                                                x=560, y=475)
        botonenv3 = Button (ventana, text= "Borrar \n Código \n Archivo",bg="Ivory3",
                            command= lambda : Funciones.borrar_listbox(list1),
                            activebackground="Ivory4").place( height=80, width=80,
                                                                    x=760, y=475)
   #cuadro 4 -Movimiento del Robot
        varpinza = IntVar()
        botonmov = Button (ventana, text= " Mover hasta la Posición "+str(vars1.get())+" ",
                           command = lambda : Conexiones.pos_mov(varpinza.get(),vars1.get(),coordenadas),
                           activebackground="Ivory4",
                           bg="Ivory3").place(height=25, width=200,x=600, y=50)
        rabuttono = Radiobutton(ventana, text= "Pinza abierta", variable = varpinza, 
                                value=1, indicatoron = 1,
                                command = lambda: Funciones.Posicion(vars1.get(),vars2.get(),ventana,varpinza.get(),coordenadas))
        rabuttono.place(x=650, y= 100)
        rabuttonc = Radiobutton(ventana, text="Pinza Cerrada" ,variable = varpinza, 
                                value=2, indicatoron = 1,
                                command = lambda: Funciones.Posicion(vars1.get(),vars2.get(),ventana,varpinza.get(),coordenadas))
        rabuttonc.place(x=650, y= 130)
        
        botonmov = Button (ventana, text= " Incrementar Posición ",
                           command = lambda: Conexiones.pos_sigui(vars1.get(),coordenadas),
                           bg="Ivory3",activebackground="Ivory4").place( x=500, y=180)
        botonmov = Button (ventana, text= " Decrementar Posición ",
                           command = lambda: Conexiones.pos_ant(vars1.get(),coordenadas),
                           bg="Ivory3",activebackground="Ivory4").place( x=700, y=180)
        
     #cuadro 5 Código Programa
        
        frame1=Frame(ventana)
        frame1.place(height=180, width=420,x = 465 , y = 240)
        frame2= Frame(ventana)
        frame2.place(height=180, width=25,x = 880 , y = 240)
        scroll1=Scrollbar(frame2)
        list1=Listbox(frame1, height=15)
        list1.pack()
        Funciones.colocar_scrollbar(list1,scroll1)
  
        
   
if __name__ == '__main__':
    root = Tk()
    app = Mi_Aplicacion(root)
    
    app.mainloop()
