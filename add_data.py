# from sqlalchemy.orm import Session
from requests import Session
from create import *
import random
import datetime

from app import db, Offices, Client, Agents
import os

random.seed(404)
session = Session(bind=engine)

if os.path.exists('myDB.db'):
  os.remove('myDB.db')
  
db.create_all()

#add datas - Client
r1 = Client(id = 123, name = 'Ann', surname = 'Rotich', email = 'Rotich@gmail')
r2 = Client(id = 345, name = 'Sam', surname = 'Kwambai', email = 'Kwambai@example.edu')
r3 = Client(id = 450, name = 'Lewis', surname = 'CS', email = 'Lewis@example.com')
r4 = Client(id = 568, name = 'Second', surname = 'Smalls', email = 'Second@example.com')
r5 = Client(id = 753, name = 'Tovia', surname = 'Yeni', email = 'yeni@example.edu')
r6 = Client(id = 653, name = 'curator', surname = 'Grey', email = 'grey@example.com')

db.session.add(r1)
db.session.add(r2)
db.session.add(r3)
db.session.add(r4)
db.session.add(r5)
db.session.add(r6)

try:
  db.session.commit()
except Exception:
  db.session.rollback()


#Add - Offices
r1 = Offices(name="California")
r2 = Offices(name="Ohio")
r3 = Offices(name="Seattle")
r4 = Offices(name="Works")
r5 = Offices(name="Good Cape")

db.session.add(r1)
db.session.add(r2)
db.session.add(r3)
db.session.add(r4)
db.session.add(r5)
try:
  db.session.commit()
except Exception:
  db.session.rollback()

#Add - Agents
agen1 = Agents(name = 'Guang', surname = 'super', email = 'Guangch@gmail')
agen2 = Agents(name = 'Sam', surname = 'Christ', email = 'Sam@example.edu')
agen3 = Agents(name = 'Mr', surname = 'CS', email = 'Mr@example.com')
agen4 = Agents(name = 'John', surname = 'Smalls', email = 'John@example.com')


db.session.add(agen1)
db.session.add(agen2)
db.session.add(agen3)
db.session.add(agen4)

try:
  db.session.commit()
except Exception:
  db.session.rollback()

#Add Listings

for i in range(100):
    session.add(Listing(
    seller_id=random.randrange(1,9),
    list_agent_id=random.randrange(1,11),
    office_id=random.randrange(1,9),
    num_bedrooms=random.randrange(1,5),
    num_bathrooms=random.randrange(1,3),
    list_price=random.randrange(100000, 2500000),
    zip_code=random.randrange(10000,100000),
    list_date=datetime.date(2022,random.randrange(1,4),random.randrange(1,28)),
    status='available'
    ))

#Add Sales

def get_comission(price):
    if price<100000:
        return round(price*0.1)
    elif price<200000:
        return round(price*0.075)
    elif price<500000:
        return round(price*0.06)
    elif price<1000000:
        return round(price*0.05)
    else:
        return round(price*0.04)

def sell_house(listing_id, buyer_id, sale_agent_id, sale_price, sale_date):
    
    #Ensure the listing exists and the house was available
    try:
        listing=session.query(Listing).filter_by(id=listing_id).one()
    except:
        print("Listing not-existent")
        return None

    if listing.status!='available':
        print(listing.status)
        print("House unavailable")
        return None
    
    #Updates the listing status and adds the sale entry
    listing.status='sold'
    session.add(Sale(
        listing_id=listing_id,
        buyer_id=buyer_id,
        sale_agent_id=sale_agent_id,
        sale_price=sale_price,
        sale_date=sale_date,
        sale_comission=get_comission(sale_price)
    ))

#sell_house(list_id, buyer_id, sale_agent, sale_price, sale_date)
for i in range(1,101):

    #Create -sale of about 80% 
    if random.randrange(0,100)<80:
        listing=session.query(Listing).filter_by(id=i).one()
        sell_house(i,
            random.randrange(1,9),
            random.randrange(1,11), 
            listing.list_price, 
            listing.list_date+datetime.timedelta(days=random.randrange(1,15)))

session.commit()
db.session.close()

