from PyQt5.QtWidgets import QWidget,QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QFrame, QHBoxLayout, QScrollArea, QStackedWidget, QComboBox
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
import random
import sys
import os 
import sqlite3


try:
    name = "Girl.db"
    if os.path.isfile(name): # 데이터베이스가 존재함
        conn = sqlite3.connect(name) # 연결
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(main);")
        columns = cursor.fetchall()

        example_column = ["voca", "id", "data"]
        column = [i[1] for i in columns]

        if len(column) == 3 and sorted(column) == sorted(example_column): # 컬럼의 개수가 3개고 컬럼이 같음
            pass
        else: # 위 조건에 해당되지 않음.
            raise Exception
        
    else: # 데이터베이스가 존재하지 않음

        conn = sqlite3.connect(name) # 생성
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS main (
                id INTEGER PRIMARY KEY,
                voca TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        # 다음과 같음 ... |id|voca|data|

        print("db가 생성됌.")
except Exception:
    print("데이터가 손상되었거나 온전하지 못합니다, 따라서 삭제합니다. \n")
    os.remove("Girl.db")

    if not os.path.exists(name):
        print("방금 삭제 됌 \n다시 시작해주세요.")
    
    else: #제거가 되지 않음
        print(f"{name} 가 삭제되지 않았습니다, 직접 삭제해주세요.")
  
    os._exit(0)

finally: # db가 반드시 존재한다는 전제가 있음.
    conn.close()


class setting_voca(QWidget):
    def __init__(self):
        super().__init__()
        self.container_in_widget_name = []

        self.setFixedSize(300,400)
        
        self.stack = QStackedWidget()

        # ------------ * ------------
        submit_name_widget = QWidget()

        submit_name_button = QPushButton("wata", submit_name_widget)
        submit_name_button.clicked.connect(self.was_submited_name)
        
        self.name_field = QLineEdit(submit_name_widget)

        submit_widget_layout = QVBoxLayout()

        submit_widget_layout.addWidget(self.name_field)
        submit_widget_layout.addWidget(submit_name_button)

        submit_name_widget.setLayout(submit_widget_layout)

        # ------------ * ------------

        chapter_widget = QWidget()

        #  버튼 프레임
        button_frame = QFrame()

        # 제작 버튼
        create_chapter_button = QPushButton("create", button_frame)
        create_chapter_button.clicked.connect(lambda: self.container_logic("add"))

        # 스크롤 
        scroll_widget = QScrollArea(chapter_widget)

        # 스크롤 안에 들어갈 컨테이너 프레임
        self.container_frame = QFrame()
        self.container_frame.setFixedSize(0,0)

        # 스크롤에 컨테이너 위젯 추가
        scroll_widget.setWidget(self.container_frame)

        # 컨테이너 프레임 레이아웃
        self.container_layout = QVBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_frame.setLayout(self.container_layout)

        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.addWidget(create_chapter_button)

        chapter_widget_layout = QVBoxLayout()
        chapter_widget_layout.setContentsMargins(0,0,0,0)
        chapter_widget_layout.addWidget(button_frame)
        chapter_widget_layout.addWidget(scroll_widget)

        chapter_widget.setLayout(chapter_widget_layout)

        # ------------ * ------------

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.stack)

        self.stack.addWidget(submit_name_widget)
        self.stack.addWidget(chapter_widget)
        self.stack.setCurrentIndex(0)

    def container_logic(self, action, name=None):
        try:
            if action == "add":
                self.add_widget()
                return

            elif action == "remove":
                self.remove_widget(name)
                return
            
            else:
                raise e("잘못된 매개변수")
            
        except Exception as e:
            print(f"{e}, 더 이상 진행을 못하기에 종료합니다.")
            sys.exit()


    def add_widget(self):
        object_name = self.set_object_name()

        if object_name is None:
            return

        main_frame = QFrame()
        main_frame.setObjectName(str(object_name))

        remove_button = QPushButton("remove", main_frame)
        remove_button.clicked.connect(lambda : self.container_logic("remove", object_name))

        name_label = QLabel("", main_frame)
        name_label.setObjectName(f"{object_name}_label")
        clicked_event_label = QLabel("edit", main_frame)

        clicked_event_label.mousePressEvent = lambda event: self.write_words(object_name)

        Hbox = QHBoxLayout()
        Hbox.addWidget(name_label)
        Hbox.addWidget(clicked_event_label)

        main_layout = QVBoxLayout()
        main_layout.addWidget(remove_button)
        main_layout.addLayout(Hbox)

        main_frame.setLayout(main_layout)

        self.container_in_widget_name.append(object_name)

        self.resize_container()

        self.container_layout.addWidget(main_frame)

    def write_words(self, object_name):
        self.chapter_name = 0
        self.location_in_list = 0
        self.words = []
        self.means = []

        self.frame = QWidget()
        self.frame.setFixedSize(300,400)
        self.frame.setWindowTitle(str(object_name))
        self.frame.show()

        main_widget_layout = QVBoxLayout()

        go_back_button = QPushButton("<", self.frame)
        go_back_button.clicked.connect(lambda : self.step_navigation("back"))

        go_button = QPushButton(">", self.frame)
        go_button.clicked.connect(lambda : self.step_navigation("go"))

        self.save_chapter_contents = QPushButton("save", self.frame)
        self.save_chapter_contents.clicked.connect(self.save_chapter)

        go_and_back_buttons_layout = QHBoxLayout()
        go_and_back_buttons_layout.addWidget(go_back_button)
        go_and_back_buttons_layout.addWidget(go_button)

        self.word_field = QLineEdit(self.frame)
        self.word_mean_field = QLineEdit(self.frame)

        self.disaply_message = QLabel("",self.frame)

        chapter_name_signs = QLabel("field", self.frame)

        self.chapter_name_field = QLineEdit(self.frame)
        self.chapter_name_field.returnPressed.connect(lambda: self.fix_chapter_name(object_name))

        chapter_widget_layout = QHBoxLayout()
        
        chapter_widget_layout.addWidget(chapter_name_signs)
        chapter_widget_layout.addWidget(self.chapter_name_field)

        add_button = QPushButton("add", self.frame)
        add_button.clicked.connect(lambda: self.submit_logic("add"))

        update_button = QPushButton("Update", self.frame)
        update_button.clicked.connect(lambda: self.submit_logic("update"))

        delete_button = QPushButton("delete", self.frame)
        delete_button.clicked.connect(lambda: self.dropbox_logic("delete"))

        self.word_combo_box = QComboBox()
        self.word_combo_box.addItem("select")
        self.word_combo_box.currentIndexChanged.connect(lambda: self.dropbox_logic("move"))

        submit_buttons = QHBoxLayout()
        submit_buttons.addWidget(add_button)
        submit_buttons.addWidget(update_button)
        submit_buttons.addWidget(delete_button)


        main_widget_layout.addLayout(chapter_widget_layout)
        main_widget_layout.addWidget(self.disaply_message)
        main_widget_layout.addWidget(self.word_combo_box)
        main_widget_layout.addWidget(self.save_chapter_contents)
        main_widget_layout.addLayout(go_and_back_buttons_layout)
        main_widget_layout.addWidget(self.word_field)
        main_widget_layout.addWidget(self.word_mean_field)
        main_widget_layout.addLayout(submit_buttons)

        self.frame.setLayout(main_widget_layout)

        QTimer.singleShot(500, lambda: self.write_to_display_label("changed"))

    def save_chapter(self, event):
        print(self.words, self.means, self.chapter_name)

        

    def dropbox_logic(self, request):
        if request == "add":
            if not len(self.words) == self.location_in_list: # ex) 5쪽 중 5쪽이 아님을 의미함
                self.word_combo_box.addItem(f"{len(self.words)}. {self.words[len(self.words)-1]}")
            else:  # ex) 5쪽 중 5쪽을 의미함
                self.word_combo_box.addItem(f"{self.location_in_list}. {self.words[self.location_in_list-1]}")


        else:
            index = self.word_combo_box.currentIndex()
            print(f"index is {index}")

            if not index == 0:
                if request == "delete":
                    """중복된 값이면 순번이 옳지 않은 문제 해결하기"""
                    self.words.pop(index-1)
                    self.means.pop(index-1)

                    self.word_combo_box.clear() # 이후에 move로 함수가 다시 실행이 됌 그때의 index는 -1임

                    self.word_combo_box.addItem("select")
                    if not len(self.words) == 0: # 빈 리스트가 아님을 의미
                        for item in self.words:
                            self.word_combo_box.addItem(f"{self.words.index(item)+1}. {item}")
                
                elif request == "move":
                    if not index == -1:
                        self.location_in_list = index
                        self.write_field()
                    
                elif request == "changed":
                    self.word_combo_box.setItemText(self.location_in_list,f"{self.location_in_list}. {self.words[self.location_in_list-1]}")
                else:
                    raise Exception("원치 않는 매개변수 발생")
                


    def fix_chapter_name(self, object_name):
        mother_field = self.findChild(QLabel, f"{object_name}_label")

        mother_text = mother_field.text().strip()
        text = self.chapter_name_field.text().strip()


        if text.isalpha():
            if not mother_field:
                raise Exception("위젯을 찾지 못했습니다.")
            
            self.chapter_name = text
            
            mother_field.setText(text)

        else:
            self.chapter_name_field.clear()  
            self.chapter_name_field.setText(mother_text)      
            print("nope")

    def submit_logic(self, request):
        word = self.word_field.text().strip()
        mean = self.word_mean_field.text().strip()

        if word.isalpha() and mean.isalpha():
            if request == "update": # 수정을 할려면 최소의 요소인 1을 가지고 있어야함
                if self.location_in_list > 0:
                    print("before", self.words, self.means)

                    self.words[self.location_in_list-1] = word   
                    self.means[self.location_in_list-1] = mean

                    self.dropbox_logic("changed")

                    self.write_to_display_label("update")


                    print("after", self.words, self.means)

                    return # 필드가 clean 당하지 않기를 위함
        
            elif request == "add":
                
                self.words.append(word)
                self.means.append(mean)

                self.location_in_list += 1

                self.dropbox_logic("add")
                

                print(self.words, self.means)

            else:
                raise Exception("비정상적인 매개변수 들어옴")

            self.word_field.clear()
            self.word_mean_field.clear()


    def step_navigation(self, step):
        if step == "back":
            if len(self.words) > 1:
                if not self.location_in_list == 1:
                    print(f"before location is {self.location_in_list} \n")
                    self.location_in_list -= 1
                    print(f"after is {self.location_in_list} .. was subed")
                    self.write_field()

                else: 
                    self.write_to_display_label("min")
            else: 
                self.write_to_display_label("small")


        elif step == "go":
            if len(self.words) > self.location_in_list:
                print(f"before location is {self.location_in_list} \n")
                self.location_in_list += 1
                print(f"after is {self.location_in_list} .. was added")
                self.write_field()
            else:
                self.write_to_display_label("max")

        


        else:
            raise Exception("잘못된 매개변수가 들어옴.")
    
        print(f"location is {self.location_in_list}")
        
    def write_to_display_label(self, request):
            if request != "changed":
                if request == "max":
                    self.disaply_message.setText("max")
                elif request == "small":
                    self.disaply_message.setText(f"cute size")
                elif request == "min":
                    self.disaply_message.setText("min")
                elif request == "update":
                    self.disaply_message.setText("You have just changed")

                QTimer.singleShot(2000, lambda : self.write_to_display_label("changed"))

            else:   

                self.disaply_message.setText(f"{len(self.words)}/{self.location_in_list}")


    def write_field(self):
        #if not self.location_in_list == -1:
            word , mean = self.words[self.location_in_list -1], self.means[self.location_in_list -1]
            print(self.words, self.means)

            self.word_field.clear()
            self.word_mean_field.clear()

            self.word_field.setText(word)
            self.word_mean_field.setText(mean)

            self.write_to_display_label("changed")


    def remove_widget(self, name):
        frame = self.container_frame.findChild(QFrame, str(name))
        
        frame.deleteLater()
        self.container_in_widget_name.remove(name)

        self.resize_container()
        
    def resize_container(self):
        constant = len(self.container_in_widget_name)

        self.container_frame.setFixedSize(280, constant*400 + 100)


    def set_object_name(self):
        object_name = random.randint(0,50)

        if not object_name in self.container_in_widget_name: # 리스트에 해당 값이 없다면
            return object_name

    def was_submited_name(self,event):

            self.name = 0
            text = self.name_field.text().strip()

            if text.isalpha():
                self.name = text # 이름 저장
                self.stack.setCurrentIndex(1)

            else: # 이름이 알파밧에 아님
                pass


    def name_field_locker(self, lock, content=None):
        try:
            self.name_field.clear()

            if lock is True: # 네임필드를 잠금
                self.name_field.setReadOnly(True)

            elif lock is False: # 네임필드 잠금 해체
                self.name_field.setReadOnly(False)

            else: # 매개변수를 잘못씀
                raise Exception("잘못된 매개변수가 들어왔음")
            
            if not content is None: # 필드에 기재할 내용이 있다면
                self.name_field.setPlaceholderText(content)
            
        except Exception as e:
            print(f"{e}, 더 이상 진행이 안됩니다. \n따라서 종료합니다.")
            sys.exit()
    
app = QApplication(sys.argv)
window = setting_voca()

window.show()

app.exec_()