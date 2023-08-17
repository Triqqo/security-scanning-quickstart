FROM python:3.9-alpine3.12

COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py

WORKDIR app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]