from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
import serial
import time
import sys
import os

from codigo.arduino import *

colorLetra = "color:#419f00;"
ColorBotones = "color:white;"
ColorRojo = 'color:red;'
border = "border: 0px solid black;"
fondo = "background-color:#000000;" + ColorBotones 
borderG = 'border:2px solid white;'
letraTexto = QFont('SansSerif',10)
letraTextoBold = QFont('SansSerif',10,QFont.Bold)
letraTitulo = QFont('SansSerif',15,QFont.Bold)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.port = ''
        self.isRun = True
        self.step = 20
        self.x = 0
        self.y = 0
        self.z = 0
        self.setWindowTitle("Monitor Serial")
        self.setStyleSheet(fondo)

        #Creacion Widget
        win = QWidget(self)
        gridLayout = QGridLayout()
        win.setLayout(gridLayout)

        Body = QFrame()
        
        gridLayout.setVerticalSpacing(0)
        gridLayout.addWidget(Body,0,0)
     
        fModoManual = QGroupBox('Monitor Serial')
        fModoManual.setFont(letraTextoBold)
        fModoManual.setStyleSheet(ColorBotones)
        
        BodyLayout = QGridLayout()
        Body.setLayout(BodyLayout)

        BodyLayout.addWidget(fModoManual,0,0)

        #Modo manual
        FEnviarDatos = QFrame()
        FControles = QFrame()
        FDatos = QFrame()
        FBotones = QFrame()

        DLayout = QVBoxLayout()
        FDatos.setLayout(DLayout)

        BLayout = QHBoxLayout()
        FBotones.setLayout(BLayout)

        FALayout = QGridLayout()
        FEnviarDatos.setLayout(FALayout)

        Mlayout = QGridLayout()
        fModoManual.setLayout(Mlayout)
        
        Mlayout.setVerticalSpacing(0)
        Mlayout.addWidget(FEnviarDatos,2,0)
        Mlayout.addWidget(FControles,0,0)
        Mlayout.addWidget(FDatos,1,0)

        RFrame = QGroupBox("Serial Cominicaciones")
        self.estiloLetraBlanco(RFrame)

        FLayout = QGridLayout()
        FControles.setLayout(FLayout)

        FLayout.addWidget(RFrame,0,0)
        
        ArLayout = QGridLayout()
        RFrame.setLayout(ArLayout)
        
        #Modo manual
        self.bConectar = QPushButton("Conectar")
        self.bConectar.clicked.connect(self.conectarArduino)
        self.estiloLetraBlanco(self.bConectar)
	  
        self.tBaudRate = QLineEdit("9600")
        self.estiloLetraBlanco(self.tBaudRate)

        self.tPuerto = QLineEdit("/dev/ttyUSB0")
        self.estiloLetraBlanco(self.tPuerto)

      
        bEnviar = QPushButton('Enviar')
        bEnviar.clicked.connect(self.mandarDatos)
        self.estiloLetraBlanco(bEnviar)
              
        self.tData = QLineEdit('Data del Arduino')
        self.tData.setReadOnly(True)
        self.estiloLetraBlanco(self.tData)

        self.tEnviar = QLineEdit()
        self.estiloLetraBlanco(self.tEnviar)
        

        #shortcut
        sConectar = QShortcut(QKeySequence("C"),win)
        sConectar.activated.connect(self.conectarArduino)
        
        sEnviar = QShortcut(QKeySequence("Ctrl+e"),win)
        sEnviar.activated.connect(self.mandarDatos)
            
        #LAYOUUT
        #HLayout.addWidget(cicata)
        #HLayout.addWidget(titulo)
        
        ArLayout.addWidget(self.tPuerto,0,0)
        ArLayout.addWidget(self.tBaudRate,1,0)
        ArLayout.addWidget(self.bConectar,2,0)



        DLayout.addWidget(self.tData)
        
        FALayout.addWidget(bEnviar,0,1)
        FALayout.addWidget(self.tEnviar,0,0)
       
        win.setFixedSize(gridLayout.sizeHint())
        self.setFixedSize(gridLayout.sizeHint()) 

#Funciones

    def estiloLetraBlanco(self,widget):
        widget.setStyleSheet(ColorBotones)
        widget.setFont(letraTexto)
    
    def mandarDatos(self):
        #dato = self.tEnviar.text() +'\r\n'
        dato = self.tEnviar.text()
        self.enviarFarmbot(dato)

    def enviarFarmbot(self,mensaje):
        try:
            self.farmbot.enviarDatos(mensaje)
            self.tData.setText(mensaje)
        except:
            print("No se envio datos")

    def leerDatos(self):
        time.sleep(1.0)
        self.farmbot.reinicarBuffer()
        while self.isRun:
            self.arduinoString = self.farmbot.recibirDatos()
            self.data = self.arduinoString.decode('utf-8',errors='replace')
            print(self.data)

        self.farmbot.arduino.close()
    
    def closeEvent(self,event):
        self.isRun = False
        print("Estoy cerrando el programa")
        time.sleep(0.5)


    def conectarArduino(self):
        self.port = self.tPuerto.text()
        self.baudRate = int(self.tBaudRate.text())
	  
        print(self.port)
        if self.bConectar.text() == 'Conectar':
            try:
                self.isRun = True
                self.farmbot = arduino(self.port,self.baudRate)
                self.thread = Thread(target=self.leerDatos)
                self.thread.start()
                self.bConectar.setText('Desconectar')
                self.bConectar.setStyleSheet(ColorRojo)
            except Exception as e:
                print(e)
        else:
            self.isRun = False
            self.bConectar.setText('Conectar')
            self.bConectar.setStyleSheet(ColorBotones)
                    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
