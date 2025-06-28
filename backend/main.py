from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Routers import Zastroy_router, User_router, Property_router, Analytics_router, Chat_router, DeveloperRating_router
from Database.DB_connection import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "*"  # для разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Zastroy_router.router)
app.include_router(User_router.router)
app.include_router(Property_router.router)
app.include_router(Analytics_router.router)
app.include_router(Chat_router.router)
app.include_router(DeveloperRating_router.router)


@app.get("/items/")
async def read_items():
    return [{"name": "Item 1"}]


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    create_tables()





