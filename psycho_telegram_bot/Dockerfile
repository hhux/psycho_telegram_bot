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
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev rust cargo dcron \
    && pip install --upgrade pip

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

# copy schedule.sh script
COPY ./shedule.sh /psycho_telegram_bot/shedule.sh
RUN chmod +x /psycho_telegram_bot/shedule.sh

# Expose the necessary ports for Django and cron
EXPOSE 8000

# Define default command for cron container
CMD ["sh", "-c", "crond -f"]
