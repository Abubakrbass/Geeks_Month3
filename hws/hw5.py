import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QListWidget
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List by Geeks")
        self.resize(400, 300)
        self.init_ui()

    def init_ui(self):
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите задачу")

        self.add_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")

        self.add_btn.clicked.connect(self.add_task)
        self.delete_btn.clicked.connect(self.delete_task)

        self.list_widget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Список задач"))
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            self.list_widget.addItem(task)
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Введите задачу!")

    def delete_task(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления!")
            return
        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())