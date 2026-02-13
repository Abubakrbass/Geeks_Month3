import sys  # Импортируем модуль sys для работы с системными параметрами и аргументами
from PyQt6.QtWidgets import QApplication, QMainWindow  # Импортируем основные классы для приложения

from ui import MainUI  # Импортируем наш класс интерфейса из файла ui.py
from logic import Logic  # Импортируем наш класс логики из файла logic.py
import config  # Импортируем файл конфигурации

def main():  # Главная функция запуска приложения
    app = QApplication(sys.argv)  # Создаем объект приложения, передавая аргументы командной строки

    window = MainUI()  # Создаем экземпляр нашего окна интерфейса
    window.setWindowTitle(config.APP_TITLE)  # Устанавливаем заголовок окна из конфига
    window.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)  # Устанавливаем размеры окна из конфига
    window.show()  # Отображаем окно на экране

    logic = Logic(window)  # Инициализируем логику, передавая ей созданное окно

    sys.exit(app.exec())  # Запускаем цикл обработки событий приложения и корректно завершаем при выходе

if __name__ == '__main__':  # Проверяем, запущен ли файл напрямую (а не импортирован)
    main()  # Вызываем главную функцию
