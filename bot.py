# -*- coding: utf-8 -*-
from db.connect_db import SessionLocal
import time
from datetime import datetime

import telebot
from telebot import types
from core.config import TELEGRAM_TOCKEN

#tocken = '5171909645:AAG8HefH3P9iSSk4eMec70jBde24Vxtb3b8'
tocken = TELEGRAM_TOCKEN
bot = telebot.TeleBot(tocken)
# parse_mode='HTML'
db = SessionLocal()

U_Name = []
U_Branch = []
U_Position = []

 # Менюшки   
menu1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1 = types.KeyboardButton("Перелік співробітників")
btn2 = types.KeyboardButton("Змінити статус")
btn3 = types.KeyboardButton("Реєстрація нового користувача")
menu1.add(btn1,btn2,btn3)

menu2 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn4 = types.KeyboardButton(text="Надати номер телефону", request_contact=True)
menu2.add(btn4)

menu3 = types.InlineKeyboardMarkup()
btn5 = types.InlineKeyboardButton(text='В роботі', callback_data='user_status_start')
btn6 = types.InlineKeyboardButton(text='Не в роботі', callback_data='user_status_end')
menu3.add(btn5,btn6)


# Функции
#Стартовое меню /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 
        "Оберіть співробітника або зареєструйте нового", 
        parse_mode="HTML", 
        reply_markup=menu1)


# Получаем список пользователей
@bot.message_handler(func=lambda message: True, content_types=['text'])
def main_menu(message):  
    if message.text == "Перелік співробітників": 
        q1 = '''
               SELECT  e.status, e.name, pn.position_name, e.phone, br.branch_name, ws.shift_name, ts.work_day_count ,ts.date
               FROM employees e
               JOIN positions pn on e.position_id = pn.id
               JOIN time_sheets ts on e.id = ts.emploe_id
	           JOIN branches br on e.branch_id = br.id
               JOIN working_shifts ws on e.work_shift = ws.id
            '''
        users = db.execute(q1)
        for user in users:
            if user[0] == 0:
                status = 'Не в роботі'
            if user[0] == 1:
                status = 'В роботі'  
            time.sleep(0.5)      
            bot.send_message(message.chat.id, 
                             f'''Статус: {status}\n ПІБ: {str(user[1])} \nПосада: {str(user[2])} 
                                 \nКонтакти: {str(user[3])} \nВідділення: {str(user[4])} \nЗміна: {str(user[5])}
                                 \nВідпрацьовані дні: {str(user[6])} \nДата: {str(user[7].strftime("%m/%d/%Y, %H:%M"))}
                               ''')

    if message.text == "Реєстрація нового користувача": 
        msg = bot.send_message(message.chat.id, "Введіть Прізвище Ім'я та натисніть Enter: ")
        bot.register_next_step_handler(msg, save_user_and_branch)
        #save_user_and_branch(msg)
    if message.text == "Змінити статус":
        q4 = f'SELECT name FROM employees WHERE telegram_id={str(message.chat.id)} LIMIT 1'
        find_user = db.execute(q4)
        for fu in find_user:
            bot.send_message(message.chat.id, "Вітаю: " + str(fu[0]), reply_markup=menu3)

        
    


# 1. Регистрация получает ФИО и отдел
def save_user_and_branch(message):
    U_Name.append(message.text)

    q2 = f'SELECT id, branch_name FROM branches'
    branches = db.execute(q2)

    bot.send_message(message.chat.id, 'Оберіть номер відділення: ') 
    for branch in branches:
        keyboard1 = types.InlineKeyboardMarkup()
        keyboard1.add(types.InlineKeyboardButton(text=branch[1], callback_data='select_branch'))
        bot.send_message(message.chat.id, str(branch[0]), reply_markup=keyboard1)


# 2. Регистрация получает Должность
def save_user_position(message):

    q3 = f'SELECT id, position_name FROM positions'
    positions = db.execute(q3)

    for position in positions:
        keyboard2 = types.InlineKeyboardMarkup()
        keyboard2.add(types.InlineKeyboardButton(text=position[1], callback_data='select_position'))
        bot.send_message(message.chat.id, str(position[0]), reply_markup=keyboard2)



# 3. Регистрация сохраняем пользователя в бд
@bot.message_handler(content_types=['contact'])
def save_all_to_db(message):
    p = str(message.contact.phone_number).strip(' ')
    # q1 = f'''SELECT name, phone ,telegram_id
    #         FROM employees 
    #         WHERE phone LIKE '{p}'   LIMIT 1
    #        '''               
    # UserIndent = db.execute(q1)
    # for us in UserIndent:
        #if len(us['phone']) == 0:
    db.execute(f'''INSERT INTO employees (name,phone,telegram_id,branch_id, position_id) 
                       VALUES ("{U_Name[-1]}",{p},{message.chat.id},{U_Branch[-1]},{U_Position[-1]})''')
        #db.execute(f'UPDATE employees SET telegram_id = {message.chat.id}  WHERE phone = {p}')
    db.commit()
    bot.send_message(message.chat.id, "Дякую тепер ви заруєстровані в системі", parse_mode="HTML", reply_markup=menu1)             







# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "select_branch": 
        U_Branch.append(call.message.json['text']) 
        msg = bot.send_message(call.message.chat.id, "Оберіть посаду: ")
        save_user_position(msg)
    
    if call.data == "select_position":
        U_Position.append(call.message.json['text'])
        bot.send_message(call.message.chat.id, 'Дякую тепер надайте номер телефону натиснувши на пипку', reply_markup=menu2)  

    if call.data == "user_status_start":
        db.execute(f'UPDATE employees SET status = 1  WHERE telegram_id = {str(call.message.chat.id)}') 
        db.commit()
        bot.send_message(call.message.chat.id, "Статус змінено -> в роботі", reply_markup=menu1)

    if call.data == "user_status_end": 
        db.execute(f'UPDATE employees SET status = 0  WHERE telegram_id = {str(call.message.chat.id)}') 
        db.commit()
        bot.send_message(call.message.chat.id, "Статус змінено -> не в роботі", reply_markup=menu1) 
            
bot.infinity_polling()    