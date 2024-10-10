FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "-m" , "flask", "run"]
