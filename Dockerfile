FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app/src

CMD ["gunicorn", "evangelion.wsgi:application", "--bind", "0:8000" ]
