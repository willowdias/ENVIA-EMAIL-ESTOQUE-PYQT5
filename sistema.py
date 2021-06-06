from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import  uic, QtWidgets
import sys
from PyQt5.QtCore import QDate, QDateTime, QTimer, QTime, QUrl, Qt
from PyQt5.QtGui import QFont, QPixmap,QIcon
import sys
from datetime import date
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFileDialog
from html import*
from css import*
from sistemaemail import*
from PyQt5 import QtWidgets
from qtwidgets import Toggle, AnimatedToggle
class sistema_login(QtWidgets.QMainWindow):
    def __init__(self):
        super(sistema_login, self).__init__()
        uic.loadUi('venda.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("icon/evolucao.jpeg"))
        QtWidgets.qApp.setStyleSheet("background-color: red;")
        #create chama 
        self.combox_porta_smtp()
        #create funcçoes inicial
        self.bt_exit.clicked.connect(self.click_exit)
        self.pushButton.clicked.connect(self.sobre)
        self.ok.clicked.connect(self.google)
        self.actionincial.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.inicial))
        self.actionEMAIL.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.email))
        self.checkBox.toggled.connect(self.password_check)#VER SENHA
        self.bt_salvar.clicked.connect(self.salvar_credenciais)
        self.bt_ajuda.clicked.connect(self.ver_credenciais)#ver
        self.bt_caixa_email.clicked.connect(self.chammartelaemail)#chamar tela email


    #chama data e hora curso
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hora_data)
        self.timer.start()
        #####        
    def hora_data(self):
        #create hora
        current_time = QDateTime.currentDateTime()
        label_time3 = current_time.toString('dd/MM/yyyy '+' hh:mm:ss'+' dddd')
        self.label_data_hora.setText(label_time3)
    def click_exit(self):#fechar tela sistema
        self.close()
    def click_minizer(self):#minimizer tela
        self.showMinimized()   

    def click_minizer_maximinizer(self):#maxmininzar
        if self.isMaximized():            
            self.showNormal()
        else:
            self.showMaximized() 
    def sobre(self):
        if self.pushButton.isChecked():
            pass
            
        else:            
            msg = QtWidgets.QMessageBox()
            msg.setText("SISTEMA DE ATENDIMENTO\n"
            "CELULAR (69)992-702408")            
            msg.setWindowTitle("SOBRE")
            msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            #msg.setStandardButtons(msg.Save | msg.Discard | msg.Cancel);
            msg.setWindowIcon(QtGui.QIcon("icon/sobre.png"))
            msg.setIconPixmap(QtGui.QPixmap("icon/sobre.png"))
            msg.setStyleSheet("QMessageBox{background-color: rgb(51, 51, 51);}QMessageBox QLabel {color: rgb(200, 200, 200);}"
            "QPushButton{background-color: rgb(103, 255, 128);font: 87 14pt Arial;}"
            "QPushButton:hover{background-color: rgb(0, 0, 255);}")
            msg.exec_()
    def salvar_credenciais(self):
        if self.line_email.text() == "":
            QMessageBox.warning(QMessageBox(), 'ERROR', 'PREENCHA O CAMPO E-MAIL!')
            return None

        if self.line_senha.text() == "":
            QMessageBox.warning(QMessageBox(), 'ERROR', 'PREENCHA O CAMPO SENHA!')
            return None

       
        
  

        else:
            
            if self.comboBox_smtp.currentText()=='smtp-relay.gmail.com':
                self.label_porta.setText('465')
             
            elif self.comboBox_smtp.currentText()=='smtp.live.com'or'smtp.brturbo.com.br'or'smtps.uol.com.br':
                self.label_porta.setText('587')
            elif self.comboBox_smtp.currentText()=='smtp.globo.com'or'smtp.mail.yahoo.com.br':
                self.label_porta.setText('25')
            self.bufersize = 64 * 1024
            self.arquivo = open('sistemaemail.txt', 'w')
            self.arquivo.write(f'{self.line_email.text()}\n')
            self.arquivo.write(f'{self.line_senha.text()}\n')
            self.arquivo.write(f'{self.comboBox_smtp.currentText()}\n')
            self.arquivo.write(f'{self.label_porta.text()}\n')
            self.arquivo.close()
            self.line_email.setText("")
            self.line_senha.setText("")

    def combox_porta_smtp(self):
        listasmtp=['','smtp-relay.gmail.com','smtp.live.com','smtp.brturbo.com.br','smtp.globo.com','smtps.uol.com.br'
        'smtp.mail.yahoo.com.br','smtp.globo.com','smtp.mail.yahoo.com.br']
        listaporta=['','465','587','25']
        self.comboBox_smtp.addItems(listasmtp)
        #self.comboBox_porta.addItems(listaporta) 
   

    def password_check(self):
        
        bt=self.sender()
     
        if bt.isChecked() == True:
            self.line_senha.setEchoMode(QLineEdit.Password)   
        else:  
            self.line_senha.setEchoMode(QLineEdit.Normal)
            
    def ver_credenciais(self):
      
        arquivo = open('sistemaemail.txt', encoding='utf8')
        lista = []
        for linha in arquivo:
            linha = linha.strip()
            lista.append(linha)

        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("SOBRE")
        self.msg.setWindowIcon(QtGui.QIcon("icon/sobre.png"))
        self.msg.setIconPixmap(QtGui.QPixmap("icon/sobre.png"))
        self.msg.setText(f'Email:{lista[0]}\nSenha:{lista[1]}\nSeviço-email:{lista[2]}\nPorta:{lista[3]}')
        self.msg.setStyleSheet("background-color: rgb(180, 180, 180);QMessageBox{font: 87 12pt Arial;color:white;}"
            "QPushButton{background-color: rgb(103, 255, 128);font: 87 12pt Arial;}"
            "QPushButton:hover{background-color: rgb(0, 0, 255);}")        
        self.msg.exec_()
        
    def google(self):
        self.chmar=googlesistema()
        self.chmar.show()
    def chammartelaemail(self):
        self.hide()
        self.chmar=tela_email()
        self.chmar.show()
        
if __name__ == '__main__':    

    app = QtWidgets.QApplication(sys.argv)
    #window = QtWidgets.QMainWindow()
    demo = sistema_login()
    app.setStyleSheet(style)
    demo.show()
    sys.exit(app.exec_())