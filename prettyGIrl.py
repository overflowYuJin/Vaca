
from PyQt5.QtWidgets import QWidget,QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QSpacerItem, QSizePolicy, QFrame, QHBoxLayout, QScrollArea, QStackedWidget
from PyQt5.QtCore import Qt
import time
import sys

# Top StyleSheet 해결하기 
# 반복되는 구조 간결하게 고치기

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.logic_widget = Logic_widget(self)

        self.setStyleSheet("""
            #voca {
                color : #33FF33;
                font : bold 60px;  
                margin-left : 5px;
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

        UserWidgets = QVBoxLayout()
        PassWidgets = QVBoxLayout()
        AvailableWidgets = QVBoxLayout()
        MainLayout = QVBoxLayout()

        self.setFixedSize(300,400)
        self.setObjectName("background")

        MainLabel = QLabel("Voca")
        MainLabel.setObjectName("voca")

        UserName = QLineEdit(self)
        UserName.setPlaceholderText("UserName")

        Password = QLineEdit(self)
        Password.setPlaceholderText("Password")
        Password.setEchoMode(QLineEdit.Password)

        ForgetUser = QLabel("Foreget username?")
        ForgetUser.mousePressEvent = self.StupidUser
        ForgetUser.setObjectName("Forget")

        ForgetPass = QLabel("Forget password?")
        ForgetPass.mousePressEvent = self.StupidUser
        ForgetPass.setObjectName("Forget")

        SignInButton = QPushButton("Sign In", self)
        SignInButton.setFixedSize(150,30)
        SignInButton.clicked.connect(self.on_sign_in)

        UserWidgets.addWidget(UserName)
        UserWidgets.addWidget(ForgetUser)

        PassWidgets.addWidget(Password)
        PassWidgets.addWidget(ForgetPass)

        AvailableWidgets.addLayout(UserWidgets)
        AvailableWidgets.addLayout(PassWidgets)

        MainLayout.addSpacerItem(QSpacerItem(0,20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        MainLayout.addWidget(MainLabel)
        MainLayout.addSpacerItem(QSpacerItem(0,30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        MainLayout.addLayout(AvailableWidgets)
        MainLayout.addWidget(SignInButton, alignment=Qt.AlignCenter)
        MainLayout.addStretch(1)

        self.setLayout(MainLayout)


    def StupidUser(self, event):
        print("*The username and password can be anything*")

    def on_sign_in(self):
        self.logic_widget.Constant = 1
        self.logic_widget.process_logic()


class LobbyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(300,400)

        TopFrame = QFrame(self)
        TopFrame.setFrameStyle(QFrame.Box)
        TopFrame.setFixedSize(300,100)
        TopFrame.setObjectName("Top")

        GreetingLabel = QLabel("Welcome!")
        GreetingLabel.setFixedSize(300,50)
        GreetingLabel.setObjectName("Greeting")

        CreateButton = QPushButton("Create", TopFrame)
        CreateButton.clicked.connect(self.CreateVoca)
        CreateButton.setFixedSize(80,20)
        CreateButton.setObjectName("Button")

        DeleteButton = QPushButton("Delete", TopFrame)
        DeleteButton.clicked.connect(self.DeleteVoca)
        DeleteButton.setFixedSize(80,20)
        DeleteButton.setObjectName("Button")

        LoadVocaButton = QPushButton("Load", TopFrame)
        LoadVocaButton.clicked.connect(self.LoadVoca)
        LoadVocaButton.setFixedSize(100,20)
        LoadVocaButton.setObjectName("Button")

        ScrollArea = QScrollArea(self)
        ScrollArea.setStyleSheet("background-color : #FFFFFF;")
        ScrollArea.setWidgetResizable(False)
        ScrollArea.setFixedSize(300,300)

        FrameLayouts = QVBoxLayout()
        topWidgetLayout = QVBoxLayout(TopFrame)
        connectButtons = QHBoxLayout()

        connectButtons.addWidget(CreateButton)
        connectButtons.addWidget(DeleteButton)
        connectButtons.addWidget(LoadVocaButton)
        connectButtons.setContentsMargins(0,0,0,0)
        connectButtons.setSpacing(5)

        topWidgetLayout.addWidget(GreetingLabel)
        topWidgetLayout.addLayout(connectButtons)

        FrameLayouts.addWidget(TopFrame)
        FrameLayouts.addWidget(ScrollArea)
        FrameLayouts.setContentsMargins(0,0,0,0)
        FrameLayouts.setSpacing(0)

        self.setStyleSheet("""
            #Top {
                background-color : #33FF33;
                border : 0px;       
            }
            #Greeting {
                color : #FFFFFF;
                font : bold 50px;  
                margin-left : 5px;
            }
            #Label {
                color : #E8E8E8; 
                font : italic;
                font-weight : 600
            }
            #TouchedLabel {
                color : #4D4DFF;
                font : bold 15px;
                           }
            #TouchedLabel:hover {
                color : #FFFFFF
            }
            #Button {
                background-color : #2542FF;
                border-radius : 10px;
                font : 13px;
            }
            #Button:hover {
                background-color : #FF9900;
            }
        """)

        self.setLayout(FrameLayouts)

    def CreateVoca(self, event):
        pass

    def DeleteVoca(self, event):
        pass

    def LoadVoca(self, event):
        pass


class Logic_widget():
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.Constant = 0
        self.login_widget = parent_widget
        self.lobby_widget = None

    def process_logic(self):
        if self.Constant == 0:
            if self.lobby_widget:
                self.lobby_widget.close()
            self.login_widget.show()
        
        if self.Constant == 1:
            self.login_widget.close()
            if not self.lobby_widget:
                self.lobby_widget = LobbyWidget()
            self.lobby_widget.show()


app = QApplication([])
window = LoginWidget()
window.show()
app.exec_()