FROM tiangolo/uwsgi-nginx-flask:python3.9-alpine

RUN apk update
RUN adduser -D ctf
RUN pip install bottle==0.13.2
COPY ./flag /flag

WORKDIR /app
ADD . .
RUN chown -R root:ctf .
RUN python3 app.py

