from fastapi import FastAPI
import uvicorn

from src.routes import auth, contacts

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Welcome in my application!"}
