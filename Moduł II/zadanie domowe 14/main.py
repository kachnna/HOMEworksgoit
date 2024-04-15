import uvicorn
from fastapi import FastAPI
from src.routes import contacts, auth, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ipaddress import ip_address
from typing import Callable
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from src.conf.config import settings

origins = [
    "http://localhost:3000"
]

ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address(
    '172.16.0.0'), ip_address("127.0.0.1")]

app = FastAPI()


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                    decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello in my application!"}
