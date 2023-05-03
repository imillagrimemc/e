import sqlite3
import time
import telebot
import xlwt

import config
import sys
from telebot import types
from datetime import datetime

print("Проект успешно запущен!")
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
      id int NOT NULL , 
      name  varchar(255), 
      phone  varchar(255),
      city  varchar(255), 
      brand  varchar(255),
      category  varchar(255), 
      mail  varchar(255), 
      site  varchar(255),
      place  varchar(255), 
      stelajone  varchar(255),
      stelajtwo  varchar(255),
      stelajthree  varchar(255),
      chair  varchar(255),
      hanger  varchar(255),
      dummy  varchar(255),
      mirror  varchar(255),
      storage  varchar(255),
      electric  varchar(255),
      price  INTEGER,
      PRIMARY KEY (id) )
      """)
    connect.commit()
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id} ")
    data = cursor.fetchone()
    if data is None:
        print(1)
        users_list = [message.chat.id]
        cursor.execute("INSERT INTO users (id) VALUES(?)", users_list)
        connect.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #btn1 = types.KeyboardButton("FAQ")
        btn2 = types.KeyboardButton("Регистрация")
        markup.add(btn2)
        bot.send_message(message.chat.id,
                         text="""Привет, {0.first_name}! 
Ты готов стать частью ART-HUB NEXT MARKET?
""".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, reg)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        next = types.KeyboardButton("Далее")
        markup.add(next)
        bot.send_message(message.chat.id,
                         text="Привет {0.first_name}!\n"
                              "Давно не виделись, мы ждали тебя с нетерпением!\n"
                              "Нажми ДАЛЕЕ что бы продолжить\n".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, exp)


@bot.message_handler(commands=['database'])
def datab(message):
    bot.send_message(message.chat.id, text= "Введите пароль:")
    bot.register_next_step_handler(message, check)

def clear_data(message):
    text = message.text
    if text == "Да":
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        # Очищаем три столбца
        cursor.execute(
            "UPDATE users SET place=?, stelajone=?, stelajtwo=?, stelajthree=?, chair=?, hanger=?, dummy=?, mirror=?, storage=?, electric=?, price=?",
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        # Сохраняем изменения
        connect.commit()
        # Закрываем подключение к базе данных
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Назад")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="База очищена", reply_markup=markup)
        bot.register_next_step_handler(message, start)

    if text == "Нет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Назад")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Перейти назад", reply_markup=markup)
        bot.register_next_step_handler(message, start)


def check(message):
    text = message.text
    print(text)
    if text == "io":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Очистка")
        btn2 = types.KeyboardButton("Экспорт")
        btn3 = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Пароль совпадает", reply_markup=markup)
        bot.register_next_step_handler(message, data)

@bot.message_handler(content_types=['text','document'])
def data(message):
    text = message.text
    if text == "Экспорт":
        bot.send_message(message.chat.id, text="Обрабатываю")
        # создание объекта курсора
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT name, phone, city, brand, category, mail, site FROM users")
        # создание нового excel файла
        wb = xlwt.Workbook()
        # добавление листа в книгу
        sheet1 = wb.add_sheet('Sheet 1')
        # запись данных из БД в Excel
        for i, row in enumerate(cursor.fetchall()):
            for j, col in enumerate(row):
                sheet1.write(i, j, col)

        # сохранение файла
        wb.save('datab/data-file.xls')
        print("us")
        with open('datab/data-file.xls', 'rb') as f1:
            bot.send_document(message.chat.id, f1)
        print("e")

    if text == "Очистка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Вы уверенны?", reply_markup=markup)
        bot.register_next_step_handler(message, clear_data)

    if text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Вы уверенны?", reply_markup=markup)
        bot.register_next_step_handler(message, start)




@bot.message_handler(content_types=['text','contact','photo'])
def reg(message):
    text = message.text
    if text == "Регистрация":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
        button_phone = types.KeyboardButton(text="Отправить телефон",  request_contact=True)  # Указываем название кнопки, которая появится у пользователя
        keyboard.add(button_phone)  # Добавляем эту кнопку
        bot.send_message(message.chat.id, 'Введите или отправьте номер телефона', reply_markup=keyboard)
        bot.register_next_step_handler(message, sch)


def sch(message):
    if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE  users SET phone =" +str( message.contact.phone_number)+" WHERE id="+str(message.chat.id))
        connect.commit()

    if message.contact == None:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE  users SET phone =" +str( message.text)+" WHERE id="+str(message.chat.id))
        connect.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back)
    urls = str(message.text)
    if (urls == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Регистрация")
        markup.add(button1)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Ташкент")
        button2 = types.KeyboardButton("Респ.Каракалпакстан")
        button3 = types.KeyboardButton("Таш.область")
        button4 = types.KeyboardButton("Андижанская область")
        button5 = types.KeyboardButton("Бухарская область")
        button6 = types.KeyboardButton("Джизакская область")
        button7 = types.KeyboardButton("Кашкадарьинская область")
        button8 = types.KeyboardButton("Навоийская область")
        button9 = types.KeyboardButton("Наманганская область")
        button10 = types.KeyboardButton("Самаркандская область")
        button11 = types.KeyboardButton("Хорезмская область")
        button12 = types.KeyboardButton("Ферганская область")
        button13 = types.KeyboardButton("Сырдарьинская область")
        button14 = types.KeyboardButton("Сурхандарьинская область")
        markups.add(button1,button2,button3,button4,button5,button6,button7,button8,button9,button10,button11,button12,button13,button14)
        bot.send_message(message.chat.id, text="Город, где находится бренд / мастер / дизайнер:", reply_markup=markups)
        bot.register_next_step_handler(message, name_user)

def name_user(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET city =? WHERE id=?" , (str(message.text) , message.chat.id))
    connect.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(message.from_user.first_name)
    markup.add(button1)
    bot.send_message(message.chat.id, text="Введите или выберите Ваше имя:", reply_markup=markup)
    bot.register_next_step_handler(message, brand)


def brand(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET name =? WHERE id=?" , (str(message.text) , message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, text="Название бренда:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, cotb)

def cotb(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET brand =? WHERE id=?" , (str(message.text) , message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, text="Категория вашего товара, ассортимент (максимально подробно, пожалуйста)", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, emails)

def emails(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET category =? WHERE id=?" , (str(message.text) , message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, text="Введите свой E-mail", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, site)

def site(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET mail =? WHERE id=?" , (str(message.text) , message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, text="АКТИВНЫЕ ссылки на социальные сети (т.е. не просто название аккаунта @sample, а именно активная ссылка) и сайт, если есть", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, update)


def update(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET site =? WHERE id=?" , (str(message.text) , message.chat.id))
    connect.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next = types.KeyboardButton("Далее")
    markup.add(next)
    bot.send_message(message.chat.id,
                     text="Вы прошли регистрацию, нажмите Далее для выбора место",
                     reply_markup=markup)
    bot.register_next_step_handler(message, exp)


def exp(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("1-Этаж")
    button2 = types.KeyboardButton("3-этаж")
    button3 = types.KeyboardButton("OpenAir")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, text="Выберите участок для аренды:", reply_markup=markup)
    bot.register_next_step_handler(message, one)

def one(message):
    one_plane = str("1-Этаж")
    three_plane = str("3-этаж")
    open_plane = str("OpenAir")
    if message.text == one_plane:
        bot.send_message(message.chat.id, text="Вы выбрали 1 этаж",reply_markup=types.ReplyKeyboardRemove())
        image_info = {
            'photo': open('one_plate.jpg', 'rb'),
            'caption': 'План 1 этажа'
        }
        bot.send_photo(message.chat.id, **image_info)
        markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("1/1")
        button2 = types.KeyboardButton("1/2")
        button3 = types.KeyboardButton("1/3")
        button4 = types.KeyboardButton("1/4")
        button5 = types.KeyboardButton("1/5")
        button6 = types.KeyboardButton("1/6")
        button7 = types.KeyboardButton("1/7")
        button8 = types.KeyboardButton("1/8")
        button9 = types.KeyboardButton("1/9")
        button10 = types.KeyboardButton("1/10")
        button11 = types.KeyboardButton("1/11")
        button12 = types.KeyboardButton("1/12")
        button13 = types.KeyboardButton("1/13")
        button14 = types.KeyboardButton("1/14")
        button15 = types.KeyboardButton("1/15")
        button16 = types.KeyboardButton("1/16")
        button17 = types.KeyboardButton("1/17")
        button18 = types.KeyboardButton("1/18")
        button19 = types.KeyboardButton("1/19")
        button20 = types.KeyboardButton("1/20")
        button21 = types.KeyboardButton("1/21")
        button22 = types.KeyboardButton("1/22")
        button23 = types.KeyboardButton("1/23")
        button24 = types.KeyboardButton("1/24")
        button25 = types.KeyboardButton("1/25")
        button26 = types.KeyboardButton("1/26")
        button27 = types.KeyboardButton("1/27")
        button28 = types.KeyboardButton("1/28")
        button29 = types.KeyboardButton("1/29")
        button30 = types.KeyboardButton("1/30")
        button31 = types.KeyboardButton("1/31")
        markups.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                    button12, button13, button14, button15, button16, button17, button18, button19, button20, button21,
                    button22, button23, button24, button25, button26, button27, button28, button29, button30, button31)

        bot.send_message(message.chat.id, text="Выберете место", reply_markup=markups)
        bot.register_next_step_handler(message, readoneDb)


    elif message.text == three_plane:
        bot.send_message(message.chat.id, text="Вы выбрали 3 этаж", reply_markup=types.ReplyKeyboardRemove())
        image_info = {
            'photo': open('three_plate.jpg', 'rb'),
            'caption': 'План 3 этажа'
        }
        bot.send_photo(message.chat.id, **image_info)
        markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("3/1")
        button2 = types.KeyboardButton("3/2")
        button3 = types.KeyboardButton("3/3")
        button4 = types.KeyboardButton("3/4")
        button5 = types.KeyboardButton("3/5")
        button6 = types.KeyboardButton("3/6")
        button7 = types.KeyboardButton("3/7")
        button8 = types.KeyboardButton("3/8")
        button9 = types.KeyboardButton("3/9")
        button10 = types.KeyboardButton("3/10")
        button11 = types.KeyboardButton("3/11")
        button12 = types.KeyboardButton("3/12")
        button13 = types.KeyboardButton("3/13")
        button14 = types.KeyboardButton("3/14")
        button15 = types.KeyboardButton("3/15")
        markups.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                    button12, button13, button14, button15)
        bot.send_message(message.chat.id, text="Выберете место", reply_markup=markups)
        bot.register_next_step_handler(message, readoneDb)

    elif message.text == open_plane:
        bot.send_message(message.chat.id, text="Вы выбрали OpenAir", reply_markup=types.ReplyKeyboardRemove())
        image_info = {
            'photo': open('open_plate.jpg', 'rb'),
            'caption': 'План 1 этажа'
        }
        bot.send_photo(message.chat.id, **image_info)
        markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("4/1")
        button2 = types.KeyboardButton("4/2")
        button3 = types.KeyboardButton("4/3")
        button4 = types.KeyboardButton("4/4")
        button5 = types.KeyboardButton("4/5")
        button6 = types.KeyboardButton("4/6")
        button7 = types.KeyboardButton("4/7")
        button8 = types.KeyboardButton("4/8")
        button9 = types.KeyboardButton("4/9")
        button10 = types.KeyboardButton("4/10")
        button11 = types.KeyboardButton("4/11")
        button12 = types.KeyboardButton("4/12")
        button13 = types.KeyboardButton("4/13")
        button14 = types.KeyboardButton("4/14")
        button15 = types.KeyboardButton("4/15")
        button16 = types.KeyboardButton("4/16")
        button17 = types.KeyboardButton("4/17")
        button18 = types.KeyboardButton("4/18")
        button19 = types.KeyboardButton("4/19")
        button20 = types.KeyboardButton("4/20")
        markups.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                    button12, button13, button14, button15, button16, button17, button18, button19, button20)

        bot.send_message(message.chat.id, text="Выберете место", reply_markup=markups)
        bot.register_next_step_handler(message, readDb)

@bot.message_handler(content_types=['text'])
def readDb(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT place from users")
    records = cursor.fetchall()
    arr = [i[0] for i in records]
    global x
    x = message.text
    if x in arr:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("1-Этаж")
        button2 = types.KeyboardButton("3-этаж")
        button3 = types.KeyboardButton("OpenAir")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Выберите другое место это уже занято!:", reply_markup=markup)
        bot.register_next_step_handler(message, one)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = types.KeyboardButton("Подтвердить")
        markup.add(button3)
        bot.send_message(message.chat.id, text="Подтвердите выбор", reply_markup=markup)
        bot.register_next_step_handler(message, open_vibor)

@bot.message_handler(content_types=['text'])
def readoneDb(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT place from users")
    records = cursor.fetchall()
    arr = [i[0] for i in records]
    x = message.text
    if x in arr:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("1-Этаж")
        button2 = types.KeyboardButton("3-этаж")
        button3 = types.KeyboardButton("AirOpen")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Выберите другое место это уже занято!:", reply_markup=markup)
        bot.register_next_step_handler(message, one)

    else:
        prices = 250000
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE  users SET place =?, price = ? WHERE id=?", (str(x), prices, message.chat.id))
        connect.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = types.KeyboardButton("Подтвердить")
        markup.add(button3)
        bot.send_message(message.chat.id, text="Подтвердите выбор", reply_markup=markup)
        bot.register_next_step_handler(message, vibor)

def vibor(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next = types.KeyboardButton("Далее")
    markup.add(next)
    bot.send_message(message.chat.id,
                     text="Место выбрано! нажмите ДАЛЕЕ чтобы продолжить.".format(
                         message.from_user), reply_markup=markup)

    bot.register_next_step_handler(message, dop_op)

def open_vibor(message):
    prices = 400000
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE  users SET place =?, price = ? WHERE id=?" , (str(x) , prices , message.chat.id))
    connect.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next = types.KeyboardButton("Далее")
    markup.add(next)
    bot.send_message(message.chat.id,
                     text="Место выбрано! нажмите ДАЛЕЕ чтобы продолжить.".format(
                         message.from_user), reply_markup=markup)

    bot.register_next_step_handler(message, dop_op)

def dop_op(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    # Очищаем три столбца
    cursor.execute(
        "UPDATE users SET stelajone=?, stelajtwo=?, stelajthree=?, chair=?, hanger=?, dummy=?, mirror=?, storage=?, electric=? WHERE id=?",
        (0, 0, 0, 0, 0, 0, 0, 0, 0, message.chat.id))
    # Сохраняем изменения
    connect.commit()
    arg = message.text
    prov = str("Далее")
    if arg == prov:
        bot.send_message(message.chat.id, text="Так-же можете выбрать это:", reply_markup=types.ReplyKeyboardRemove())
        markup = telebot.types.InlineKeyboardMarkup()
        btn_1 = telebot.types.InlineKeyboardButton('Стеллаж №1', callback_data='tovar_1')
        btn_2 = telebot.types.InlineKeyboardButton('Стеллаж №2', callback_data='tovar_2')
        btn_3 = telebot.types.InlineKeyboardButton('Стеллаж №3', callback_data='tovar_3')
        btn_4 = telebot.types.InlineKeyboardButton('Стул', callback_data='tovar_4')
        btn_5 = telebot.types.InlineKeyboardButton('Вешалка', callback_data='tovar_5')
        btn_6 = telebot.types.InlineKeyboardButton('️Манекен', callback_data='tovar_6')
        btn_7 = telebot.types.InlineKeyboardButton('Зеркало', callback_data='tovar_7')
        btn_8 = telebot.types.InlineKeyboardButton('Камера хранения', callback_data='tovar_8')
        btn_9 = telebot.types.InlineKeyboardButton('Эл.сеть', callback_data='tovar_9')
        btn_10 = telebot.types.InlineKeyboardButton('Очистить корзину', callback_data='tovar_10')
        btn_11 = telebot.types.InlineKeyboardButton('К оплате!', callback_data='tovar_11')
        markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, btn_9, btn_10, btn_11)
        bot.send_message(message.chat.id, text="""
****************************************
🪟Стеллаж №1 - 40 000 сум (Угловой, размер 2х0,50м)
🪟Стеллаж №2 - 50 000 сум ( Х, размер 1,5х2м)
🪟Стеллаж №3 - 60 000 сум (Летнница, размер 2х1,5м)
🪑Стул - 20 000 сум
🧬Вешалка - 40 000 сум
👯‍♀️Манекен (с человеческий рост) - 40 000 сум
🪞Зеркало на стойке - 25 000 сум
🚪Место в камере хранения (от выставки до выставки, или при многодневных ивентах) 5000 сум за 1 сутки
🖲Подключение к эл.сети - 25 000 сум
****************************************""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'tovar_1':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT stelajone FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET stelajone =? WHERE id=?", ("40000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, 'Стеллаж №1 добавлен в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 40000
            sv = sd / 40000 + 1.0
            cursor.execute("UPDATE  users SET stelajone =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Стеллаж №1 добавлен в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_2':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT stelajtwo FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET stelajtwo =? WHERE id=?", ("50000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, 'Стеллаж №2 добавлен в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 50000
            sv = sd / 50000 + 1.0
            cursor.execute("UPDATE  users SET stelajtwo =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Стеллаж №2 добавлен в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_3':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT stelajthree FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET stelajthree =? WHERE id=?", ("60000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, 'Стеллаж №3 добавлен в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 60000
            sv = sd / 60000 + 1.0
            cursor.execute("UPDATE  users SET stelajthree =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Стеллаж №3 добавлен в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_4':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT chair FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET chair =? WHERE id=?", ("20000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, 'Стул добавлен в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 20000
            sv = sd / 20000 + 1.0
            cursor.execute("UPDATE  users SET chair =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Стул добавлен в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_5':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT dummy FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET dummy =? WHERE id=?", ("40000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'️Манекен добавлена в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 40000
            sv = sd / 40000 + 1.0
            cursor.execute("UPDATE  users SET dummy =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'️Манекен добавлена в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_6':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT hanger FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET hanger =? WHERE id=?", ("40000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Вешалка добавлена в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 40000
            sv = sd / 40000 + 1.0
            cursor.execute("UPDATE  users SET hanger =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Вешалка добавлена в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_7':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT mirror FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET mirror =? WHERE id=?", ("25000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Зеркало добавлено в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 25000
            sv = sd / 25000 + 1.0
            cursor.execute("UPDATE  users SET mirror =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Зеркало добавлено в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)



    elif call.data == 'tovar_8':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT storage FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET storage =? WHERE id=?", ("5000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Место хранения добавлена в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 5000
            sv = sd / 5000 + 1.0
            cursor.execute("UPDATE  users SET storage =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Место хранения добавлена в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)


    elif call.data == 'tovar_9':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT electric FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        ako = str(data)
        if ako == '(None,)':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE  users SET electric =? WHERE id=?", ("25000", call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Эл.сеть добавлена в корзину! Всего:1.0')
        else:
            sd = int(data[0])
            sf = sd + 25000
            sv = sd / 25000 + 1.0
            cursor.execute("UPDATE  users SET electric =? WHERE id=?", (sf, call.message.chat.id))
            connect.commit()
            bot.send_message(call.message.chat.id, f'Эл.сеть добавлена в корзину! Всего:{sv}')
        bot.answer_callback_query(call.id)

    elif call.data == 'tovar_10':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        # Очищаем три столбца
        cursor.execute("UPDATE users SET stelajone=?, stelajtwo=?, stelajthree=?, chair=?, hanger=?, dummy=?, mirror=?, storage=?, electric=? WHERE id=?", (0,0,0,0,0,0,0,0,0,call.message.chat.id))
        # Сохраняем изменения
        connect.commit()
        # Закрываем подключение к базе данных
        bot.send_message(call.message.chat.id, 'Корзина очищена!')
        bot.answer_callback_query(call.id)

    elif call.data == 'tovar_11':
        #bot.send_message(call.message.chat.id, 'Ссылка на оплату!')
        bot.send_message(call.message.chat.id, text="Произвожу расчеты", reply_markup=types.ReplyKeyboardRemove())
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        people_id = call.message.chat.id
        cursor.execute(f"SELECT * FROM users WHERE id = {people_id} ")
        data = cursor.fetchone()
        print(data)
        palate = str(data[8])
        prises = int(data[18])
        stelajone = int(data[9])
        stelajtwo = int(data[10])
        stelajthree = int(data[11])
        chair = int(data[12])
        dummy = int(data[13])
        hanger = int(data[14])
        mirror = int(data[15])
        storage = int(data[16])
        electric = int(data[17])
        pay = stelajone + stelajtwo + stelajthree + chair + dummy + hanger + mirror + storage + electric + prises
        #ako = str(data)
        markup = telebot.types.InlineKeyboardMarkup()
        btn_1 = telebot.types.InlineKeyboardButton('Подтвердить!', callback_data='okay')
        btn_2 = telebot.types.InlineKeyboardButton('Отменить', callback_data='not')
        markup.add(btn_2, btn_1)
        bot.send_message(call.message.chat.id, f"""
Подтвердите свой заказ
Ваша корзина:
Место [{palate}] Цена - [{prises}]
Стеллаж №1 - [{stelajone}]
Стеллаж №2 - [{stelajtwo}]
Стеллаж №3 - [{stelajthree}]
Стул - [{chair}]
Манекен - [{dummy}]
Вешалка - [{hanger}]
Зеркало - [{mirror}]
Место для хранения - [{storage}]
Эл.сеть - [{electric}]
ОБЩАЯ СУММА: [{pay}]
""",reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == 'okay':
        bot.send_message(call.message.chat.id, text="""Ссылка на оплату**********!
После транзакции сделайте скрин оплаты и скиньте сюда.  
      
ПРИМЕЧАНИЕ - скриншот отправлять как фото не файл!
""")
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(call.message, screen)

    elif call.data == 'not':
        bot.answer_callback_query(call.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("1-Этаж")
        button2 = types.KeyboardButton("3-этаж")
        button3 = types.KeyboardButton("OpenAir")
        markup.add(button1, button2, button3)
        bot.register_next_step_handler(call.message, one)
        bot.send_message(call.message.chat.id, text="Выберите участок для аренды:", reply_markup=markup)
@bot.message_handler(content_types=['photo'])
def screen(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.chat.id
    cursor.execute(f"SELECT * FROM users WHERE id = {people_id} ")
    data = cursor.fetchone()
    print(data)
    palate = str(data[8])
    prises = int(data[18])
    stelajone = int(data[9])
    stelajtwo = int(data[10])
    stelajthree = int(data[11])
    chair = int(data[12])
    dummy = int(data[13])
    hanger = int(data[14])
    mirror = int(data[15])
    storage = int(data[16])
    electric = int(data[17])
    pay = stelajone + stelajtwo + stelajthree + chair + dummy + hanger + mirror + storage + electric + prises
    app_id = str(data[0])
    app_name = str(data[1])
    app_number = str(data[2])
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    with open(f"screens/{app_id}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    admin_id = 1441817634
    bot.send_message(admin_id, f"Поступила заявка от {app_name} !\n"
                               f"Его номер - {app_number}\n"
                               f"Арендованное место - {palate}\n"
                               f"Сумма для оплаты = {pay}\n"
                               f"Скриншот ⬇️⬇️⬇️⬇️⬇️")
    image_info = {
        'photo': open(f'screens/{app_id}.jpg', 'rb')
    }
    bot.send_photo(admin_id, **image_info)



try:
    try:
        time.sleep(10)
        bot.polling(none_stop=True)
        print("ошибка")
        time.sleep(20)
    except:
        bot.polling(none_stop=True)
except:
    bot.polling(none_stop=True)
