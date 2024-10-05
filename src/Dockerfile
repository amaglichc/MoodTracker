FROM python:3.12

WORKDIR /app

COPY . .

RUN pip3 install -r req.txt

CMD uvicorn main:app --host 0.0.0.0 --port 8080