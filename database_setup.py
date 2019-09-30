from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)


class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    @property
    def serialize(self):
        return {
            'name'      :   self.name
            'id'        :   self.id
        }

class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category = Column(Integer, ForeignKey('category.id'))
    uid = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'name'          :   self.name
            'id'            :   self.id
            'category'      :   self.category
            'uid'           :   self.uid
            'description'   :   self.description
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)