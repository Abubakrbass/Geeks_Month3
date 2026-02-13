import sys
import sqlite3
from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QMessageBox
)

def connect_db():
    return sqlite3.connect("Peoples.database")

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peoples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def create_people(name, age):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO peoples (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

def show_all():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM peoples")
    data = cursor.fetchall()
    conn.close()
    return data

def delete_people(people_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peoples WHERE id = ?", (people_id,))
    
    cursor.execute("SELECT COUNT(*) FROM peoples")
    if cursor.fetchone()[0] == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='peoples'")
        
    conn.commit()
    conn.close()

def update_people(people_id, name, age):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE peoples SET name = ?, age = ? WHERE id = ?", (name, age, people_id))
    conn.commit()
    conn.close()

class PeopleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DZ 6')
        self.resize(600, 300)
        self.init_ui()
        self.refresh_people_list()

    def init_ui(self):
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")


        self.add_btn = QPushButton("Добавить")
        self.show_btn = QPushButton("Показать всех")
        self.update_btn = QPushButton("Изменить")
        self.delete_btn = QPushButton("Удалить")

        self.add_btn.clicked.connect(self.add_people)
        self.show_btn.clicked.connect(self.show_all_people)
        self.update_btn.clicked.connect(self.update_people)
        self.delete_btn.clicked.connect(self.delete_people)

        self.list_widget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.id_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.show_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def add_people(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()

        if not name or not age:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return

        create_people(name, int(age))
        self.refresh_people_list()

    def show_all_people(self):
        self.refresh_people_list()

    def refresh_people_list(self):
        self.list_widget.clear()
        people = show_all()
        for person in people:
            self.list_widget.addItem(f"{person[0]}: {person[1]} ({person[2]} лет)")

    def delete_people(self):
        people_id = self.id_input.text().strip()
        if not people_id.isdigit():
            QMessageBox.warning(self, "Ошибка", "ID должен быть числом")
            return

        delete_people(int(people_id))
        self.refresh_people_list()

    def update_people(self):
        people_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()

        if not people_id.isdigit() or not name or not age:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля и убедитесь, что ID - число")
            return

        update_people(int(people_id), name, int(age))
        self.refresh_people_list()

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = PeopleApp()
    window.show()
    sys.exit(app.exec())