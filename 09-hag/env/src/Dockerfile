FROM ubuntu:20.04

ENV HOST localhost:3000
ENV FLAG b6actf{testflag}

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install requests Flask flask-session

RUN mkdir /app
COPY . /app

WORKDIR /app

CMD ["python3", "app.py"]