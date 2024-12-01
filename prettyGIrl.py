
from PyQt5.QtWidgets import QWidget,QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QSpacerItem, QSizePolicy, QFrame, QHBoxLayout, QScrollArea, QStackedWidget, QLayout
from PyQt5.QtCore import Qt
import time
import sys

# 반복되는 구조 간결하게 고치기 [12.2 해결]

class login_widget(QWidget):
    def __init__(self):
        super().__init__()

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

        user_widgets = QVBoxLayout()
        pass_widgets = QVBoxLayout()
        available_widgets = QVBoxLayout()
        main_layout = QVBoxLayout()

        self.setFixedSize(300,400)
        self.setObjectName("background")

        main_label = QLabel("Voca")
        main_label.setObjectName("voca")

        username = QLineEdit(self)
        username.setPlaceholderText("UserName")

        password = QLineEdit(self)
        password.setPlaceholderText("Password")
        password.setEchoMode(QLineEdit.Password)

        forget_user = QLabel("Foreget username?")
        forget_user.mousePressEvent = self.stupid_user
        forget_user.setObjectName("Forget")

        forget_pass = QLabel("Forget password?")
        forget_pass.mousePressEvent = self.stupid_user
        forget_pass.setObjectName("Forget")

        sumbit_button = QPushButton("Sign In", self)
        sumbit_button.setFixedSize(150,30)
        sumbit_button.clicked.connect(self.was_sumbited)

        user_widgets.addWidget(username)
        user_widgets.addWidget(forget_user)

        pass_widgets.addWidget(password)
        pass_widgets.addWidget(forget_pass)

        available_widgets.addLayout(user_widgets)
        available_widgets.addLayout(pass_widgets)

        main_layout.addSpacerItem(QSpacerItem(0,20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        main_layout.addWidget(main_label)
        main_layout.addSpacerItem(QSpacerItem(0,30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        main_layout.addLayout(available_widgets)
        main_layout.addWidget(sumbit_button, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)

        self.setLayout(main_layout)


    def stupid_user(self, event):
        print("*The username and password can be anything*")

    def was_sumbited(self, event):
        parent_widget = self.parent()

        if isinstance(parent_widget, QStackedWidget):
            parent_widget.setCurrentIndex(1)
        else:
            print("orphanage")

class lobby_widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(300,400)

        top_frame = QFrame(self)
        top_frame.setFixedSize(300,80)
        top_frame.setObjectName("top")

        middle_frame = QFrame(self)
        middle_frame.setFixedSize(300,40)
        middle_frame.setObjectName("middle")

        bottom_frame = QScrollArea(self)
        bottom_frame.setFixedSize(300,280)
        bottom_frame.setObjectName("bottom")

        main_label = QLabel("Wataya", top_frame)
        main_label.setObjectName("voca-label")

        create_voca = self.create_button("create", 80, 20, self.create_voca, middle_frame)
        delete_voca = self.create_button("delete", 80, 20, self.delete_voca, middle_frame)
        load_voca = self.create_button("load", 100, 20, self.load_voca, middle_frame)

        button_layout = QHBoxLayout(middle_frame)
        button_layout.addWidget(create_voca)
        button_layout.addWidget(delete_voca)
        button_layout.addWidget(load_voca)
        button_layout.setContentsMargins(5,0,0,0)

        frame_layout = QVBoxLayout(self)
        frame_layout.addWidget(top_frame)
        frame_layout.addWidget(middle_frame)
        frame_layout.addWidget(bottom_frame)
        frame_layout.setContentsMargins(0,0,0,0)
        frame_layout.setSpacing(0)

        self.setStyleSheet("""
            #top { 
                background-color : #FFFFFF;
                border : 0px;
            }  
            #middle { 
                background-color : #FFFFFF;            
                border-top : 1px solid #E0E0E0;
                border-bottom : 1px solid #F2F2F2;
            }
            #bottom { 
                background-color : #FFFFFF;   
                border : 0px;     
            }
            #voca-label { 
                color : #33FF33;
                font-size : 50px;
                font-weight : bold;
                margin-left : 5px;
                margin-top : 5px;
            }
        """)

    def create_button(self, title ,width, height, connectEvent, parent):
        button = QPushButton(title, parent)
        button.setFixedSize(width, height)
        button.clicked.connect(connectEvent)
        button.setStyleSheet("""
            QPushButton {
                background-color : #FFFFFF;
                color : #DBDBDB;
                border-radius : 10px;
                border : 1px solid #F2F2F2;
                font : bold;
            }
            QPushButton:hover {
                color : #222222;    
            }
        """)

        return button
    
    def create_voca(self, event):
        print("was created")


    def delete_voca(self, event):
        print("was deleted")

    def load_voca(self, event):
        print("was loaded")

class widget_controller(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(300,400)

        self.stack_wideget = QStackedWidget(self)
        self.stack_wideget.setContentsMargins(0,0,0,0)
        self.stack_wideget.setStyleSheet("background-color : #FFFFFF;")

        Login_widget = login_widget()
        Lobby_widget = lobby_widget()

        self.stack_wideget.addWidget(Login_widget)
        self.stack_wideget.addWidget(Lobby_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.stack_wideget)
        self.setLayout(layout)

        self.stack_wideget.setCurrentIndex(0)

app = QApplication([])

window = widget_controller()
window.show()

app.exec_()