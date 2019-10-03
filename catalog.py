from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import string
from database_setup import Base, User, Category, Item

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)



engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
dbsession.autoflush = True

#READ fuctions

@app.route('/')
@app.route('/catalog/')
def viewCatalog():
    category = dbsession.query(Category).all()

    return render_template('catalog.html', category = category)

@app.route('/catalog/<int:category_id>/')
def viewCategory(category_id):
    category = dbsession.query(Category).filter_by(id=category_id)
    item = dbsession.query(Item).filter_by(category=category_id)

    return render_template('category.html', category = category, item = item)

@app.route('/catalog/<int:category_id>/<int:item_id>/')
def viewItem(category_id, item_id):
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    return render_template('item.html', item = item, c = category)

#functions requiring login funtionality (CREATE, UPDATE, DELETE)

@app.route('/catalog/create', methods=['GET', 'POST'])
def createItem():
    if request.method == 'POST':
        newItem = Item(
            uid=1, #TODO:Change to accept uid
            name=request.form['name'],
            category=int(request.form['category']),
            description=request.form['description']
        )
        dbsession.add(newItem)
        dbsession.flush()
        dbsession.commit()
        return redirect(
            url_for('viewItem', item_id = newItem.id, category_id = newItem.category)
        )
    else:
        #categories = dbsession.query(Category).all()
        return render_template('create.html')
    
@app.route('/catalog/<int:category_id>/<int:item_id>/edit')
def editItem():
    return "Edited"

@app.route('/catalog/<int:category_id>/<int:item_id>/delete')
def deleteItem():
    return "Deleted"

#API related functions and paths

@app.route('/catalog/json')
def json():
    return "JSON API"
    
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8001)