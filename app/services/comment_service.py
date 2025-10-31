from sqlalchemy.orm import Session
from app import models,schemas
from fastapi import HTTPException


def create_comment(db:Session,comment_data:schemas.CommentCreate,current_user_id:int):
    new_comment = models.Comment(**comment_data.dict(),user_id=current_user_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comments_by_post(db:Session,post_id:int):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

def update_comment(db:Session,comment_id:int,comment_data:schemas.CommentUpdate,current_user_id:int):
    update_comment_obj = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not update_comment_obj:
        return None
    if update_comment_obj.user_id != current_user_id:
        return "forbidden"
    for key,value in comment_data.dict().items():
        setattr(update_comment_obj,key,value)
    db.commit()
    db.refresh(update_comment_obj)
    return update_comment_obj

def delete_comment(db:Session,comment_id:int,current_user_id:int):
    delete_comment_obj = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not delete_comment_obj:
        return None
    if delete_comment_obj.user_id != current_user_id:
        return "forbidden"
    db.delete(delete_comment_obj)
    db.commit()
    return delete_comment_obj
    




