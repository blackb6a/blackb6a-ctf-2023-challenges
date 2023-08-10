FROM ubuntu:20.04

ENV HOST localhost:3000
RUN echo "b6actf{testflag}" > /proof-of-p011ut10n-$(cat /dev/urandom | tr -dc [:alnum:] | fold -w 64 | head -n 1)
RUN useradd b6auser --create-home

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install Flask

RUN mkdir /app
COPY src/ /app

WORKDIR /app

# RUN pip3 install 
USER b6auser
CMD ["python3", "app.py"]