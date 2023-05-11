FROM python:3.11.3-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
 
CMD python manage.py runserver 0.0.0.0:8000
