FROM python:3.9.6-slim-buster

WORKDIR /appplication

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./source .

CMD ["python", "manage.py", "runserver", "0.0.0.0:7652"]
