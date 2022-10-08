import telebot
from telebot import types
import requests
import sqlite3

connect = sqlite3.connect('bdForUP.db', check_same_thread=False)

bot = telebot.TeleBot("5775281001:AAGDsJDcKpwA3asnAsPeu1QzVhiKAojVUik")
ap_key = "ea3ccad46a1b44719978d13cfeb1ad86"
news = ["business", "entertainment", "general",
		"health", "science", "sports", "technology"]
textt = ''
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

cursor.execute(f"SELECT * FROM category")
arr = cursor.fetchall()
if len(arr) < len(news):
	for category in news:
		cursor.execute(f"INSERT INTO category (name) VALUES('{category}')")
		connect.commit()

# @bot.message_handler(commands=['start'])
# def start(message):
# 	u_login = f"твой логин - <CODE>{message.from_user.id}</CODE>"
# 	bot.send_message(message.chat.id, u_login, parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
	#Добавление пользователя в базу
	u_login = str(message.from_user.id)
	cursor.execute(f"SELECT login FROM users WHERE login={u_login}")
	# connect.commit()

	if cursor.fetchone() is None:
		cursor.execute(f"INSERT INTO users (login) VALUES({u_login})")
		connect.commit()
		print ("Вы успешно зарегистрировались! ")
	else:
		print ("Пользователь с таким логином уже существует")
	bot.reply_to(message, "Банкок-Таганрог запущен")
@bot.message_handler(commands=['help'])
def send_welcome(message):
	commands ="/start - запуск бота"+"\n"+"/help - список команд"+"\n"+"/news - показывает новости на которые вы подписаны"+"\n"\
			  +"/subscribe - показывает категории новостей на которые пользователь может подписаться"+"\n"+\
			  "/subscriptions - показывает на что вы под  писаны"+"\n"+"/unSubscription - отписаться от категории новостей"
	bot.reply_to(message, commands)
@bot.message_handler(commands=['subscribe'])
def send_welcome(message):
	u_login = str(message.from_user.id)
	print(u_login)
	cursor.execute(f"SELECT * FROM category").fetchall()
	markup = types.ReplyKeyboardMarkup()
	if news is not None:
		for category in news:
			markup.add(types.KeyboardButton(category))
	bot.send_message(u_login, "Пожалуйста, выберите категорию на которую хотите подписаться:", reply_markup=markup)

	bot.register_next_step_handler(message, subscribe_user)
def subscribe_user(message):
	u_login = str(message.from_user.id)

	print(message.text)
	if message is not None:
		cursor.execute(
			f"SELECT id_user, id_category FROM subscription WHERE id_user = '{u_login}' AND id_category = '{message.text}'")

		if (cursor.fetchall() == []):
			cursor.execute(f"SELECT id FROM category WHERE name='{message.text}'")
			if cursor.fetchone() is None:
				print("Такой категории нет")
			else:
				cursor.execute(f"INSERT INTO subscription (id_user, id_category) VALUES('{u_login}','{message.text}')")
				connect.commit()
				textt = "Вы успешно подписались на категорию!"+ "\n"+"Выберите ещё одну /subscribe"
		else:
			textt = "Вы уже подписаны на эту категорию..."+ "\n"+"Попробовать ещё раз /subscribe ?"
	else:
		print('массив пустой')
		textt = "Попробуйте ещё раз"

	bot.send_message(message.from_user.id, textt, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['subscriptions'])
def subscriptions_user(message):
	u_login = str(message.from_user.id)
	cursor.execute(f"SELECT * FROM subscription WHERE id_user = '{u_login}'")
	m = cursor.fetchall()
	if m != []:
		textt = "Ваши подписки:" + "\n"
		for i in m:
			# cursor.execute(f"SELECT name FROM category WHERE name = {i[1]}")
			# connect.commit()
			print(i[1])
			# r = cursor.fetchone()
			textt += i[1]+"\n"
	else:
		textt="Вы ни на что не подписаны"

	bot.send_message(message.from_user.id, textt)
@bot.message_handler(commands=['unSubscription'])
def subscriptions_for_unsubscribing(message):
	u_login = str(message.from_user.id)
	cursor.execute(f"SELECT * FROM subscription WHERE id_user = '{u_login}'")
	markup = types.ReplyKeyboardMarkup()
	m = cursor.fetchall()
	if m is not None:
		for category in m:
			markup.add(types.KeyboardButton(category[1]))
	bot.send_message(u_login, "Пожалуйста, выберите категорию от которой хотите отписаться:", reply_markup=markup)

	bot.register_next_step_handler(message, unsubscribe)

def unsubscribe(message):
	u_login = str(message.from_user.id)

	print(message.text)
	cursor.execute(f"SELECT id FROM category WHERE name='{message.text}'")
	if cursor.fetchone() is None:
		textt = "Такой категории нет"
	else:
		cursor.execute(f"DELETE FROM subscription WHERE id_user = '{u_login}' AND id_category ='{message.text}'")
		connect.commit()
		textt = "Вы успешно отписались от категории!"

	bot.send_message(message.from_user.id, textt, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['news'])
def echo_all(message):
	u_login = str(message.from_user.id)
	cursor.execute(f"SELECT * FROM subscription WHERE id_user = '{u_login}'")
	m = cursor.fetchall()
	news_1 = []
	print(m)
	if m is not None:
		for category in m:
			a = requests.get(
				f'https://newsapi.org/v2/top-headlines?apiKey={ap_key}&country=de&pageSize=2&category={category[1]}')
			for i in a.json()['articles']:
				news_1.append([i['title'], i['description'], i['url']])

		print(news_1)
		answer = ""
		for i in range(len(news_1)):
			# print(i)
			# print(news[i])
			# print(news[i][0],news[i][1],news[i][2])
			# + news[i][1] + "\n"
			answer = news_1[i][0] + "\n" + news_1[i][2] + "\n"
			# print(answer)
			bot.send_message(message.from_user.id, answer)
	else:
		bot.send_message(message.from_user.id, 'вы ещё не подписались на новости')

# # @bot.message_handler(func=lambda message: True)
# # def echo_all(message):
# # 	bot.reply_to(message, "Сам такой")

# bot.polling(none_stop=True)
bot.infinity_polling()
# print('hello')