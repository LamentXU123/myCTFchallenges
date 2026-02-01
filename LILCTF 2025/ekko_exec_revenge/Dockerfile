FROM python:3.13.4

RUN pip install flask werkzeug flask_sqlalchemy

COPY --chown=ctf --chmod=700 src /home/ctf/app/
COPY --chown=ctf --chmod=744 flag /flag

WORKDIR /home/ctf/app

EXPOSE 5000

CMD ["./init.sh"]