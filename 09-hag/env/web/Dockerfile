FROM ubuntu:20.04

ENV HOST localhost:3000
ENV FLAG b6actf{p0llute_the_w0r1d_4_sweet_sweet_c00k1es}

RUN apt update && apt install -y python3 python3-pip cron
RUN pip3 install requests flask flask-session

RUN mkdir /app
COPY app /app
COPY start.sh /start.sh

RUN chmod 555 /start.sh

WORKDIR /app

CMD [ "/start.sh" ]