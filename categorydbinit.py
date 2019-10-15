from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category

print '[+] Connecting to database...'
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

print '[+] Creating Categories...'

aud = Category(name="Audio", id=1)
session.add(aud)
session.commit()
print '[+] Created Category: Audio.'

browser = Category(name="Browsers", id=2)
session.add(browser)
session.commit()
print '[+] Created Category: Browsers.'

db = Category(name="Database", id=3)
session.add(db)
session.commit()
print '[+] Created Category: Database.'

dt = Category(name="Developer Tools", id=4)
session.add(dt)
session.commit()
print '[+] Created Category: Developer Tools.'

gaming = Category(name="Gaming", id=5)
session.add(gaming)
session.commit()
print '[+] Created Category: Gaming.'

os = Category(name="Operating Systems", id=6)
session.add(os)
session.commit()
print '[+] Created Category: Operating Systems.'

rt = Category(name="Theming/Ricing", id=7)
session.add(rt)
session.commit()
print '[+] Created Category: Theming/Ricing.'

sys = Category(name="System", id=8)
session.add(sys)
session.commit()
print '[+] Created Category: System.'

util = Category(name="Utilities", id=9)
session.add(util)
session.commit()
print '[+] Created Category: Utilities.'
