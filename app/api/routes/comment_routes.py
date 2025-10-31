from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.comment_schema import CommentCreate,CommentResponse,CommentUpdate
from app.services import comment_service
from .post_routes import get_current_user

router = APIRouter(prefix="/comments",tags=["Comments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/",response_model=CommentResponse)
def create_comment(comment_data:CommentCreate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    comment = comment_service.create_comment(db,comment_data,current_user.id)
    return comment

@router.get("/post/{post_id}",response_model=list[CommentResponse])
def get_comments_by_post(post_id: int, db:Session = Depends(get_db)):
    return comment_service.get_comments_by_post(db,post_id)

@router.put("/{comment_id}",response_model=CommentResponse)
def update_comment(comment_id:int,comment_data:CommentUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    updated = comment_service.update_comment(db,comment_id,comment_data,current_user.id)
    if updated == "forbidden":
        raise HTTPException(status_code=403,detail="You can only edit your own comments")
    if not updated:
        raise HTTPException(status_code=404,detail="Comment not found")
    return updated

@router.delete("/{comment_id}")
def delete_comment(comment_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    deleted = comment_service.delete_comment(db,comment_id,current_user.id)
    if deleted == "forbidden":
        raise HTTPException(status_code=403,detail="You can only edit your own comments")
    if not deleted:
        raise HTTPException(status_code=404,detail="Comment not found")
    return {"message":"Comment deleted"}
