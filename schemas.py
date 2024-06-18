from pydantic import BaseModel
from typing import Optional


class RegisterModel(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


class LoginModel(BaseModel):
    username: str
    password: str


class CategoryModel(BaseModel):
    id: Optional[int]
    name: str

class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: float
    category_id: Optional[int]


class OrderModel(BaseModel):
    id: Optional[int]
    user_id: int
    product_id: int



class UserModel(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


"""class Token(BaseModel):
    access_token: str
    token_type: str"""

class JWTModel(BaseModel):
    authjwt_secret_key: str=  '34d48611a054e230745fce12d3ec2b634fe142665a2a77a94fd6979cf2b70904'