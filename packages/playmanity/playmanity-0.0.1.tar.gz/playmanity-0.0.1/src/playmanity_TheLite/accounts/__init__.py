from array import *
import asyncio
import json
import requests
class Bot():
    def __init__(self,login:str,password:str,token:str=None):
        self.login = login
        self.password = password
        self.token = token
    
    def run(self):
        async def go(self, login, password):
            loginres = await Auth.login(login,password)
            if loginres.status_code == 200:
                token = loginres.json()
                res = {"token": token["value"],"response": "Connected to SOON user"}
                return res
            else:
                status = loginres.status_code
                token = loginres.json()
                res = {"token": token["value"],"response": f"failed to run bot with status {status}"}
                return res
        
        self.token = asyncio.run(go(self,self.login,self.password))
        return (Bot(self.login,password=self.password,token=self.token))

class Auth():
    def __init__(self,login:str, password:str):
        pass

    async def login(login:str, password:str):
        
        req = requests.post('https://api.playmanity.com/sign-in', json={"username": login, "password": password})
        return req