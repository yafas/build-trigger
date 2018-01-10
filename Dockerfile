FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=/app/app.py

CMD gunicorn app:app -w 4 -b 0.0.0.0:5000
