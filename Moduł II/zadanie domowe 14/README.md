## INSTRUCTION

## Docker

1. \*\*

```
docker-compose up -d
```

2. \*\*
   Create file env example

```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=567234
POSTGRES_PORT=5432

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

SECRET_KEY=secret_key
ALGORITHM=HS256

MAIL_USERNAME=example@meta.ua
MAIL_PASSWORD=secretPassword
MAIL_FROM=example@meta.ua
MAIL_PORT=465
MAIL_SERVER=smtp.meta.ua

REDIS_HOST=localhost
REDIS_PORT=6379


CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRECT=
```

3. \*\*

```

```

4. \*\*

```
 uvicorn main:app --host localhost --port 8000 --reload
```

5. \*\* create test contacts

```
{
 "name": "John",
 "lastname": "Doe",
 "email": "johndoe@example.com",
 "phone": "123456789",
 "birthday": "1990-01-01",
 "notes": "string"
}
```

```
{
 "name": "Jane",
 "lastname": "Smith",
 "email": "jane.smith@emailprovider.com",
 "phone": "987654321",
 "birthday": "1985-12-15",
 "notes": "string"
}

```

```
{
 "name": "Alice",
 "lastname": "Johnson",
 "email": "alice.johnson@example.org",
 "phone": "555555555",
 "birthday": "1978-06-30",
 "notes": "string"
}
```

```
{
  "name": "Bob",
  "lastname": "Brown",
  "email": "bob.brown@example.net",
  "phone": "999888777",
  "birthday": "1982-03-10",
  "notes": "string"
}

```

5. \*\* create test users

```
{
 "username": "john_doe",
 "email": "john.doe@example.com",
 "password": "Secure123!"
}


```

```
{
 "username": "alice_j",
 "email": "alice.johnson@example.org",
 "password": "Pass123!"
}

```

```
{
 "username": "bob_b",
 "email": "bob.brown@example.net",
 "password": "Brown456"
}

```

```
{
  "username": "jane_s",
  "email": "jane.smith@emailprovider.com",
  "password": "Smith123"
}


```
