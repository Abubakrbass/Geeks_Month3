import sys, json, urllib.request, urllib.parse, ssl, time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QDoubleSpinBox, QPushButton, QMessageBox
)

from PyQt6.QtCore import Qt

ssl._create_default_https_context = ssl._create_unverified_context

currencies = ['USD', 'EUR', 'KGS', 'KZT', 'UZB', 'RUB', 'CNY']

API_MAIN = "https://api.exchangerate-api.com/v4/latest"
API_BACKUP = 'https://api.exchangerate-api.com/v4/latest'

class CurrencyAPI():
    def __init__(self):
        self.cashe = {}
        self.cashe_time = 60

    def fetch_json(self, url):
        with urllib.request.urlopen(url, timeout=8) as r:
            return json.loads(r.read().decode('utf-8'))
        
    def get_rate(self, src, dst, amount):
        key = f'{src}_{dst}'

        if key in self.cashe:
            rate, timestamp = self.cashe[key]
            if time.time() - timestamp < self.cashe_time:
                return rate * amount
        
        try:
            url = f"{API_MAIN}/{src}"
            data = self.fetch_json(url)
            rate = data.get('rates', {}).get(dst)
            
            if rate:
                self.cashe[key] = (rate, time.time())
                return rate * amount

        except:
            pass
        
        raise ValueError('Курс не найден.')
    
    


    
class Converter(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Конвертер валют")
        self.resize(420, 220)

        self.api = CurrencyAPI()

        
        input_layout = QHBoxLayout()
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.0, 1e9)
        self.amount_input.setDecimals(2)
        self.amount_input.setValue(100.0)

        self.src_currency = QComboBox()
        self.src_currency.addItems(currencies)

        self.from_cb = QComboBox()
        self.to_cb = QComboBox()

        self.from_cb.addItems(currencies)
        self.to_cb.addItems(currencies)

        self.from_cb.setCurrentText("USD")
        self.to_cb.setCurrentText("KGS")

        self.result = QLabel("-")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin-top: 10px;"
            )
        
        convert_btn = QPushButton("Конвертировать")
        convert_btn.clicked.connect(self.convert)

        swap_btn = QPushButton("Поменять")
        swap_btn.clicked.connect(self.swap_currencies)

        self.amount_input.returnPressed.connect(self.convert)


        layout = QVBoxLayout()

        for text, widget in [
            ("Сумма:", self.amount_input),
            ("Из:", self.from_cb),
            ("В:", self.to_cb)
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel(text))
            row.addWidget(widget)
            layout.addLayout(row)

        
        btn_row = QHBoxLayout()
        btn_row.addWidget(convert_btn)
        btn_row.addWidget(swap_btn)

        layout.addLayout(btn_row)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def swap_currencies(self):
        src = self.from_cb.currentText()
        dst = self.to_cb.currentText()
        self.from_cb.setCurrentText(dst)
        self.to_cb.setCurrentText(src)
        

    def convert(self):
        amount = self.amount_input.value()
        src = self.from_cb.currentText()
        dst = self.to_cb.currentText()

        if src == dst:
            self.result.setText(f"{amount:.2f} {src}")
            self.result.setStyleSheet('font-size: 18px; color: green;')
            return
        
        try:
            result = self.api.get_rate(src, dst, amount)
            self.result.setText(f"{result:.2f} {src} = {result:.2f} {dst}")
            self.result.setStyleSheet('font-size: 18px; color: green;')

        except Exception as e:
            self.result.setText("Ошибка при конвертации.")
            self.result.setStyleSheet('font-size: 18px; color: red;')
            QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = Converter()
    converter.show()
    sys.exit(app.exec())