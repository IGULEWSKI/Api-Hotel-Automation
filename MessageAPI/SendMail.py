import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv(dotenv_path="MessageAPI/api_token.env")
mail_key = os.getenv("MAIL_KEY","")
mail_address = os.getenv("MAIL_ADDRESS","")
def send_mail(to:str,content:str,subject:str,test=0): # Sending mails using smtp protocol
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']=mail_address
    msg['To']=to
    msg.set_content(content)
    try:
        if test==0:
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(mail_address,mail_key)
                smtp.send_message(msg)
        print(f"Mail sent to {to}.")
    except Exception as e:
        print(f"Sth wrong with sending mail {e}")
        return -1

if __name__ == "__main__":
    send_mail("test mail here",'Test','Test')
