## INSTRUCTION "QuoWeb"

## Docker

1. \*\* Create file env and fill wilt necessery information.

```
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

```

2. \*\*

```
cd quowebapp

```

3. \*\*

```
docker run --name {DATABASE_USER} -p {DATABASE_HOST}:{POSTGRES_PORT} -e POSTGRES_PASSWORD={DATABASE_PASSWORD} -d {DATABASE_NAME}


```

4. \*\*

```
pip install psycopg2
```

5. \*\*

```
python manage.py migrate
```

6. \*\*

```
python manage.py runserver
```
