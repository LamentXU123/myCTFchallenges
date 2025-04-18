FROM tiangolo/uwsgi-nginx-flask:python3.9-alpine

RUN apk update
RUN adduser -D ctf
RUN pip install bottle==0.13.2
COPY ./flag /flag_dda2d465-af33-4c56-8cc9-fd4306867b70
COPY ./secret.txt /secret.txt

WORKDIR /app/app
ADD . .
RUN chown -R root:ctf .
RUN python3 app.py

