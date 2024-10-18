import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
from model import EMAILSENT
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import create_engine




def mailu(listu):
    load_dotenv()
    
    result = ''

    for title, date, link in listu:
        result+=f"\n\tTitle:{title} \n \tDate:{date} \n \tLink:{link}" + "\n"
    print(result)

    subject= "!!INCOME TAX UPDATE!! INCOMETAXINDIA has updated their site"
    body='''\
    hello,
    Here is the list of updated titles from incometaxindia site.
    Main Site Link: https://incometaxindia.gov.in/Pages/communications/circulars.aspx
    
    The following titles have been updated:
    {result}
    regards,
    SIV
    '''.format(result=result)

    print(body)
    email_sender=os.getenv("EMAIL_SENDER")
    email_password=os.getenv("EMAIL_PASSWORD")
    email_receivers=os.getenv("EMAIL_RECEIVER").split(",")
    print(email_receivers)




    em = EmailMessage()
    em['From']=email_sender
    em['To'] = ', '.join(email_receivers) 
    em['Subject']=subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
        print(f"email sent to {email_receivers}")
    
    DATABASE_URL = 'sqlite:///example.db'
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session=Session()
    email_reciever_string=",".join(email_receivers)
    email=EMAILSENT(sentto=email_reciever_string,senttime=datetime.now())
    session.add(email)
    session.commit()
    session.close()
        