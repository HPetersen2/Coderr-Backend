#syntax=docker/dockerfile:1

FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]