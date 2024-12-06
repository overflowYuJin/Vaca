
from PyQt5.QtWidgets import QWidget,QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QSpacerItem, QSizePolicy, QFrame, QHBoxLayout, QScrollArea, QStackedWidget, QLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
import os 
import sqlite3

# 반복되는 구조 간결하게 고치기 [12.2 해결]
# 다 만들면 스타일시트 맨 아래로 보내기 (미완성이라 위에 배치)

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
                margin-top : 10px;
            }
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

        db = os.path.abspath("Girl.db")
        conn = sqlite3.connect(db)

        self.Cursor = conn.cursor()

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

        main_label = QLabel("Shinobu", top_frame)
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


    def create_button(self, title ,width, height, connectEvent, parent):
        button = QPushButton(title, parent)
        button.setFixedSize(width, height)
        button.clicked.connect(connectEvent)

        return button
    
    def create_voca(self, event):
        # 제작시 반드시 로드를 통해 위젯을 불러옴

        self.setEnabled(False)
        self.create_window = create_voca_widget(self.Cursor, self)
        self.create_window.show()

    def delete_voca(self, event):
        # 삭제시 반드시 로드를 통해 위젯을 불러옴
        print("was deleted")

    def load_voca(self, event):
        self.Cursor.execute("SELECT * FROM Voca")
        rows = self.Cursor.fetchall()

        print(rows)
        # row 만큼 위젯을 만듬
        for i in rows:
            print(i)

class create_voca_widget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__()
        
        self.setStyleSheet("""
            #first-frame {
                background-color : red;    
            }
            #second-frame {
                background-color : green;               
            }
            #third-left-frame {
                background-color : blue;   
            }
            #third-right-frame {
                background-color : orange;        
            }
            #fourth-frame {
                background-color : purple;
            }
        """)

        self.db = db
        self.Parent = parent
        self.voca_name = 0
        self.name_submit_enable = True
        self.chapter_submit_enable = True

        self.setFixedSize(300,400)
        self.setObjectName("window")

        first_frame = QFrame(self)
        first_frame.setFixedSize(300,80)
        first_frame.setObjectName("first-frame")

        second_frame = QFrame(self)
        second_frame.setFixedSize(300,40)
        second_frame.setObjectName("second-frame")

        third_left_frame = QFrame(self)
        third_left_frame.setFixedSize(100,20)
        third_left_frame.setObjectName("third-left-frame")
        row_chapter = QLabel("chapters", third_left_frame)

        third_right_frame = QFrame(self)
        third_right_frame.setFixedSize(200,20)
        third_right_frame.setObjectName("third-right-frame")
        row_words = QLabel("words", third_right_frame)

        self.fourth_frame = QScrollArea(self)
        self.fourth_frame.setWidgetResizable(True)
        self.fourth_frame.setFixedSize(300,260)
        self.fourth_frame.setObjectName("fourth-frame")
        self.fourth_frame.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


        self.container_widget = QWidget()
        self.fourth_frame.setWidget(self.container_widget)

        self.voca_name_field = QLineEdit(first_frame)
        self.voca_name_field.setPlaceholderText("name of Vocabulary")
        self.voca_name_field.returnPressed.connect(self.save_voca_name)
        self.voca_name_field.setFixedSize(200,40)
        self.voca_name_field.setObjectName("voca-name")

        submit_voca_name = QPushButton("save", first_frame)
        submit_voca_name.setFixedSize(100,30)
        submit_voca_name.setObjectName("submit")

        self.voca_chapter_field = QLineEdit(second_frame)
        self.voca_chapter_field.setPlaceholderText("name of Chapter")
        self.voca_chapter_field.setFixedSize(170,30)

        submit_voca_chapter = QPushButton("add chapter", second_frame)
        submit_voca_chapter.clicked.connect(lambda:[self.add_chapter(self.voca_chapter_field.text())])
        submit_voca_chapter.setFixedSize(100,30)
        submit_voca_chapter.setObjectName("submit")



        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setSpacing(10)
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container_layout.setAlignment(Qt.AlignTop)

        name_field_widgets = QHBoxLayout(first_frame)
        name_field_widgets.addWidget(self.voca_name_field)
        name_field_widgets.addWidget(submit_voca_name)
        name_field_widgets.setContentsMargins(0,0,0,0)

        chapter_field_widgets = QHBoxLayout(second_frame)
        chapter_field_widgets.addWidget(self.voca_chapter_field)
        chapter_field_widgets.addWidget(submit_voca_chapter)
        chapter_field_widgets.setContentsMargins(0,0,0,0)

        display_frame = QHBoxLayout()
        display_frame.addWidget(third_left_frame)
        display_frame.addWidget(third_right_frame)
        display_frame.setContentsMargins(0,0,0,0)

        Main_layout = QVBoxLayout(self)
        Main_layout.addWidget(first_frame)
        Main_layout.addWidget(second_frame)
        Main_layout.addLayout(display_frame)
        Main_layout.addWidget(self.fourth_frame)

        Main_layout.setContentsMargins(0,0,0,0)
        Main_layout.setSpacing(0)

        self.setLayout(Main_layout)


    def closeEvent(self, event):
        self.Parent.setEnabled(True)   
        event.accept()


    def save_voca_name(self):
        pass

    def add_chapter(self, name):
        self.name = name
        
        test_frame = QFrame()
        test_frame.setFixedSize(280,60)
        test_frame.setStyleSheet("background-color : yellow;")

        test_label = QLabel(self.name, test_frame)
        test_label.setFixedSize(50,30)
        test_label.setStyleSheet("background-color : pink;")

        test_line = QLineEdit(test_frame)
        test_line.setFixedSize(220,30)
        test_line.setStyleSheet("background-color : blue;")

        test_layout = QHBoxLayout()
        test_layout.addWidget(test_label)
        test_layout.addWidget(test_line)

        test_layout.setContentsMargins(0,0,0,0)
        test_frame.setLayout(test_layout)

        self.container_layout.addWidget(test_frame)


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