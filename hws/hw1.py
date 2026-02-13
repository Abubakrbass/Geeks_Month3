import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("DZ2. Приветствие пользователя")
        self.resize(400, 200)

       
        self.label = QLabel("Введите имя:")
        self.input = QLineEdit()
        self.button = QPushButton("Нажмите что бы получить приветствие")

        
        self.button.clicked.connect(self.show_greeting)

        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_greeting(self):
        name = self.input.text().strip()

        if not name:
            self.label.setText("Введите имя:")
            return

        self.label.setText(f"Привет, {name}!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
