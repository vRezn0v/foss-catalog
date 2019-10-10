from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String())


class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    @property
    def serialize(self):
        return {
            'id'            :   self.id,
            'name'          :   self.name
            }

class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category = Column(Integer, ForeignKey('category.id'), nullable = False)
    uid = Column(Integer, ForeignKey('user.id'), nullable = False)
    url = Column(String(250))
    
    @property
    def serialize(self):
        return {
            'name'          :   self.name,
            'id'            :   self.id,
            'category'      :   self.category,
            'uid'           :   self.uid,
            'description'   :   self.description,
            'url'           :   self.url;
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)