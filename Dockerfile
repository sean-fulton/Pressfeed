# base image
FROM python:3.11.0

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1	
ENV PYTHONUNBUFFERED 1

# create the app directory
RUN mkdir -p /app
WORKDIR /app

#install requirements
COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/


#copy project
COPY . /app/

#expose port 8000
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "core.wsgi:application"]