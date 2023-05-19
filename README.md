# evadocker

## Local launch instraction

### Create .env file with data for db in the root directory of the project

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
