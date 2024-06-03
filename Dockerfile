FROM python:3.11.3-alpine3.18
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add bash gcc python3-dev musl-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN python manage.py collectstatic -v 2 --noinput
CMD ["gunicorn", "--timeout", "1800", "-w", "1", "-b", ":8000", "--pythonpath", "rrii", "--env", "DJANGO_SETTINGS_MODULE=rrii.settings", "rrii.wsgi:application"]