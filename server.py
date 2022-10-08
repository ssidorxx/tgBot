import sqlite3
connect = sqlite3.connect('bdForUP.db')

cursor = connect.cursor()

# Создание таблиц
cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"login"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS "category" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS "subscription" (
	"id_user"	INTEGER NOT NULL,
	"id_category"	INTEGER NOT NULL
);""")

# Функция для регистрации
def reg(u_login):
    cursor.execute(f"SELECT login FROM users WHERE login={u_login}")
    # connect.commit()

    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users (login) VALUES({u_login})")
        connect.commit()
        return ("Вы успешно зарегистрировались! ")
    else:
        return ("Пользователь с таким логином уже существует")

# reg('12345')
#
# # Функция для аутентификации
# def auth(u_login, u_password):
#     cursor.execute(f"SELECT login, password FROM users WHERE login = '{u_login}' AND password = '{u_password}'")
#     connect.commit()
#
#     if (cursor.fetchall() == []):
#         print("Неверный логин или пароль")
#     else:
#         print('Вы успешно вошли')
#         k = cursor.execute(f"SELECT id FROM users WHERE login = '{u_login}' AND password = '{u_password}'").fetchone()
#         u_id = k[0]
#         print(u_id)
#         ifCategory(u_id)
#
#
# # Функция для добавления категории
# def addCategory(c_name):
#     cursor.execute(f"SELECT name FROM category WHERE name='{c_name}'")
#
#     if cursor.fetchone() is None:
#         cursor.execute(f"INSERT INTO category (name) VALUES('{c_name}')")
#         connect.commit()
#         print("Вы успешно добавили категорию")
#     else:
#         print("Такая категория уже существует, придумай что-то оригинальное")
#
#
# # Функция для подписки на определенную категорию
# def subscribe(u_id):
#     cursor.execute(f"SELECT * FROM category")
#
#     print("Выбирите номер на которую хотите подписаться")
#     m = cursor.fetchall()
#     for i in m:
#         print(f'{i[0]} - {i[1]}')
#
#     c_id = int(input("Номер категории на которую хотите подписаться:"))
#
#     cursor.execute(f"SELECT id_user, id_category FROM subscription WHERE id_user = '{u_id}' AND id_category = '{c_id}'")
#
#     if (cursor.fetchall() == []):
#         cursor.execute(f"SELECT id FROM category WHERE id='{c_id}'")
#         if cursor.fetchone() is None:
#             print("Такой категории нет")
#         else:
#             cursor.execute(f"INSERT INTO subscription (id_user, id_category) VALUES('{u_id}','{c_id}')")
#             connect.commit()
#             print("Вы успешно подписались на категорию!")
#     else:
#         print("Вы уже подписаны на эту категорию...")
#
#
# # Функция для просмотра категорий, на которые подписан определенный пользователь
# def subscriptions(u_id):
#     cursor.execute(f"SELECT * FROM subscription WHERE id_user = '{u_id}'")
#     m = cursor.fetchall()
#
#     if m != []:
#         print("Ваши подписки:")
#         for i in m:
#             cursor.execute(f"SELECT category.name FROM category WHERE id = {i[1]}")
#             connect.commit()
#             r = cursor.fetchone()
#             print(f"{i[1]} - {r[0]}")
#     else:
#         print("Вы ни на что не подписаны")
#
#
# # Функция для отписки пользователя от конкретной категории
# def unSubscription(u_id, c_id):
#     cursor.execute(f"SELECT id FROM category WHERE id='{c_id}'")
#     if cursor.fetchone() is None:
#         print("Такой категории нет")
#     else:
#         cursor.execute(f"DELETE FROM subscription WHERE id_user = '{u_id}' AND id_category ='{c_id}'")
#         connect.commit()
#         print("Вы успешно отписались от категории!")
#
#     subscriptions(u_id)
#
#
# # Функция для удаления категории
# def deleteCategory():
#     cursor.execute(f"SELECT * FROM category")
#     connect.commit()
#     # c_id, u_id
#     print("Список имеющихся категорий:")
#     m = cursor.fetchall()
#     # print(m)
#     for i in m:
#         print(f'{i[0]} - {i[1]}')
#
#     c_id = int(input("Номер категории которую хотите удалить: "))
#     print(f'Вы уверены, что хотите удалить категорию под номером "{c_id}"?')
#     f = int(input(f"1 - Да; 2 - Нет"))
#     if (f == 1):
#         cursor.execute(f"SELECT id FROM category WHERE id='{c_id}'")
#         if cursor.fetchone() is None:
#             print("Вы не можете удалить категорию, которой нет :(")
#         else:
#             cursor.execute(f"DELETE FROM category WHERE id ='{c_id}'")
#             connect.commit()
#             cursor.execute(f"DELETE FROM subscription WHERE id_category ='{c_id}'")
#             connect.commit()
#             print("Вы успешно удалили категорию")
#
#
# # Функция для работы с категориями
# def ifCategory(u_id):
#     print('Действия с категориями')
#     print("1 - Добавить; 2 - Подписаться; 3 - Отписаться; 4 - Подписки; 5 - Удалить категорию; 0 - Выйти;")
#     b = int(input(''))
#     while b != 0:
#         if b == 1:
#             c_name = input("Название категории: ")
#             addCategory(c_name)
#         elif b == 2:
#             subscribe(u_id)
#         elif b == 3:
#             c_id = int(input("Введите номер категории от которой хотите отписаться: "))
#             unSubscription(u_id, c_id)
#         elif b == 4:
#             subscriptions(u_id)
#         elif b == 5:
#             deleteCategory()
#         print()
#         print(
#             "1 - Добавить; 2 - Подписаться; 3 - Отписаться; 4 - Подписки; 5 - Удалить категорию; 0 - Выйти из аккаунта;")
#         b = int(input(''))
#
#
# # запуск программы, вход и авторизация
# print("1 - зарегистрироваться; 2 - войти;")
# a = int(input(''))
# while a != 0:
#     if a == 1:
#         u_login = input("Login: ")
#         u_password = input("Password: ")
#
#         reg(u_login, u_password)
#     elif a == 2:
#         u_login = input("Login: ")
#         u_password = input("Password: ")
#         auth(u_login, u_password)
#     else:
#         print("Такой команды нет")
#
#     print("1 - зарегистрироваться; 2 - войти; 0 - завершить работу;")
#     a = int(input(''))
