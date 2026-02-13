class Logic:  # Класс для обработки бизнес-логики приложения
    def __init__(self, ui):  # Конструктор принимает объект интерфейса (ui)
        self.ui = ui  # Сохраняем ссылку на объект интерфейса
        self.connect_signals()  # Вызываем метод подключения сигналов (событий)

    def connect_signals(self):  # Метод для связывания кнопок с функциями
        self.ui.hello_button.clicked.connect(self.say_hello)  # При клике на hello_button запускаем say_hello
        self.ui.clear_button.clicked.connect(self.clear)  # При клике на clear_button запускаем clear

    def say_hello(self):  # Функция приветствия
        name = self.ui.input_name.text()  # Получаем текст из поля ввода имени
    
        if name:  # Проверяем, не пустое ли имя
            self.ui.result_label.setText(f'Привет, {name}!')  # Если имя есть, выводим приветствие
        else:  # Если поле пустое
            self.ui.result_label.setText('Пожалуйста, введите ваше имя.')  # Просим ввести имя

    def clear(self):  # Функция очистки
        self.ui.input_name.clear()  # Очищаем поле ввода имени
        self.ui.result_label.clear()  # Очищаем метку с результатом