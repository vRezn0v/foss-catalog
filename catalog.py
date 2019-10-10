from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash, make_response
from flask import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random
import string


import google.oauth2.credentials
import google_auth_oauthlib.flow

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from database_setup import Base, User, Category, Item

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

#flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secrets.json',)
#flow.redirect_uri = 'https://www.example.com/oauth2callback'

engine = create_engine("sqlite:///catalog.db", 
                        connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
dbsession.autoflush = True

#Anti-Forgery Token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    session['state'] = state
    return render_template('login.html', client_id=CLIENT_ID, STATE=state)


'''
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid State Parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'http://localhost:5000/catalog'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://oauth2.googleapis.com/tokeninfo?id_token=%s'
            % access_token)
    
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gid = credentials.id_token['sub']
    if result['user_id'] != gid:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's.", 401)
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_token = session.get('access_token')
    stored_gid = gid

    if stored_token is not None and gid == stored_gid:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['email'] = data['email']
    session['picture'] = data['picture']

    flash("Welcome %s" % session['username'])
    return redirect(url_for('viewCatalog'))

@app.route('/gdisconnect')
def gdisconnect():
    access_token = session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
'''


#Error Handler
@app.errorhandler(404)
def not_found(error):
    return render_template("404err.html")

#User related functions

def createUser(session):
    newUser =  User(name=session['username'],
                    email=session['email'],
                    picture=['picture'])
    dbsession.add(newUser)
    dbsession.commit()
    user = dbsession.query(User).filter_by(email=session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = dbsession.query(User).filter_by(id=user_id)
    return user

def getUserID(email):
    try:
        user = dbsession.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

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
    categories =  dbsession.query(Category).all()

    if request.method == 'POST':
        newItem = Item(
            uid=1, #TODO:Change to accept uid
            name=request.form['name'],
            category=int(request.form['category']),
            description=request.form['description']
            url=request.form['url']
        )
        dbsession.add(newItem)
        dbsession.flush()
        dbsession.commit()
        return redirect(
            url_for('viewItem', item_id = newItem.id, category_id = newItem.category)
        )
    else:
        return render_template('create.html', c = categories)
    
@app.route('/catalog/<int:category_id>/<int:item_id>/edit',methods=['GET', 'POST'])
def editItem(category_id, item_id):
    #requires login
    item = dbsession.query(Item).filter_by(id=item_id).one()
    category = dbsession.query(Category).filter_by(id=item.category).one()
    c = dbsession.query(Category).all()

    if request.method  == 'POST':
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
        return render_template('edit.html', category=category, item=item, categories = c)


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
    app.run(host='0.0.0.0', port=5000)