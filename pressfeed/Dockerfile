ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    apt-get update && apt-get install -y build-essential
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
CMD ["daphne", "pressfeed.asgi:application", "-b", "0.0.0.0", "-p", "8000", "-w", "2"]

