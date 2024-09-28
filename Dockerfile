FROM public.ecr.aws/docker/library/python:3.10-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && \
    apt-get install libpq-dev postgresql-client -y && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

RUN  python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]