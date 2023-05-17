FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

RUN cd /app/src

RUN python manage.py migrate

CMD ["python3", "manage.py", "runserver", "0:8000"]
