# DOCKERFILE for techtrends project

FROM python:3.8

LABEL maintainer="Michel M. Ferreira"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python init_db.py

CMD ["python", "app.py"]

EXPOSE 3111