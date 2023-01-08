from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#---main---
btnMe = KeyboardButton('Расписание')
btnMe1 = KeyboardButton('Другое')
main = ReplyKeyboardMarkup(resize_keyboard = True).add(btnMe, btnMe1)


#---other---
btn1 = KeyboardButton('Оценки')
btn2 = KeyboardButton('Дом. задание')
btnMain = KeyboardButton('Обратно')
other = ReplyKeyboardMarkup(resize_keyboard = True).add(btn1, btn2, btnMain)