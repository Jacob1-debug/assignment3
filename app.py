from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from create import Office

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

#the Office!
class Offices(db.Model):
    name = db.Column(db.String(80), index = True, unique = True) # Name client
   
    #Printout of Offices info
    def __repr__(self):
        return "{} in: {},{}".format(self.id, self.month, self.year)

#Declaring details of client
class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    surname = db.Column(db.String(80), unique = False, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    #get a nice printout for Details
    def __repr__(self):
        return "Name ID: {}, email: {}".format(self.id, self.email)

#Declaring details of Agent
class Agent(db.Model):
    name = db.Column(db.String(50), index = True, unique = False)
    surname = db.Column(db.String(80), unique = False, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    #get a nice printout for Details
    def __repr__(self):
        return "Name ID: {}, email: {}".format(self.id, self.email)

        
import routes