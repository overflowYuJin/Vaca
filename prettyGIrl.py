
from PyQt5.QtWidgets import QWidget,QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import sys

# 부자연스러운 Voca 해결하기 11.30


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()


        self.setStyleSheet("""
            #voca {
                color : #33FF33;
                font : bold 60px;  
            }
            #background {background-color : #FFFFFF;}
            #Forget {color : rgba(128, 128, 128, 0.5);}

            QLineEdit {
                background-color : #555555;
                border : 10px solid #555555;
                border-radius : 15px;

            }
            QPushButton {
                color : white;
                background-color : #33FF33; 
                border-radius : 15px;  
                font : bold;      
            }





        """)

        self.UserWidgets = QVBoxLayout()
        self.PassWidgets = QVBoxLayout()
        self.AvailableWidgets = QVBoxLayout()
        self.MainLayout = QVBoxLayout()

        self.setFixedSize(300,400)
        self.setObjectName("background")

        self.MainLabel = QLabel("Voca")
        #self.MainLabel.setAlignment(Qt.AlignCenter)
        self.MainLabel.setObjectName("voca")

        self.UserName = QLineEdit(self)
        self.UserName.setPlaceholderText("UserName")

        self.Password = QLineEdit(self)
        self.Password.setPlaceholderText("Password")
        self.Password.setEchoMode(QLineEdit.Password)

        self.ForgetUser = QLabel("Foreget username?")
        self.ForgetUser.mousePressEvent = self.StupidUser
        self.ForgetUser.setObjectName("Forget")

        self.ForgetPass = QLabel("Forget password?")
        self.ForgetPass.mousePressEvent = self.StupidUser
        self.ForgetPass.setObjectName("Forget")

        self.SignInButton = QPushButton("Sign In", self)
        self.SignInButton.setFixedSize(150,30)
        self.SignInButton.clicked.connect(self.WasSumbited)

        self.UserWidgets.addWidget(self.UserName)
        self.UserWidgets.addWidget(self.ForgetUser)

        self.PassWidgets.addWidget(self.Password)
        self.PassWidgets.addWidget(self.ForgetPass)

        self.AvailableWidgets.addLayout(self.UserWidgets)
        self.AvailableWidgets.addLayout(self.PassWidgets)

        self.MainLayout.addWidget(self.MainLabel)
        self.MainLayout.addSpacerItem(QSpacerItem(0,50, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.MainLayout.addLayout(self.AvailableWidgets)
        self.MainLayout.addWidget(self.SignInButton, alignment=Qt.AlignCenter)
        self.MainLayout.addStretch(1)

        self.setLayout(self.MainLayout)


    def StupidUser(self, event):
        print("*The username and password can be anything*")
    

    def WasSumbited(self, evnet):
        print("Cool..")


app = QApplication(sys.argv)
window = LoginWidget()
window.show()
sys.exit(app.exec_())