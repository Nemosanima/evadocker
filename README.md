# evadocker

## Local launch instraction

### Create .env file with data for db in the root directory of the project
# example
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Running docker-compose
```
docker-compose up -d
```

### When finished, docker-compose will report that the containers are built and running
```
# run the following commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
### Site launched locally
```
http://localhost/
```
### Stop and remove containers with all dependencies
```
docker-compose down -v
```
