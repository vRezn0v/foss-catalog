from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import string
from database_setup import Base, User, Category, Item


app = Flask(__name__)

engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
dbsession.autoflush = True

#Error Handler
@app.errorhandler(404)
def not_found(error):
    return render_template("404err.html")

#READ functions
@app.route('/')
@app.route('/catalog/')
def viewCatalog():
    """Reads categories from database and displays them."""
    category = dbsession.query(Category).all()

    return render_template('catalog.html', category = category)

@app.route('/catalog/<int:category_id>/')
def viewCategory(category_id):
    """Displays Items Contained in a Category"""
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(category=category_id)

    return render_template('category.html', category = category, item = item)

@app.route('/catalog/<int:category_id>/<int:item_id>/')
def viewItem(category_id, item_id):
    """Displays Information on a Specific Item"""
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    return render_template('item.html', item = item, c = category)

#functions requiring login functionality (CREATE, UPDATE, DELETE)

@app.route('/catalog/create', methods=['GET', 'POST'])
def createItem():
    #requires login
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
        return render_template('create.html')
    
@app.route('/catalog/<int:category_id>/<int:item_id>/edit',methods=['GET', 'POST'])
def editItem(category_id, item_id):
    #requires login
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=item.category).one()

    if request.method  == 'POST':
        item.id = item.id
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category = request.form['category']
        if request.form['url']:
            item.url = request.form['url']
        
        dbsession.add(item)
        dbsession.commit()
        flash("Item Updated Successfully.")
        return redirect(
            url_for('viewItem', category_id=category.id, item_id=item.id)
        )
    else:
        return render_template('edit.html', category=category, item=item)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    #requires login
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=item.category).one()

    if request.method == 'POST':
        dbsession.delete(item)
        dbsession.commit()
        flash('Deletion Success.')
        return redirect(url_for('viewCategory', category_id=category.id))
    
    else:
        return render_template('delete.html', category=category, item=item)

#API related functions and paths

@app.route('/catalog/json')
def catalogJSON():
    return "JSON API"
    
if __name__ == "__main__":
    app.secret_key = "peterparkerisspiderman"
    app.debug = True
    app.run(host='0.0.0.0', port=8001)