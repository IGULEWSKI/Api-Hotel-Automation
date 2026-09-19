import requests
import json
def get_AccessTokken():
    url = "https://euapi.ttlock.com/oauth2/token"


    header = {'Content-Type' : 'application/x-www-form-urlencoded'}
    with open("TTLockAPI/payload.json", "r", encoding="utf-8") as plik1:
        payload = json.load(plik1)

    response = requests.post(url, headers=header, data=payload)
    if not response.ok:
        return "Couldn't generate AccessTokken"
    dane=response.json()
    if "access_token" in dane:
        with open("TTLockAPI/ttlock_tokeny.json", "w", encoding="utf-8") as plik2:
                    json.dump(dane, plik2, indent=4, ensure_ascii=False)
    return "Success"
if __name__=="__main__":
    print(get_AccessTokken())
