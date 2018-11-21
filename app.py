#!/usr/bin/env python3

"""The second project of the Udacity Full-Stack Engineer Nanodegree.

An item catalog that utilizes the Flask framework to create a web application
with authentication and authorization for users to read, add, update, and
delete items they have placed inside the application.
"""

# import needed modules
from flask import Flask, render_template, url_for, request, redirect
from flask import jsonify, make_response, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Items
from flask import session as login_session
import random
import string
import json
import httplib2
import requests
from login_decorator import login_required
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# flask instance
app = Flask(__name__)

# Client Secrets
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


# connect to database
engine = create_engine('sqlite:///itemcatalog.db', pool_pre_ping=True)
Base.metadata.bind = engine

# create db session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    """Create user if user is not in the database."""
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Retrieve user information."""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Retrieve user ID."""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# -----------------------------------------
#     LOG IN - GCONNECT ROUTING START HERE
# ------------------------------------------


@app.route('/login')
def login():
    """Allows user to login into application."""
    # Create anti forgery state token
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    gdisconnect()
    del login_session['gplus_id']
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']

    return redirect(url_for('showCategories'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Validates state token and allows user to login with Google."""
    # validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request & parse response
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    response_str = response.decode('utf-8')
    result = json.loads(response_str)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                        'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; '
    output += '"-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnects user from the application."""
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showCategories'))
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# -----------------------------------------
#     LOG IN - GCONNECT ROUTING END HERE
# ------------------------------------------


# -----------------------------------------
#     APPLICATION ROUTING START HERE
# ------------------------------------------

# Homepage


@app.route('/')
@app.route('/catalog/')
def showCategories():
    """Displays all categories and items."""
    # get all categories, items and display them
    categories = session.query(Category).all()
    items = session.query(Items).all()
    return render_template('categories.html',
                           categories=categories, items=items)

# Show a specific category with its specific Items


@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCategory(catalog_id):
    """Displays a specific category with its items."""
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=catalog_id).one()
    categoryName = category.name
    items = session.query(Items).filter_by(category_id=catalog_id).all()
    itemCount = session.query(Items).filter_by(category_id=catalog_id).count()

    return render_template('category.html',
                           categories=categories,
                           items=items,
                           categoryName=categoryName,
                           itemCount=itemCount)

# Show specific item


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showItem(catalog_id, item_id):
    """Displays a specific item."""
    items = session.query(Items).filter_by(id=item_id).one()
    creator = getUserInfo(items.user_id)
    return render_template('items.html', items=items, creator=creator)


# Add an item


@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def addItems():
    """Adds an item into the database."""
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        if not request.form['name']:
            flash("Please add item name")
            return redirect(url_for('addItems.html'))

        if not request.form['description']:
            flash("Please add item description")
            return redirect(url_for('addItems.html'))
        # get form data
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        creator = login_session['user_id']

        newItem = Items(name=name, description=description,
                        category_id=category, user_id=creator)
        session.add(newItem)
        session.commit()
        flash("Your item as been added!")
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category).all()
        return render_template('addItems.html', categories=categories)

# Edit an item


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(catalog_id, item_id):
    """Edits an item in the database."""
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Items).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)

    # check if the user logged in is owner of item
    if creator.id != login_session['user_id']:
        return redirect('/login')

    categories = session.query(Category).all()

    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash("Your item as been updated!")

        return redirect(url_for('showItem',
                        catalog_id=item.category_id,
                        item_id=item.id))
    else:
        return render_template('editItem.html',
                               categories=categories,
                               item=item)

# Delete an item


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(catalog_id, item_id):
    """Deletes an item from the database."""
    # check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Items).filter_by(id=item_id).first()
    creator = getUserInfo(item.user_id)

    # check if logged in user is owner of item
    if creator.id != login_session['user_id']:
        return redirect('/login')

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Your item as been deleted!")
        return redirect(url_for('showCategory', catalog_id=item.category_id))
    else:
        return render_template('deleteItem.html', item=item)


# -----------------------------------------
#     APPLICATION ROUTING ENDS HERE
# ------------------------------------------


# -----------------------------------------
#     JSON ENDPOINTS ROUTING STARTS HERE
# ------------------------------------------


@app.route('/catalog/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/catalog/<int:catalog_id>/JSON')
@app.route('/catalog/<int:catalog_id>/items/JSON')
def showCategoryJSON(catalog_id):
    categories = session.query(Category).filter_by(id=catalog_id).one()
    items = session.query(Items).filter_by(category_id=catalog_id).all()
    return jsonify(items=[item.serialize for item in items],
                   categories=[categories.serialize])


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/JSON')
def showItemsJSON(catalog_id, item_id):
    category = session.query(Category).filter_by(id=catalog_id).one()
    items = session.query(Items).filter_by(id=item_id).one()
    return jsonify(items=[items.serialize],
                   category=[category.serialize])

# -----------------------------------------
#     JSON ENDPOINTS ROUTING ENDS HERE
# ------------------------------------------


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8080)
