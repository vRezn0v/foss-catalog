from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash, make_response
from flask import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random
import string


import google.oauth2.credentials
import google_auth_oauthlib.flow

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

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    userinfo_url = "https://graph.facebook.com/v2.8/me"

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    session['access_token'] = token

    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    uid = getUserID(session['email'])
    if not uid:
        user_id = createUser(session)
    session['uid'] = uid

    output = ''
    output += '<h1>Welcome, '
    output += session['username']

    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % session['username'])
    return output
'''
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid State Parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    code = request.data

    auth_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets.json',
        ['securetoken.googleapis.com'])
    auth_flow.redirect_uri = url_for('gconnect', _external=True)

    credentials = auth_flow.fetch_token(code)
    authorization_url, state = auth_flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true')

    session['state'] = state
    return redirect(authorization_url)

    #token = credentials.access_token
    #url = 'https://accounts.google.com/o/oauth2/v2/auth/'

@app.route('/oauth2callback')
def oauth2callback():
    state  = session['state']
    auth_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secrets.json',
            ['securetoken.googleapis.com'])
    auth_flow.redirect_uri = url_for('oauth2callback', _external=True)
    auth_response = request.url
    auth_flow.fetch_token(authorization_response=auth_response)
    credentials = flow.credentials
    session['credetials']  = credentials_to_dict(credentials)
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
            description=request.form['description'],
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