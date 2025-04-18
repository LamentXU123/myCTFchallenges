FROM python:3.13.2-slim-bookworm

RUN useradd -m  ctf

# 拷贝源码和启动脚本至根目录
COPY ./src/ /app
COPY ./service/docker-entrypoint.sh /
RUN chown -R root:ctf /app

EXPOSE 13337

# 指定容器入口点
ENTRYPOINT ["/bin/sh","/docker-entrypoint.sh"]