from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout
)  # Импортируем необходимые виджеты и макеты из библиотеки PyQt6

class MainUI(QWidget):  # Создаем класс MainUI, который наследуется от QWidget
    def __init__(self):  # Конструктор класса
        super().__init__()  # Вызываем конструктор родительского класса QWidget

        self.label = QLabel('Введите ваше имя:')  # Создаем текстовую метку
        self.input_name = QLineEdit()  # Создаем поле для ввода текста
        self.input_name.setPlaceholderText('Ваше имя')  # Устанавливаем подсказку внутри поля ввода
        self.button = QPushButton('Нажми меня')  # Создаем кнопку (в данном коде не используется в layout)

        self.hello_button = QPushButton('Приветствие')  # Создаем кнопку "Приветствие"
        self.clear_button = QPushButton('Очистить')  # Создаем кнопку "Очистить"

        self.result_label = QLabel('')  # Создаем пустую метку для вывода результата

        button_layout = QHBoxLayout()  # Создаем горизонтальный макет для кнопок
        button_layout.addWidget(self.hello_button)  # Добавляем кнопку приветствия в горизонтальный макет
        button_layout.addWidget(self.clear_button)  # Добавляем кнопку очистки в горизонтальный макет

        main_layout = QVBoxLayout()  # Создаем основной вертикальный макет
        main_layout.addWidget(self.label)  # Добавляем метку "Введите ваше имя" сверху
        main_layout.addWidget(self.input_name)  # Добавляем поле ввода под меткой
        main_layout.addLayout(button_layout)  # Добавляем горизонтальный макет с кнопками
        main_layout.addWidget(self.result_label)  # Добавляем метку результата в самый низ

        self.setLayout(main_layout)  # Устанавливаем созданный вертикальный макет как основной для этого окна