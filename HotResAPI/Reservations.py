import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(dotenv_path="HotResAPI/ApiAuth.env")
AuthKey=os.getenv("HRAuth_Key")
ApiKey=os.getenv("HRAPI_Key")

def List_Reservations(arrival_date,AuthKey=AuthKey,ApiKey=ApiKey): # Extracting list of recent reservations and formating it
    urlres=f"https://panel.hotres.pl/api_reservations?auth={AuthKey}&apikey={ApiKey}"
    data={
        "arrival_date" : arrival_date,
        "mode" : 'reception'
    }
    res=requests.get(url=urlres,params=data)
    if not res.ok:
        print("There was an problem with HotResAPI")
        return -1
    Tabela=res.json()
    ForTab = [{"id" : el["id"], "name" : (el["first_name"],el["last_name"]), "phone": (el["phone_prefix"],el["phone"]),"mail":el["email"], "arrival" : el["arrival_date"], "departure" : el["departure_date"], "rooms": [{"type_id": room["type_id"],"title":room["title"]} for room in el["rooms"]]} for el in Tabela] #Formated list
    return ForTab
if __name__=="__main__":
    now = datetime.now()
    print(List_Reservations(now.strftime("%Y-%m-%d")))
