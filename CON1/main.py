import sys 
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QListWidget
)
import sqlite3

def connect_db():
    return sqlite3.connect('Work.db')

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Задачи')
        self.resize(400, 300)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('Введите задачу')

        self.add_button = QPushButton('Добавить задачу')
        self.add_button.clicked.connect(self.add_task)

        self.delete_btn = QPushButton('Удалить задачу')
        self.delete_btn.clicked.connect(self.delete_task)

        self.task_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_list)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.load_tasks()
        self.show()

    def add_task(self):
        text = self.task_input.text()
        if text:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (text) VALUES (?)', (text,))
            conn.commit()
            conn.close()
            self.task_input.clear()
            self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT text FROM tasks')
        tasks = cursor.fetchall()
        conn.close()
        for task in tasks:
            self.task_list.addItem(task[0])

    def delete_task(self):
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (current_row + 1,))
            conn.commit()
            conn.close()
            self.load_tasks()

init_db()

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())