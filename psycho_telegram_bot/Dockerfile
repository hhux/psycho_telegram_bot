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
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev rust cargo \
    && apk add --no-cache busybox-suid \
    && pip install --upgrade pip

# install cron
RUN apk add --no-cache crond

# copy crontab file
COPY ./crontab /etc/crontabs/root

# start cron in the background and run the telegram bot
CMD crond && python app/telegram_bot.py

# install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# create directory for static files
RUN mkdir -p /psycho_telegram_bot/staticfiles

# collect static files
RUN python manage.py collectstatic --no-input

# Run the telegram bot script
CMD ["python", "app/telegram_bot.py"]
