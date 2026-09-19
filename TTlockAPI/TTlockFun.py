import json
import requests
import time
from datetime import datetime
with open("TTlockAPI/ttlock_tokeny.json",encoding="utf-8") as plik: # Opening files and getting jsons api parameters (some confidential)
    daneAccess=json.load(plik)
with open("TTlockAPI/payload.json",encoding="utf=8") as plik2:
    danePayload=json.load(plik2)
def LockList(daneAccess=daneAccess,danePayload=danePayload): # Listing all locks on ttlock account
    url='https://euapi.ttlock.com/v3/lock/list'
    data={ # data in our api request
            "clientId": danePayload["clientId"],
            "accessToken": daneAccess["access_token"],
            "pageNo": 1,
            "pageSize": 100,
            "date": int(time.time())*1000
        }
    records=requests.post(url,params=data) #Request that return list of locks
    if not records.ok:
        print(f"Sth wrong with LockList for TTlock details:\n{records.json()}")
        return -1
    RecDict=records.json()
    FormRec=[{"alias": el["lockAlias"],"Id" : el["lockId"], "group" : el['lockVersion']['groupId'] }for el in RecDict["list"]] #RecDict formated for my needs
    return FormRec
def SetPassword(lockId,end:tuple,start=(-1,-1,-1),daneAccess=daneAccess,danePayload=danePayload,endHour=(14,0,0),startHour=(0,0,0)):#Setting passwords on lock with Id the password are temporary determined by start(optional) and end
    url="https://euapi.ttlock.com/v3/keyboardPwd/get"
    end_dt=datetime(int(end[0]),int(end[1]),int(end[2]),endHour[0],endHour[1],endHour[2])
    if start==(-1,-1,-1):
        start_dt=datetime.now()
    else:
        start_dt=datetime(start[0],start[1],start[2],startHour[0],startHour[1],startHour[2])
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)
    data={
        "clientId": danePayload["clientId"],
        "accessToken": daneAccess["access_token"],
        "lockId" : lockId,
        "keyboardPwdType" : 3,
        "startDate" : start_ms,
        "endDate" : end_ms,
        "date" : int(time.time())*1000,
    }
    PassId=requests.get(url=url,params=data)
    if not PassId.ok:
        print(f"Sth wrong with SetPassword for TTlock details:\n{PassId.json()}")
        return -1
    return PassId.json()
if __name__=="__main__":
    print(LockList())
