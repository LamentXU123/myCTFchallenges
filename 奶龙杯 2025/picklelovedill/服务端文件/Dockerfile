FROM tiangolo/uwsgi-nginx-flask:python3.9-alpine


RUN apk update && \
    adduser -D ctf && \
    pip install bottle==0.13.2 dill==0.4.0

WORKDIR /app
ADD . .


RUN chown -R root:ctf /app && \
    chmod 751 /app && \         
    chmod 000 /app/app.py && \   
    chmod o+x /app/app.py   

USER ctf
CMD ["python3", "app.py"]