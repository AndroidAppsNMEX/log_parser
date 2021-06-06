FROM python:3.8-slim
WORKDIR /
# ENV FLASK_APP interface
# ENV FLASK_ENV development
RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0"]