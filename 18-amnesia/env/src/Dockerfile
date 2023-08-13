FROM ubuntu:20.04

ENV HOST localhost:3000
ENV FLAG b6actf{h4v1ng_b64ctf_1n_my_pub1c_key_m4d5_m5_s0b5r}

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install Flask

RUN mkdir /app
COPY . /app

WORKDIR /app

RUN pip3 install PyJWT cryptography

ENTRYPOINT ["python3", "app.py"]