FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--app-dir","src","--host", "0.0.0.0", "--port", "8000" ]

