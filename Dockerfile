FROM python:3.8.1-alpine
RUN apk update && \
    apk add --virtual build-base gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd build-base python-dev py-pip jpeg-dev zlib-dev

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
#CMD [ "python /app/server/manage.py migrate" ]
