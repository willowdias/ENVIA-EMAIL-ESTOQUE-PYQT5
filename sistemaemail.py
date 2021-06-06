from email.message import EmailMessage
from email.mime.text import MIMEText
import smtplib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import  uic, QtWidgets
import os
import sys
from sistema import*
class tela_email(QtWidgets.QMainWindow):
    def __init__(self):
        super(tela_email, self).__init__()
        uic.loadUi('caixaemail.ui', self)
        self.setWindowTitle("EVOLUÇAO EMAIL")
        self.setWindowIcon(QtGui.QIcon("icon/evolucao.jpeg"))
        self.statusBar().showMessage("EMAIL")
        #create line edite funçao digita maisculo
        self.lineEdit_email_add.textChanged.connect(self.press)
        self.lineEdit.textChanged.connect(self.press)
        #close funcoes
        self.progressnavegar.close() 
        self.lineEdit.close()
        self.web_browser.close()
        #menu navegador
        self.web_browser.setUrl(QUrl('https://www.google.com.br'))
        #create frame check box
        self.status=QFrame(self)
        self.botao=AnimatedToggle(self.status,)
        self.botao.setToolTip('LIGAR')  
        self.botao.setWindowTitle('LIGAR')
        self.botao.setFixedSize(85,60)     
        self.status.setGeometry(15,95,85,85)
        ############################################
        #funçao libera line botao
        self.funcaoliberar()
        #close progresso bar
        self.progressBar.close()
        #create funçao preencher email
        self.preencher_email()
        #CREATE TAMANAHO COLUNA TABLEWIDEG
        self.tableWidget.setColumnWidth(0,15)#id
        self.tableWidget.setColumnWidth(1,350)#email
        #create funçao envia
        self.bt_enviar.clicked.connect(self.enviar_email)#chamar tela email
        self.bt_anexa.clicked.connect(self.anexar_arquivo)#anexa arquivo
        self.bt_volta.clicked.connect(self.tela_email)#volta tela de emai
        self.bt_mais.clicked.connect(self.addemail)#ADICIONAR EMAIL tablewidget
        self.bt_menos.clicked.connect(self.removeemail)#removo tablewideg email
        self.botao.toggled.connect(self.botaobr)
        self.checkBox_habilitar.toggled.connect(self.checkhabilitar)#hababilitar navegaçao
        #create funçao botao navegador
        self.botao_envia_site.clicked.connect(self.navega)
    def press(self):#funçao digitar
        b=self.lineEdit.text().upper()
        self.lineEdit.setText(b)
        maisculo=self.lineEdit_asstuno.text().upper()
        self.lineEdit_asstuno.setText(maisculo)
        #self.lineEdit_2.clear()       
    def funcaoliberar(self):
        #create linede edite
        self.lineEdit_email.setEnabled(False)
        self.lineEdit_email_add.setEnabled(False)
        self.lineEdit_asstuno.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.bt_mais.setEnabled(False)
        self.bt_menos.setEnabled(False)
        self.bt_anexa.setEnabled(False)
        self.bt_enviar.setEnabled(False)
    def liberar(self):
        self.lineEdit_email.setEnabled(True)
        self.lineEdit_email_add.setEnabled(True)
        self.lineEdit_asstuno.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.bt_mais.setEnabled(True)
        self.bt_menos.setEnabled(True)
        self.bt_anexa.setEnabled(True)
        self.bt_enviar.setEnabled(True)
    def anexar_arquivo(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif *.pdf *)")
            self.label_3.setPixmap(QtGui.QPixmap(file_name))
            self.label_caminho.setText(file_name)
        except Exception as ERROR:
            print(ERROR)
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(), 'ERROR', 'SELECIONE O(S) ARQUIVO(s)')

    def tela_email(self):
        self.hide()
        self.chmar=sistema_login()
        self.chmar.show()
    def enviar_email(self):
        email_edite=self.lineEdit_email.text()
        caminhofoto=self.label_caminho.text()
        nomedafoto=self.lineEdit_nome.text()
        tipoaquivo=self.comboBox_formato.currentText().lower()
        if  email_edite == "" or email_edite == "" or self.textEdit.toPlainText() == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(), 'ERROR', 'PREENCHA ESSES CAMPOS ABAIXO \naaaaaaaDIGITE O E-MAIL DO DESTINATARIO!\n'
            'DIGITE O ASSUNTO DO E-MAIL!\nDIGITE A MENSAGEM PARA O DESTINATARIO!')
    
        else:
            try:
                #ler arquivo txt
                arquivo = open('sistemaemail.txt', mode='r',encoding='utf8')
                lista = []
                for linha in arquivo:
                    linha = linha.strip()
                    lista.append(linha)

                arquivo.close()
                email = lista[0]
                senha = lista[1]
                smpt = lista[2]
                porta = lista[3]
                #ler email e a porta dentro do arquivo
                self.server = smtplib.SMTP(smpt, int(porta))
                self.server.starttls()
                self.server.login(email, senha)
                try:
                    self.mail = EmailMessage()
                    self.mail['From'] = email#email do banco
                    self.mail['To'] = self.lineEdit_email.text();self.lineEdit_email_add.text()#email destinatario
                    self.mail['Subject'] = self.lineEdit_asstuno.text().upper()#assunto
                    self.mail.set_content(self.textEdit.toPlainText())
                    #funcçao arquivo
                    foto = MIMEText(open(f'{caminhofoto}','rb').read(), 'base64', 'utf-8')
                    foto['Content-disposition'] = f'attachment;filename="{nomedafoto}.{tipoaquivo}"'
                    self.mail.set_content(foto)
                    #carregando envio progressobar
                    self.progressBar.show() 
                    self.completo=0
                    self.progressBar.setFormat("ENVIANDO")
                    while self.completo < 100:                
                        self.completo += 0.0001
                        self.progressBar.setValue(self.completo)   
                    #funçaoenvio para email
                    self.server.send_message(self.mail)#funçao envia
                    if QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(), f'{lista[0]}', 'E-MAIL ENVIADO COM SUCESSO!'):
                        self.bufersize = 64 * 1024
                        self.arquivo = open('email.txt', 'a')
                        self.arquivo.write(f'{email_edite}\n')
                        self.arquivo.close()
                        self.lineEdit_email.setText("")
                        self.lineEdit_asstuno.setText("")
                        self.lineEdit_email_add.setText("")
                        self.textEdit.setText("")
                        self.preencher_email()
                        self.progressBar.close() 
                except Exception as ERROR:
                    print(ERROR)
            except Exception as ERROR:
                print(ERROR)
    ######################################################funçoes################################################################           
    def preencher_email(self):
        try:
            #preencher site
            arquivo = open('site.txt',encoding='utf8')
            site=[]
            for linha in arquivo:
                linha = linha.strip()
                site.append(linha)
            arquivo.close()
            completer = QtWidgets.QCompleter(site)
            self.lineEdit_navega.setCompleter(completer) 
            #preencer email
            arquivo = open('email.txt',encoding='utf8')
            lista = []
            for linha in arquivo:
                linha = linha.strip()
                lista.append(linha)
            arquivo.close()
            completer = QtWidgets.QCompleter(lista)
            self.lineEdit_email.setCompleter(completer)
            self.lineEdit_email_add.setCompleter(completer)
             
        except:
            print(os.error)
    def addemail(self):#adicionar tablewidegt
        b=self.lineEdit_email_add.text().lower()
        if self.lineEdit_email_add.text()=="":
            self.menssagemerro()
            
        else:
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            self.tableWidget.setItem(numRows, 1, QTableWidgetItem(b))
            self.lineEdit_email_add.setText("")
    def removeemail(self):#remove linha 
        linha = self.tableWidget.currentRow()
        self.tableWidget.removeRow(linha)
    def checkhabilitar(self,pressed):
        if pressed:
            self.web_browser.show()
            self.lineEdit.show()
        else:
            self.lineEdit.close()
            self.web_browser.close()

    def botaobr(self,pressed):
        if pressed:
            self.liberar()#libera botao
            self.statusBar().showMessage("LIBERADO")
        else:
            self.setWindowIcon(QtGui.QIcon("icon/evolucao.jpeg"))
            self.funcaoliberar()#bloquear botao
            self.statusBar().showMessage("BLOQUEADO")
            self.lineEdit_email.setText("")
            self.lineEdit_asstuno.setText("")
            self.lineEdit_email_add.setText("")
            self.textEdit.setText("")
    def menssagemerro(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setText("SISTEMA DE ATENDIMENTO\n"
        "CELULAR (69)992-702408")            
        self.msg.setWindowTitle("ERRO")
        self.msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #msg.setStandardButtons(msg.Save | msg.Discard | msg.Cancel);
        self.msg.setWindowIcon(QtGui.QIcon("icon/erro.ico"))
        self.msg.setIconPixmap(QtGui.QPixmap("icon/erro.ico"))
        self.msg.setStyleSheet("QMessageBox{background-color: rgb(51, 51, 51);}QMessageBox QLabel {color: rgb(200, 200, 200);}"
        "QPushButton{background-color: rgb(103, 255, 128);font: 87 14pt Arial;}"
        "QPushButton:hover{background-color: rgb(0, 0, 255);}")
        self.statusBar().showMessage("CAMPOS VAZIO PREENCHA")
        self.setWindowIcon(QtGui.QIcon("icon/erro.ico"))
        self.msg.exec_()
    def navega(self):
        import time
        self.progressnavegar.show() 
        self.completo=0
        t=self.lineEdit_navega.text()
        self.progressnavegar.setFormat("CARREGANDO")
        while self.completo < 100:                
            self.completo += 0.0001
            self.progressnavegar.setValue(self.completo)
        if t=="":
            QtWidgets.QMessageBox.about(self, "Title", "CAMPO URL VAZIO \n SEJA BEM VINDO")
        if t==self.lineEdit_navega.text():
            self.web_browser.setUrl(QUrl(f'http://{t}'))
            time.sleep(0.5);
            self.arquivo = open('site.txt', 'a')
            self.arquivo.write(f'{t}\n')
            self.arquivo.close()
        else:
            print('ok')
        self.progressnavegar.close()          
if __name__ == '__main__':    

    app = QtWidgets.QApplication(sys.argv)
    #window = QtWidgets.QMainWindow()
    demo = tela_email()
    demo.show()
    sys.exit(app.exec_())