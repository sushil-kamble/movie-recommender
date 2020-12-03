#### Now Run the following commands one by one
```
pip install pipenv
pipenv install
```
```
pipenv run python manage.py migrate

pipenv run python manage.py createsuperuser
```
> Enter the necessary details...(username & password remember)
```
pipenv run python manage.py makemigrations

pipenv run python manage.py migrate
```

```
pipenv run python manage.py runserver
```