FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . .
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD gunicorn app:app