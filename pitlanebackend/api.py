from ninja import NinjaAPI
from ninja import Schema
from ninja.responses import Response
from django.contrib.auth.models import User
from typing import List

api = NinjaAPI()

class UserOut(Schema):
    id:int
    first_name:str
    last_name:str
    username:str
    email:str

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