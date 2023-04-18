from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import Optional
from Class import *
import RenterInstance as r
import DealerInstance as d 
import CarInstance as c
import uvicorn
class UserModel(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    user_role: Optional[str] = None


app = FastAPI()
system = System()
user_instance_list = r.renter_instance_list + d.dealer_instance_list
for acc in user_instance_list:
    system.add_account(acc)

accounts = []

thisuser = [User()]
guest = User()

@app.get("/")
async def read_root():
    print(thisuser[0].get_name())
    return {'data': thisuser[0].get_name()}
@app.post("/register")
async def register(user:UserModel):
    for detail in user.dict().keys():
        if user.dict()[detail] == '' or user.dict()[detail] == None:    
            return {'message':'Please fill all requirements'}
    if system.check_used_username(user.username):
        return {'message':'This username is used'}
    if user.user_role == 'Renter':
        new_user = Renter(name=user.name,username=user.username, password=user.password)
    elif user.user_role == 'Dealer':
        new_user = Dealer(name=user.name,username=user.username, password=user.password)
    system.add_account(new_user)
    return {"message" : "Register success!"}

@app.get("/account")
async def get_accounts():
    for account in system.get_account_list():
        temp = {}
        temp['name'] = account.get_name()
        temp['profile_image'] = account.get_profile_image()
        temp['gender'] = account.get_gender()
        temp['birth_date'] = account.get_birth_date()
        temp['info'] = account.get_info()
        temp['username'] = account.get_username()
        temp['password'] = account.get_password()
        accounts.append(temp)
    return { "data" : accounts}

@app.get("/login")
async def login(username:str, password:str):
    logic,returned_user = system.check_account(username,password)
    if logic:
        thisuser.pop()
        thisuser.append(returned_user)
        return {'data': 'Login success, ' + 'Welcome back! ' + str(type(returned_user)) + ' ' + returned_user.get_name()}
    
    raise HTTPException(401,detail='Login failed')
@app.get("/logout")
async def logout():
    thisuser.pop()
    thisuser.append(guest)
    return {'message': 'Logged out!'}

for car in c.Car_instance_list:
    system.add_car(car)
@app.get("/car/{car_id}")
async def view_car(car_id:str):
    for car in system.get_car_list():
        if car_id == car.get_car_ID():
            temp = {}
            temp['brand'] = str(car.get_brand())
            temp['car_id'] = car.get_car_ID()
            
            return {"data": temp}

if __name__ == "__main__":
     uvicorn.run("login_with_api:app", host="127.0.0.1", port=8000, reload=True)