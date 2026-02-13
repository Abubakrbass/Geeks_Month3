#                  --------Десктопные приложения 1 ч.  Знакомство PyQt6. Понятия Декомпозиция.---------
# import sys
# from PyQt6.QtWidgets import (
#     QApplication,
#     QWidget,
#     QVBoxLayout,
#     QPushButton,
#     QLabel,
#     QLineEdit
# )

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle('PyQt6: Widgets')
#         self.resize(400, 300)

#         self.label = QLabel('Введите ваше имя:')
#         self.input_name = QLineEdit()
#         self.button = QPushButton('Нажми меня')
#         self.button.clicked.connect(self.on_click)

#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.input_name)
#         layout.addWidget(self.button)

#         self.setLayout(layout)

#     def on_click(self):
#         name = self.input_name.text()
#         self.label.setText(f'Привет, {name}!')
    
# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()

# sys.exit(app.exec())