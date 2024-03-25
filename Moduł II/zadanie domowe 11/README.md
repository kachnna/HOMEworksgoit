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
