import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="MessageAPI/api_token.env")
api_key = (os.getenv("SMSAPI_KEY"),os.getenv("SMSAPI_PASS"))
url="https://api2.smsplanet.pl/sms"

def Send_SMS(content:str,number:str,url=url,api_key=api_key,test=0):
    data={"key" : api_key[0],
          "password" : api_key[1],
          "from" : 'TEST',
          "msg" : content,
          "to" : number,
          "clear_polish" : 1,
          "test" : test
        }
    smssend=requests.post(url=url,data=data)
    if ( 'errorCode' not in smssend.json() ) and smssend.ok:
        print(f"Sent sms to {number} details: {smssend.json()}")
        return smssend.json()
    else:
        print(f"Sth wrong with SMSAPI details:\n{smssend.json()}")
        return -1

if __name__=="__main__":
    print(Send_SMS('test',"555555555",test=1))
