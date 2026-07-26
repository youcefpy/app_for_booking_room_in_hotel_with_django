FROM python:3.12-slim

WORKDIR /app 

COPY Pipfile Pipfile.lock ./


RUN pip install --upgrade pip \ 
    && pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile


    
COPY . . 