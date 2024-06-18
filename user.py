from fastapi import APIRouter
from .database import session, ENGINE
from .schemas import UserModel
from .models import User
from fastapi import HTTPException, status,Depends
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer



session = session(bind=ENGINE)

user_router = APIRouter(prefix="/user")


@user_router.get("/")
async def get(status_code=status.HTTP_200_OK):
    user= session.query(User).all()
    context = [
        {
            "id": users.id,
            "username": users.username,
        }
        for users in user
    ]

    return jsonable_encoder(context)


@user_router.post("/create")
async def create(user: UserModel):
    check_user = session.query(User).filter(User.id == user.id).first()
    if check_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Allready exists")

    new_user = User(
        id=user.id,
        first_name=user.firstname,
        last_name=user.lastname,
        username=user.username,
        password=user.password,
        is_staff=user.is_staff,
        is_active=user.is_active,

    )
    session.add(new_user)
    session.commit()

    return user



@user_router.delete("/delete")
async def delete(user: UserModel):
    check_user = session.query(User).filter(User.id == user.id).first()
    if check_user:
        session.delete(check_user)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode = {**data, "exp": expire}
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


fake_users_db = {
    "john_doe": {
        "username": "john_doe",
        "password": "secret",
        "disabled": False,
    }
}


def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or password != user["password"]:
        return None
    return user


@user_router.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    user_info = authenticate_user(user.username, user.password)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bunday foydalanuvchi mavjud emas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="tokeni yoq")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="tokeni yoq")