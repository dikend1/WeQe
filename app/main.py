from fastapi import FastAPI
from app.api.routes import auth_routes
from app.db.base import Base
from app.db.session import engine


app = FastAPI(title="WeQe")

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
