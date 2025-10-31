from fastapi import FastAPI
from app.api.routes import auth_routes,post_routes,comment_routes
from app.db.base import Base
from app.db.session import engine


app = FastAPI(title="WeQe")

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(post_routes.router)
app.include_router(comment_routes.router)