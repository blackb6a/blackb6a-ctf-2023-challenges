FROM ubuntu:20.04

ENV HOST localhost:3000
ENV FLAG b6actf{p0llute_the_w0r1d_4_sweet_sweet_c00k1es}

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install requests flask flask-session

RUN mkdir /app
COPY . /app

WORKDIR /app

CMD ["python3", "app.py"]