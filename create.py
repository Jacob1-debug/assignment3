import sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///listings.db')

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String

class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('clients.id'))
    list_agent_id = Column(Integer, ForeignKey('agents.id'))
    office_id = Column(Integer, ForeignKey('offices.id'))
    zip_code = Column(Integer)
    num_bathrooms = Column(Integer)
    num_bedrooms = Column(Integer)
    list_price = Column(Integer)
    list_date = Column(Date)
    status = Column(String)

    sale = relationship("Sale", backref="listing", uselist=False)

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    buyer_id = Column(Integer, ForeignKey('clients.id'))
    sale_agent_id = Column(Integer, ForeignKey('agents.id'))
    sale_price = Column(Integer)
    sale_date = Column(Date)
    sale_comission = Column(Integer)

class Office(Base):
    __tablename__ = 'offices'
    
    id = Column(Integer, primary_key=True)    
    name = Column(String)
    listings = relationship("Listing", backref="office")

class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    listings = relationship("Listing", backref="list_agent")
    sales = relationship("Sale", backref="sale_agent")
    comissions = relationship("MonthlyComission", backref="agent")

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    listings = relationship("Listing", backref="seller")
    purchases = relationship("Sale", backref="buyer")

class MonthlyComission(Base):
    __tablename__ = 'monthly_comissions'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    total_comission = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
        