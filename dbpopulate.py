from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

print '[+] Connecting to database...'
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

print "[+] Creating User admin..."

admin = User(id=100, name="admin",
             email="atomar.cse18@chitkarauniversity.edu.in")
session.add(admin)
session.commit()

print "[+] Adding Items to Audio:"
i1 = Item(name="Audacity", id=1, category=1, uid=100)
i2 = Item(name="Audacious", id=2, category=1, uid=100)
i3 = Item(name="LMMS", id=3, category=1, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Browsers:"
i1 = Item(name="Chromium", id=4, category=2, uid=100)
i2 = Item(name="Firefox", id=5, category=2, uid=100)
i3 = Item(name="Surf", id=6, category=2, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Database:"
i1 = Item(name="Postgresql", id=7, category=3, uid=100)
i2 = Item(name="MongoDB", id=8, category=3, uid=100)
i3 = Item(name="Apache CouchDB", id=9, category=3, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Developer Tools:"
i1 = Item(name="Atom", id=10, category=4, uid=100)
i2 = Item(name="Code OSS", id=11, category=4, uid=100)
i3 = Item(name="Vim", id=12, category=4, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Gaming:"
i1 = Item(name="Super Tux Cart", id=13, category=5, uid=100)
i2 = Item(name="0 A.D.", id=14, category=5, uid=100)
i3 = Item(name="Half Life 2", id=15, category=5, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Operating Systems:"
i1 = Item(name="Arch Linux", id=16, category=6, uid=100)
i2 = Item(name="NetBSD", id=17, category=6, uid=100)
i3 = Item(name="Gentoo", id=18, category=6, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Theming/Ricing:"
i1 = Item(name="Compton", id=19, category=7, uid=100)
i2 = Item(name="Neofetch", id=20, category=7, uid=100)
i3 = Item(name="Lolcat", id=21, category=7, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to System:"
i1 = Item(name="Gparted", id=22, category=8, uid=100)
i2 = Item(name="Alacritty", id=23, category=8, uid=100)
i3 = Item(name="Urxvt Unicode", id=24, category=8, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

print "[+] Adding Items to Utilities:"
i1 = Item(name="Gotop", id=25, category=9, uid=100)
i2 = Item(name="Bat", id=26, category=9, uid=100)
i3 = Item(name="Bleachbit", id=27, category=9, uid=100)
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()
