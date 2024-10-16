# Dockerfile for the Telegram Bot (psycho_telegram_bot)

# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /psycho_telegram_bot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# Run the telegram bot script
CMD ["python", "app/telegram_bot.py"]
