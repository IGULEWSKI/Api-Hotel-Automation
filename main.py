from MessageAPI.SendSMS import Send_SMS
import TTlockAPI.TTlockFun as ttapi
from HotResAPI.Reservations import List_Reservations
from datetime import datetime
import secrets
import json
import KillJason
import os
from dotenv import load_dotenv
from MessageAPI.SendMail import send_mail

load_dotenv(dotenv_path="secret.env")
with open("DoneRes.json","r",encoding="utf-8") as Jason: # its json file that make sure we dont send message for same reservation twice
    done_res=set(json.load(Jason))

def main():
    global done_res
    Locks=ttapi.LockList()


    if Locks == -1:
        return 1

    #Making a dict that pairs lock id with this lock alias (I know there arent any duplicates in sytem so it works)
    alias_dict={lock['alias']:lock['Id'] for lock in Locks}

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    reservations=List_Reservations(today) #Reservation after today
    if reservations == -1:
        return 1
    for res in reservations:
        if res["id"] not in done_res and res["arrival"]==today:
            hasla=[]
            #Setting password on lock
            for room in res['rooms']:
                haslo = "".join(secrets.choice("0123456789") for _ in range(4))
                print(f"Generated password {haslo}")

                departure=tuple(res["departure"].split("-"))
                reshasla=ttapi.SetPassword(alias_dict[room['title']],departure) #It works because in ttlock app we set all aliases of locks equal to name of room in hotres
                if reshasla==-1:
                     return 1
                hasla.append((room['title'],haslo)) # not really user friendly needs polish (not language xd)

            #Sending messages to client
            phone_prefix=res["phone"][0]
            if phone_prefix=='48' or phone_prefix=='': #We check if customer is polish otherwise we send only mail
                Subject = "Rezerwacja pokoju"
                Szablon = f"Dziękujemy za rezerwacje,\noto kod/y do drzwi {hasla}." # this is our Message we are going to send with password to doors (its early version)

                if res["phone"][1]!='':
                    Sms_Res=Send_SMS(Szablon,res["phone"][1],test=1) # set test=0 before use
                    print(f"\nWysłano sms pod numer {res["phone"]} o treści",
                    f"\n{Szablon})",)

                    if Sms_Res==-1:
                        return 1
            else:
                Subject="Room reservation"
                Szablon=f"Thank you for your reservation,\nhere's your door passcode {hasla}."
            
            send_mail(res["mail"],Szablon,Subject,test=1) # set test=0 before use
            print(f"\nWysłano maila pod {res["mail"]} o treści",
                f"\n{Szablon})",)
            print('---------------------\n')
            done_res.add(res["id"])
            

            
    if len(done_res)>100:
        KillJason.wipe()
    with open("DoneRes.json","w",encoding="utf-8") as Jason:
        json.dump(list(done_res),Jason,indent=4)
    return 0

admin_tel=os.getenv("ADMIN_TEL","") #getting admin number from .env file so it wont leak in github repo
if __name__ == "__main__":
    if main()==1:
        with open("DoneRes.json","w",encoding="utf-8") as Jason:
            json.dump(list(done_res),Jason,indent=4)
        print("Sending alert sms to administrator if possible:")
        if Send_SMS("Reservation app has isuues fix it",admin_tel,test=1)!=-1:
            print("Success")
        else:
            print("Couldn't send sms")


