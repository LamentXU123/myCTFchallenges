FROM tiangolo/uwsgi-nginx-flask:python3.9-alpine

RUN apk update
RUN adduser -D ctf
RUN pip install Flask==3.1.0
COPY ./flag /flag_h4r4

WORKDIR /app
ADD . .
RUN chown -R root:ctf .
RUN python3 app.py

