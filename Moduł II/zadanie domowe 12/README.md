## INSTRUCTION 

## Docker
1. **
  ```
  docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

  ```
2. **
  ```
alembic upgrade head 
  ```
3. **
 ```
 alembic revision --autogenerate -m 'Init'
 ```
4. **
 ```
  uvicorn main:app --host localhost --port 8000 --reload 
 ```
5. ** create test contacts
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
5. ** create test users
 ```
{
  "username": "kate_davis",
  "email": "kate.davis@example.com",
  "password": "MyPassw0rd2024"
}

 ```
 ```
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}

 ```
 ```
{
  "username": "emma_wilson",
  "email": "emma.wilson@example.com",
  "password": "Password123#"
}

```
```
{
  "username": "alex_smith",
  "email": "alex.smith@example.com",
  "password": "StrongSecret@123"
}

 ```

