FROM python:3.11

WORKDIR /home/fastapi-detectron/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

COPY src /home/fastapi-detectron/
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'

RUN chmod +x /home/fastapi-detectron/docker-entrypoint.sh
