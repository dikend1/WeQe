from sqlalchemy.orm import Session
from app import models,schemas
from fastapi import HTTPException

def create_post(db:Session,post_data:schemas.UserCreate,user_id:int):
    post = models.User(**post_data.dict(),ownew_id = user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db:Session,skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post_by_id(db:Session,post_id):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail="Task not found")
    return post

def update_post(db:Session,post_id:int,post_data:schemas.PostUpdate,user_id:int):
    post = db.query(models.Post).filter(models.Post.id==post_id,models.Post.owner_id == user_id).first()
    if not post:
        return None
    for key,value in post_data.dict().items():
        setattr(post,key,value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db:Session,post_id:int,user_id:int):
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == user_id)
    if not post:
        return None
    db.delete(post)
    db.commit()
    return post

