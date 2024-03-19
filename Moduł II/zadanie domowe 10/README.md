## INSTRUCTION "QuoWeb" 

## Docker
1. **
  ```
  cd quowebapp 

  ```
2. **
  ```
  docker run --name QuoWeb-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

  ```
3. **
 ```
 pip install psycopg2 
 ```
4. ** W pliku settings wkleić
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '567234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
5. **
 ```
python manage.py migrate 
 ```
6. **
 ```
python manage.py runserver
```
