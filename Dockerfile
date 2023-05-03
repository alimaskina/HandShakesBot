FROM python:3.10-slim-buster
WORKDIR /home

RUN apt-get update && apt-get -y install git python3 python3-pip

ARG VK_TOKEN=your_token
ENV VK_TOKEN="${VK_TOKEN}"
ARG TG_TOKEN=your_token
ENV TG_TOKEN="${TG_TOKEN}"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m", "src.App", "telegram" ]