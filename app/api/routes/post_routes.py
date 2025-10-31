from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services import post_service
from app.core.security import decode_access_token
from app import models
from app.schemas.post_schema import PostCreate,PostResponse,PostUpdate

security = HTTPBearer()
router = APIRouter(prefix="/posts", tags=["Posts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db:Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.post("/",response_model=PostResponse)
def create_post(post_data:PostCreate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return post_service.create_post(db,post_data,current_user.id)

@router.get("/",response_model=list[PostResponse])
def get_posts(db:Session = Depends(get_db)):
    return post_service.get_posts(db)

@router.get("/{post_id}",response_model=PostResponse)
def get_post_by_id(post_id: int, db:Session = Depends(get_db)):
    post = post_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404,detail="Not found Post")
    return post

@router.put("/{post_id}",response_model=PostResponse)
def update_post(post_id: int,post_data:PostUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    updated = post_service.update_post(db,post_id,post_data,current_user.id)
    if not updated:
        raise HTTPException(status_code=403,detail="Not authorized or post not found")
    return updated

@router.delete("/{post_id}")
def delete_post(post_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    deleted = post_service.delete_post(db,post_id,current_user.id)
    if not deleted:
        raise HTTPException(status_code=403,detail="Not authorized or post not found")
    return {"message": "Post deleted"}




