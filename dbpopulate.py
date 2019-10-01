from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

print '[+] Connecting to database...'
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

print "[+] Creating User admin..."

admin = User(id=100, name="admin", email="atomar.cse18@chitkarauniversity.edu.in")
session.add(admin)
session.commit()

print "[+] Adding Items to Audio:"
i1 = Item(name="Audacity", id=1001, category=1, uid=100)
i2 = Item(name="Audacious", id=1002, category=1, uid=100)
i3 = Item(name="LMMS", id=1003, category=1, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Browsers:"
i1 = Item(name="Chromium", id=2001, category=2, uid=100)
i2 = Item(name="Firefox", id=2002, category=2, uid=100)
i3 = Item(name="Surf", id=2003, category=2, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Database:"
i1 = Item(name="Postgresql", id=3001, category=3, uid=100)
i2 = Item(name="MongoDB", id=3002, category=3, uid=100)
i3 = Item(name="Apache CouchDB", id=3003, category=3, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Developer Tools:"
i1 = Item(name="Atom", id=4001, category=4, uid=100)
i2 = Item(name="Code OSS", id=4002, category=4, uid=100)
i3 = Item(name="Vim", id=4003, category=4, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Gaming:"
i1 = Item(name="Super Tux Cart", id=5001, category=5, uid=100)
i2 = Item(name="0 A.D.", id=5002, category=5, uid=100)
i3 = Item(name="Half Life 2", id=5003, category=5, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Operating Systems:"
i1 = Item(name="Arch Linux", id=6001, category=6, uid=100)
i2 = Item(name="NetBSD", id=6002, category=6, uid=100)
i3 = Item(name="Gentoo", id=6003, category=6, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Theming/Ricing:"
i1 = Item(name="Compton", id=7001, category=7, uid=100)
i2 = Item(name="Neofetch", id=7002, category=7, uid=100)
i3 = Item(name="Lolcat", id=7003, category=7, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to System:"
i1 = Item(name="Gparted", id=8001, category=8, uid=100)
i2 = Item(name="Alacritty", id=8002, category=8, uid=100)
i3 = Item(name="Urxvt Unicode", id=8003, category=8, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Utilities:"
i1 = Item(name="Gotop", id=9001, category=9, uid=100)
i2 = Item(name="Bat", id=9002, category=9, uid=100)
i3 = Item(name="Bleachbit", id=9003, category=9, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()