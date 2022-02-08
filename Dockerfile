FROM python:3.10 AS build

ENV APP_CODE=/code
WORKDIR $APP_CODE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system
RUN pip install flake8 && mkdir -p ./docs/Flake8

COPY . ./

FROM build AS development
CMD flake8 -v --ignore=E501 --count --output-file=./docs/Flake8/flake8.log
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

EXPOSE 8000