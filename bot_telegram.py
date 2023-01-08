from aiogram import Bot, Dispatcher, executor, types
import markup as nav
import db
import os

TOKEN = os.environ['TELEGRAM_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

WRITE_USERS = [1893965033, 1862257837]

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup = nav.main)
    await bot.send_message(message.from_user.id, 'Ваш ID {0.id}.\nЧтобы вы хотели знать?'.format(message.from_user))
        
@dp.message_handler()
async def bot_message(message: types.Message):
    if 'асписани' in message.text:
        photo = open('img/schedule.png', 'rb')
        await bot.send_photo(message.from_user.id, photo)
    elif message.text == 'Другое':
        await bot.send_message(message.from_user.id, 'Пожалуйста!', reply_markup = nav.other)
    elif message.text == 'Обратно':
        await bot.send_message(message.from_user.id, 'Пожалуйста!', reply_markup = nav.main)

    # Запрос оценок. Формат запроса: Оценки: Имя Ученика
    elif 'ценк:' in message.text:
        pupil_name = message.text.replace(": ", ":").split(":")[1]
        marks = db.get_marks(pupil_name)
        if marks.count() > 0:
            for row in marks:
                await bot.send_message(message.from_user.id, list(row._asdict().values()))
        else:
            await bot.send_message(message.from_user.id, 'Ученик с таким именем не найден')

    # Добавление оценок. Формат запроса: Оценка: Дата, Имя ученика, Предмет, Оценка
    elif 'Добавить оценку:' in message.text:
        if message.from_user.id in WRITE_USERS:
            mark_record = message.text.replace(": ", ":").split(":")[1].split(", ")
            db.add_mark(mark_record[0], mark_record[1], mark_record[2], mark_record[3])
            await bot.send_message(message.from_user.id, 'Оценка добавлена')
        else:
            await bot.send_message(message.from_user.id, 'Нет прав на добавление оценок')

    # Удаление оценок. Формат запроса: Удалить оценку: ID оценки
    elif 'Удалить оценку:' in message.text:
        if message.from_user.id in WRITE_USERS:
            mark_id = message.text.replace(": ", ":").split(":")[1]
            if db.delete_mark(int(mark_id)):
                await bot.send_message(message.from_user.id, 'Оценка удалена')
            else:
                await bot.send_message(message.from_user.id, 'Ошибка при удалении оценки. Проверьте ID оценки.')
        else:
            await bot.send_message(message.from_user.id, 'Нет прав на удаление оценок')

    elif 'Оценки' in message.text:
        await bot.send_message(message.from_user.id, 'Для просмотра оценок напишите:\nОценки: Имя Ученика\n \nДля добавления оценки напишите:\nДобавить оценку: Дата, Имя ученика, Предмет, Оценка\n \nДля удаления оценки напишите:\nУдалить оценку: ID оценки')
    
    # Добавление ДЗ. Формат запроса: Оценка: Дата, Имя ученика, Предмет, Оценка
    elif 'Добавить ДЗ:' in message.text:
        if message.from_user.id in WRITE_USERS:
            homework_record = message.text.replace(": ", ":").split(":")[1].split(", ")
            db.add_homework(homework_record[0], homework_record[1], homework_record[2])
            await bot.send_message(message.from_user.id, 'ДЗ добавлено')
        else:
            await bot.send_message(message.from_user.id, 'Нет прав на добавление ДЗ')

    # Удаление записей с ДЗ. Формат запроса: ДЗ: ID ДЗ
    elif 'Удалить ДЗ:' in message.text:
        if message.from_user.id in WRITE_USERS:
            homework_id = message.text.replace(": ", ":").split(":")[1]
            if db.delete_homework(int(homework_id)):
                await bot.send_message(message.from_user.id, 'ДЗ удалено')
            else:
                await bot.send_message(message.from_user.id, 'Ошибка при удалении ДЗ. Проверьте ID ДЗ.')
        else:
            await bot.send_message(message.from_user.id, 'Нет прав на удаление ДЗ')

    # Запрос ДЗ. Формат запроса: ДЗ: Название предмета
    elif 'ДЗ:' in message.text:
        subject = message.text.replace(": ", ":").split(":")[1]
        homework = db.get_homework(subject)
        if homework.count() > 0:
            for row in homework:
                await bot.send_message(message.from_user.id, list(row._asdict().values()))
        else:
            await bot.send_message(message.from_user.id, 'ДЗ по предмету не найдены')
            
    elif 'Дом. задание' in message.text or 'ДЗ' in message.text:
        await bot.send_message(message.from_user.id, 'Для просмотра ДЗ напишите:\nДЗ: Название предмета\n \nДля добавления ДЗ напишите:\nДобавить ДЗ: Дата, Название предмета, Текст ДЗ\n \n Для удаления ДЗ напишите:\nУдалить ДЗ: ID ДЗ')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)