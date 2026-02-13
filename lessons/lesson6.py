#                                     --------CRUD - 2 ч. Поиск. Удаление.--------
import sqlite3

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    genre TEXT,
    year TEXT
)
''')

conn.commit()

def add_game():
    title = input(" Название игры: ")
    genre = input(" Жанр игры: ")
    year = input("Год: ")

    cursor.execute(
        "INSERT INTO games (title, genre, year) VALUES (?, ?, ?)",
        (title, genre, year)
    )
    

conn.commit()
print(" Игра добавлена!")

def show_games():
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()

    print('\nСписок игр:')
    for game in games:
        print(game)

def search_games():
    name = input("Введите название игры для поиска: ")

    cursor.execute(
        'SELECT * FROM games WHERE title LIKE ?',
        ('%' + name + '%',)
    )
    
    results = cursor.fetchall()

    if results:
        print("\nНайдено:")
        for game in results:
            print(game)

def delete_game():
    game_id = input("Введите ID игры для удаления: ")

    cursor.execute(
        'DELETE FROM games WHERE id = ?',
        (game_id,)
    )
    
    conn.commit()
    print(" Игра удалена!")


def update_game():
    game_id = input("Введите ID игры для изменение: ")
    new_title = input("Новое название игры: ")
    new_genre = input("Новый жанр игры: ")
    new_year = input("Новый год: ")

    cursor.execute(
        'UPDATE games SET title = ?, genre = ?, year = ? WHERE id = ?',
        (new_title, new_genre, new_year, game_id)
    )
    
    conn.commit()
    print(" Игра обновлена!")

def menu():
    while True:
        print("\n--------МЕНЮ--------")
        print("1. Добавить игру")
        print("2. Показать все игры")
        print("3. Поиск игры")
        print("4. Удалить игру")
        print("5. Изменить игру")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            add_game()
        elif choice == '2':
            show_games()
        elif choice == '3':
            search_games()
        elif choice == '4':
            delete_game()
        elif choice == '5':
            update_game()
        elif choice == '6':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

menu()
conn.close()