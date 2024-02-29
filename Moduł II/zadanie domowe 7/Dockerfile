FROM python:3.11-alpine

ENV APP_HOME /app

EXPOSE 5432

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --system

COPY . /app/

CMD ["python", "main.py"]