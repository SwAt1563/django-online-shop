FROM python:3.8-alpine
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

# image for our application
# we create two contatiners of these image
# one for web for run ther server
# and other for use celery when the server on



