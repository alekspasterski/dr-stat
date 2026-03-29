# System Monitor

This application shows statistics from the host server (uptime, memory, CPU).
The backend uses Django to implement a REST API, and the frontend is written in React.

![Screenshot](Screenshot.png)

The app uses:
- Django and DRF to create an API with system information
- React to create the frontend
- Gunicorn and nginx as web servers
- Celery and RabbitMQ to run workers polling the host for state
- Postgres as the DB
- Built-in Django account system with JWT for authentication
- psutil and diskinfo libraries to gather system data

## Running the application

### Development

First, you will need to set the DJANGO_SECRET environmental variable in a .env file. Rename the provided example file and change the DJANGO_SECRET variable inside.

``` sh
mv .env.example .env
```

Second, use the start.sh script to launch the application. 

``` sh
start.sh -D
```

Then you will need to create a user account to log into the monitor. You can use a superuser account or a regular account.

``` sh
docker exec -it <backend container id> /bin/bash
python manage.py createsuperuser
```

The frontend should now be accessible at ```http://localhost:5173```.

### Production build

First, you will need to create a .env.prod file. You can use the provided example file as a base:

``` sh
mv .env.prod.example .env.prod
```

Inside, set the DJANGO_SECRET and POSTGRES_PASSWORD to custom values.

To start the application, use the start.sh script.

``` sh
./start.sh
```


Then you will need to create a user account to log into the monitor. You can use a superuser account or a regular account.

``` sh
docker exec -it <backend container id> /bin/bash
python manage.py createsuperuser
```

The frontend should now be accessible at ```http://localhost:5173```.
