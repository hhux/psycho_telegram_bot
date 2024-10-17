import logging
from datetime import datetime, timedelta

import openai
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
from prompt import text

# Устанавливаем токены для Telegram и OpenAI
TELEGRAM_TOKEN = '8095205112:AAE7gmwyImi7LkPanQwQ8OMkiU_FyY4HHd4'
OPENAI_API_KEY = 'sk-svcacct-ghH7e9F_wXQ6rWrzgLcZf3pqBX9zdZ3mtbh3aVp62PEi7zQjl30rTaclKIaT3BlbkFJKtSEvjdhHrZgiCRizALyh4ixpePVNbJlrvtNayi8wUlkX2OjKW5qaOnUhngA'

API_BASE_URL = 'http://backend:8000'

openai.api_key = OPENAI_API_KEY

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Храним информацию о пользователях и их чатах с GPT
user_sessions = {}

# Шаблонный промт для консультации по психологии
PROMPT_TEMPLATE = (f"{text}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    # Получаем список пользователей и проверяем, существует ли пользователь
    response = requests.get(f"{API_BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        user_data = next((user for user in users if user['user_id'] == user_id), None)
        if user_data:
            if user_data['is_active']:
                await update.message.reply_text("Привет! Я бот-психолог. Задайте ваш вопрос, и я постараюсь помочь.")
            else:
                await update.message.reply_text(
                    "Ваша подписка истекла. Пожалуйста, продлите подписку, чтобы продолжить использовать бота.")
                
        else:
            # Если пользователя нет в базе, регистрируем его
            create_response = requests.post(f"{API_BASE_URL}/users/create/", json={"user_id": user_id})
            if create_response.status_code == 201:
                user_sessions[user_id] = []
                await update.message.reply_text(
                    "Привет! Ваш аккаунт создан. Задайте ваш вопрос, и я постараюсь помочь.")
            else:
                await update.message.reply_text("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")
    else:
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_message = update.message.text

    logging.info(f"Сообщение от пользователя {user_id}: {user_message}")

    # Проверяем статус пользователя перед ответом
    response = requests.get(f"{API_BASE_URL}/users/")
    users = response.json()
    if response.status_code == 200:
        user_data = next((user for user in users if user['user_id'] == user_id), None)
        if not user_data['is_active']:
            logging.info(f"{user_id} подписка закончилась. Пользователь отключен")
            await update.message.reply_text(
                "Ваша подписка истекла. Пожалуйста, продлите подписку, чтобы продолжить использовать бота.")
            return
    else:
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")
        return

    # Проверяем, есть ли у пользователя сессия
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    # Добавляем сообщение пользователя в историю
    user_sessions[user_id].append({"role": "user", "content": user_message})

    # Создаем сообщение для GPT с учетом шаблонного промта
    messages = [{"role": "system", "content": PROMPT_TEMPLATE}] + user_sessions[user_id]

    # Отправляем запрос к альтернативной модели GPT-4o-mini
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Получаем ответ от GPT и отправляем его пользователю
    gpt_response = response.choices[0].message['content']
    user_sessions[user_id].append({"role": "assistant", "content": gpt_response})
    await update.message.reply_text(gpt_response)
    logging.info(f"Ответ бота: {gpt_response[:35]}...")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(msg="Exception while handling an update:", exc_info=context.error)


import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, JobQueue

async def main():
    # Создаем приложение и регистрируем обработчики
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    job_queue = JobQueue()
    job_queue.set_application(application)
    await job_queue.start()  # Нужно await

    # Команда /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    await application.run_polling()  # Нужно await

if __name__ == '__main__':
    # Создаем приложение и регистрируем обработчики
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Команда /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    application.run_polling()

