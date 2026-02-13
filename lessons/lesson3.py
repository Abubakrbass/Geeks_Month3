import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox

)

from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt6: Calculator')
        self.resize(450, 320)

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.title_label = QLabel('Анкета пользователя')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet('font-size: 18px; font-weight: bold;')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите ваше имя')

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText('Введите ваш возраст')

        self.language_box = QComboBox()
        self.language_box.addItems(['Python', 'C++', 'Java', 'JavaScript', 'Ruby'])

        self.is_student_checkbox = QComboBox('Я студент')
        
        self.submit_button = QPushButton('Отправить')
        self.clear_button = QPushButton('Очистить')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.clear_button)
