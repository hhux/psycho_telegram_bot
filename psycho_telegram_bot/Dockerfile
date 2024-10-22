FROM python:3.8.3-alpine

WORKDIR /psycho_telegram_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache curl postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev rust cargo dcron \
    && pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY . .

RUN mkdir -p /psycho_telegram_bot/staticfiles
RUN python manage.py collectstatic --no-input

COPY ./shedule.sh /psycho_telegram_bot/shedule.sh
RUN chmod +x /psycho_telegram_bot/shedule.sh

RUN echo "3 8 1 8 * /psycho_telegram_bot/shedule.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root
