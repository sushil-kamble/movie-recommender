# Recommendation System

My Python Version 3.7.9
#### Go to the root folder and Run the following commands one by one
```
pip install pipenv
pipenv install
```
####
You need redis-server, for that click on the link below.

[Download, Extract and Run redis-server.exe](https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip)

redis-server.exe should run in background.
```
pipenv shell
python manage.py migrate
python manage.py createsuperuser
```
> Enter the necessary details...(username & password remember)


```
python manage.py runserver
```