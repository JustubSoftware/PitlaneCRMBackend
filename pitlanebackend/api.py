from typing import Optional, List
from ninja import NinjaAPI
from ninja import Schema
from ninja.responses import Response
from django.contrib.auth.models import User

api = NinjaAPI()

class UserOut(Schema):
    id:int
    first_name:str
    last_name:str
    username:str
    email:str

class UserCreate(Schema):
    username:str
    email:str
    password:str
    first_name:Optional[str] = ""
    last_name:Optional[str] = ""

@api.get("/user", response=List[UserOut])
def get_all_users(request):
    users = User.objects.all()
    return users

@api.get("/user/{user_id}", response=UserOut)
def get_single_user(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return Response(
            {"detail": f"User with id {user_id} not found"},
            status=404
        )

@api.post("/user", response={201: UserOut, 400:dict})
def create_user(request, payload:UserCreate):
    if User.objects.filter(username=payload.username).exists():
        return Response({"detail": "Username already exists"}, status=400)
    
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name = payload.last_name
    )

    return Response(UserOut.from_orm(user), status=201)