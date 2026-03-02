from sqlalchemy import create_engine, Column, String, Integer, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import json

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String)
    region = Column(String)
    empCode = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'name': self.name,
            'region': self.region,
            'empCode': self.empCode
        }

class Client(Base):
    __tablename__ = 'clients'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    region = Column(String)
    empCode = Column(String)
    data = Column(Text) # Store full JSON object for flexibility

    def to_dict(self):
        d = json.loads(self.data) if self.data else {}
        d['id'] = self.id
        return d

class Product(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    data = Column(Text)

    def to_dict(self):
        d = json.loads(self.data) if self.data else {}
        d['id'] = self.id
        d['stock'] = self.stock
        return d

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(String, primary_key=True)
    clientId = Column(String, ForeignKey('clients.id'))
    total = Column(Float, default=0.0)
    createdAt = Column(String)
    data = Column(Text)

    def to_dict(self):
        d = json.loads(self.data) if self.data else {}
        d['id'] = self.id
        return d

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(String, primary_key=True)
    productId = Column(String, ForeignKey('products.id'))
    quantity = Column(Integer)
    data = Column(Text)

    def to_dict(self):
        d = json.loads(self.data) if self.data else {}
        d['id'] = self.id
        return d

class Request(Base):
    __tablename__ = 'requests'
    id = Column(String, primary_key=True)
    clientId = Column(String, ForeignKey('clients.id'))
    status = Column(String)
    data = Column(Text)

    def to_dict(self):
        d = json.loads(self.data) if self.data else {}
        d['id'] = self.id
        return d

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String, primary_key=True)
    clientId = Column(String, ForeignKey('clients.id'))
    amount = Column(Float)
    date = Column(String)
    data = Column(Text)

    def to_dict(self):
        d = json.loads(self.data) if self.data else {}
        d['id'] = self.id
        return d

# Setup DB
engine = create_engine('sqlite:///billing.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
