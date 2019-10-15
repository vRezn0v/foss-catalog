from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash, make_response
from flask import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random
import string
from functools import wraps

from oauth2client import client

import httplib2
import json
import requests

from database_setup import Base, User, Category, Item

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Create Database Engine and disable threading for performance puropses
engine = create_engine("sqlite:///catalog.db",
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
dbsession.autoflush = True


# Anti-Forgery Token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template('login.html', client_id=CLIENT_ID, STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Callback Function For Google Login"""
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if not request.headers.get('X-Requested-With'):
        abort(403)

    code = request.data

    CLIENT_SECRET_FILE = 'client_secrets.json'

    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        code)

    http_auth = credentials.authorize(httplib2.Http())

    session['name'] = credentials.id_token['name']
    session['email'] = credentials.id_token['email']
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['uid'] = user_id
    print session.get('access_token')
    output = ''
    output += '<h1>Welcome, '
    output += session['name']
    output += '!</h1>'
    flash("you are now logged in as %s" % session['name'])
    return output


# Logout Routes
@app.route('/gdisconnect')
def gdisconnect():
    if session:
        print 'User name is: '
        print session['name']
        del session['uid']
        del session['name']
        del session['email']
        del session['state']
        session.clear()
        flash('Logged out successfully.')
        return redirect(url_for('viewCatalog'))


# Error Handler
@app.errorhandler(404)
def not_found(error):
    return render_template("404err.html")


# User related functions
def createUser(session):
    """Creates a new user in database"""
    newUser = User(name=session['name'],
                   email=session['email'])
    dbsession.add(newUser)
    dbsession.commit()
    user = dbsession.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Fetches UserInfo with id (redundant)"""
    user = dbsession.query(User).filter_by(id=user_id)
    return user


def getUserID(email):
    """Fetches UID with email"""
    try:
        user = dbsession.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Login Condition
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'name' not in session:
            flash('Login Required to Continue.')
            return redirect(url_for('viewCatalog'))
        return func(*args, **kwargs)
    return decorated_function


# READ functions
@app.route('/')
@app.route('/catalog/')
def viewCatalog():
    """Reads categories from database and displays them."""
    category = dbsession.query(Category).all()

    return render_template('catalog.html', category=category)


@app.route('/catalog/<int:category_id>/')
def viewCategory(category_id):
    """Displays Items Contained in a Category"""
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(category=category_id)

    return render_template('category.html', category=category, item=item)


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def viewItem(category_id, item_id):
    """Displays Information on a Specific Item"""
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=category_id).one()

    return render_template('item.html', item=item, c=category)


# functions requiring login functionality (CREATE, UPDATE, DELETE)
@app.route('/catalog/create', methods=['GET', 'POST'])
@login_required
def createItem():
    categories = dbsession.query(Category).all()

    if request.method == 'POST':
        newItem = Item(
            uid=session['uid'],
            name=request.form['name'],
            category=int(request.form['category']),
            description=request.form['description'],
            url=request.form['url']
        )
        dbsession.add(newItem)
        dbsession.flush()
        dbsession.commit()
        return redirect(
            url_for('viewItem', item_id=newItem.id,
                    category_id=newItem.category)
        )
    else:
        return render_template('create.html', c=categories)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=item.category).one()
    c = dbsession.query(Category).all()

    if int(session['uid']) != item.uid:
        flash("You are not authorized to perform this action.")
        return redirect(
            url_for('viewItem', category_id=category.id, item_id=item.id)
        )

    if request.method == 'POST':
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
        return render_template('edit.html', category=category,
                               item=item, categories=c)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=item.category).one()

    if int(session['uid']) != item.uid:
        flash("You are not authorized to perform this action.")
        return redirect(
            url_for('viewItem', category_id=category.id, item_id=item.id)
        )
    else:
        if request.method == 'POST':
            dbsession.delete(item)
            dbsession.commit()
            flash('Deletion Success.')
            return redirect(url_for('viewCategory', category_id=category.id))

        else:
            return render_template('delete.html', category=category, item=item)


# API related functions and paths
@app.route('/json/index')
def catalogJSON():
    categories = dbsession.query(Category).all()
    result = []
    for c in categories:
        result.append(c.serialize)
    return jsonify(Categories=result)


@app.route('/json/<int:category_id>')
def categoryJSON(category_id):
    items = dbsession.query(Item).filter_by(category=category_id).all()
    result = []
    for i in items:
        result.append(i.serialize)
    return jsonify(Items=result)


@app.route('/json/<int:category_id>/<int:item_id>')
def itemJSON(category_id, item_id):
    item = dbsession.query(Item).filter_by(id=item_id).one()
    result = item.serialize
    return jsonify(Item=result)


if __name__ == "__main__":
    app.secret_key = "peter parker is spiderman"
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
