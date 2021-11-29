ARG IMAGE_VARIANT=buster
ARG PYTHON_VERSION=3.9.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3

COPY requirements.txt requirements.txt
ENV STAGE=dev

RUN pip install -r requirements.txt
RUN apt update
RUN apt install curl -y
RUN apt install unzip -y
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
WORKDIR /src