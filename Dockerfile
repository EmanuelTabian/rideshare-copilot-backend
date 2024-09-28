FROM public.ecr.aws/docker/library/python:3.10-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && \
    apt-get install libpq-dev postgresql-client gcc -y && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip psycopg2-binary 

WORKDIR /code

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

RUN  python /code/ridebackend/manage.py collectstatic --no-input

EXPOSE 8000

CMD ["sh", "-c", "python /code/ridebackend/manage.py makemigrations && python /code/ridebackend/manage.py migrate && python /code/ridebackend/manage.py runserver 0.0.0.0:8000"]
