import sys
import psycopg2
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QListWidget
)

conn = psycopg2.connect(
    host="localhost",
    database="db_hw8",
    port=5432,
    user="postgres",
    password="445415"
)

cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL
)
''')
conn.commit()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.resize(400, 300)

        self.layout = QVBoxLayout()

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Введите заметку")

        self.add_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")

        self.notes_list = QListWidget()
        self.count_label = QLabel("Заметок: 0")

        self.layout.addWidget(self.note_input)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.delete_btn)
        self.layout.addWidget(self.notes_list)
        self.layout.addWidget(self.count_label)

        self.setLayout(self.layout)
        self.add_btn.clicked.connect(self.add_note)
        self.delete_btn.clicked.connect(self.delete_note)
        self.load_notes()

    def add_note(self):
        note_text = self.note_input.text().strip()
        if note_text:
            cur.execute("INSERT INTO notes (text) VALUES (%s)", (note_text,))
            conn.commit()
            self.note_input.clear()
            self.load_notes()

    def delete_note(self):
        selected_items = self.notes_list.selectedItems()
        if not selected_items:
            return

        item_text = selected_items[0].text()
        note_id_to_delete = item_text.split(" | ")[0]
        cur.execute("DELETE FROM notes WHERE id = %s", (note_id_to_delete,))

        cur.execute("SELECT text FROM notes ORDER BY id")

        remaining_notes = cur.fetchall()
        cur.execute("TRUNCATE TABLE notes RESTART IDENTITY")

        if remaining_notes:
            cur.executemany("INSERT INTO notes (text) VALUES (%s)", remaining_notes)
        conn.commit()
        self.load_notes()

    def load_notes(self):
        self.notes_list.clear()
        cur.execute("SELECT id, text FROM notes ORDER BY id")
        for row in cur.fetchall():
            self.notes_list.addItem(f"{row[0]} | {row[1]}")
        self.update_status()

    def update_status(self):
        cur.execute("SELECT COUNT(*) FROM notes")
        count = cur.fetchone()[0]
        self.count_label.setText(f"Заметок: {count}")

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())

conn.close()