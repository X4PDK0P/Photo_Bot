import telebot
from config import TOKEN, path
import os
from datetime import datetime
from pathlib import Path
from photo_edit import pedit


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    mes_text = f'Привет, {message.from_user.first_name}\nКартинку ?'
    bot.send_message(message.chat.id, mes_text)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, "Секунду...")
    file_photo = bot.get_file(message.photo[-1].file_id)  # Забираем ID фото (самая крупная версия)
    filename, file_extension = os.path.splitext(file_photo.file_path)  # Берем имя файла и расширение
    downloaded_photo = bot.download_file(file_photo.file_path)  # скачиваем с телеграмма
    photo_name = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + "_" + str(message.from_user.id) + file_extension
    src = Path(path, photo_name)
    with open(src, "wb") as new_file:
        new_file.write(downloaded_photo)  # Сохраняем файл на сервере
    bot.send_photo(message.chat.id, pedit(photo_name))  # Редактируем файл и отправляем пользователю
    bot.send_message(message.chat.id, "Поделись фотографией с друзьями :0")


bot.polling(none_stop=True)
