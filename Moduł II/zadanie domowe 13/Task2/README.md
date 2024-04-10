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
4. **
 ```
python manage.py migrate 
 ```
5. **
```
python manage.py runserver
```
