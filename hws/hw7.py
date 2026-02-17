import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QCheckBox,
    QAbstractItemView
)
from PyQt6.QtCore import Qt

DB_NAME = "shopping.db"


class ShoppingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список покупок")
        self.conn = sqlite3.connect(DB_NAME)
        self.create_table()
        self.init_ui()
        self.load_data()
        self.update_status()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL,
           qty INT,
           category TEXT,
           priority TEXT,
           bought INT DEFAULT 0,
           created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 69)
        self.qty_input.setValue(1)

        self.category_input = QComboBox()
        self.category_input.addItems(["Овощи", "Молочные", "Бытовое", "Другое"])

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Низкий", "Средний", "Высокий"])

        form_layout.addWidget(QLabel("Название"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Количество"))
        form_layout.addWidget(self.qty_input)
        form_layout.addWidget(QLabel("Категория"))
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(QLabel("Приоритет"))
        form_layout.addWidget(self.priority_input)

        layout.addLayout(form_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название", "Кол-во", "Категория", "Приоритет", "Куплено"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.update_btn = QPushButton("Обновить")
        self.delete_btn = QPushButton("Удалить")
        self.toggle_btn = QPushButton("Отметить купленным")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.toggle_btn)

        layout.addLayout(btn_layout)

        central.setLayout(layout)
        self.statusBar()

        self.add_btn.clicked.connect(self.add_item)
        self.update_btn.clicked.connect(self.update_item)
        self.delete_btn.clicked.connect(self.delete_item)
        self.toggle_btn.clicked.connect(self.toggle_bought)
        self.table.cellClicked.connect(self.fill_form)

    def add_item(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым")
            return

        qty = self.qty_input.value()
        category = self.category_input.currentText()
        priority = self.priority_input.currentText()

        self.conn.execute(
            "INSERT INTO items (name, qty, category, priority) VALUES (?, ?, ?, ?)",
            (name, qty, category, priority)
        )
        self.conn.commit()
        self.load_data()
        self.update_status()
        self.name_input.clear()
        self.qty_input.setValue(1)

    def update_item(self):
        row = self.table.currentRow()
        if row < 0:
            return

        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым")
            return

        item_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        qty = self.qty_input.value()
        category = self.category_input.currentText()
        priority = self.priority_input.currentText()

        self.conn.execute(
            "UPDATE items SET name=?, qty=?, category=?, priority=? WHERE id=?",
            (name, qty, category, priority, item_id)
        )
        self.conn.commit()
        self.load_data()
        self.update_status()

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            return

        item_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        self.conn.commit()
        self.load_data()
        self.update_status()

    def toggle_bought(self):
        row = self.table.currentRow()
        if row < 0:
            return

        item_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        bought = self.conn.execute(
            "SELECT bought FROM items WHERE id=?", (item_id,)
        ).fetchone()[0]

        new_value = 0 if bought else 1

        self.conn.execute(
            "UPDATE items SET bought=? WHERE id=?",
            (new_value, item_id)
        )
        self.conn.commit()
        self.load_data()
        self.update_status()

    def load_data(self):
        self.table.setRowCount(0)
        cursor = self.conn.execute(
            "SELECT id, name, qty, category, priority, bought FROM items ORDER BY created_at DESC"
        )

        for row_data in cursor:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)

            id_, name, qty, category, priority, bought = row_data

            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.ItemDataRole.UserRole, id_)
            self.table.setItem(row_number, 0, name_item)
            self.table.setItem(row_number, 1, QTableWidgetItem(str(qty)))
            self.table.setItem(row_number, 2, QTableWidgetItem(category))
            self.table.setItem(row_number, 3, QTableWidgetItem(priority))

            checkbox = QCheckBox()
            checkbox.setChecked(bool(bought))
            checkbox.setEnabled(False)
            self.table.setCellWidget(row_number, 4, checkbox)

    def fill_form(self, row, column):
        self.name_input.setText(self.table.item(row, 0).text())
        self.qty_input.setValue(int(self.table.item(row, 1).text()))
        self.category_input.setCurrentText(self.table.item(row, 2).text())
        self.priority_input.setCurrentText(self.table.item(row, 3).text())

    def update_status(self):
        total = self.conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        bought = self.conn.execute("SELECT COUNT(*) FROM items WHERE bought=1").fetchone()[0]
        self.statusBar().showMessage(
            f"Всего: {total} | Куплено: {bought} | Осталось: {total - bought}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoppingApp()
    window.resize(900, 400)
    window.show()
    sys.exit(app.exec())