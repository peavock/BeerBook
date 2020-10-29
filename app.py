import os

from flask import Flask, render_template, request, flash, redirect, session, g, request
from flask_debugtoolbar import DebugToolbarExtension
import requests
# from sqlalchemy.exc import Integrity Error

from forms import SignupForm, LoginForm, ReviewForm
from models import db, connect_db, User, Review, LikedBeer, TriedBeer, WishedBeer, Style, Category

app = Flask(__name__)


API_KEY = "dfdffcce0e73c5d909dde5471b0e5b8b"
CURR_USER_KEY = "curr_user"
API_BASE_URL = "https://sandbox-api.brewerydb.com/v2"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgres:///cicerone')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',"it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id 

def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def show_homepage():

    return render_template("base.html")

@app.route('/signup', methods = ["GET","POST"])
def signup_page():
    """Show the form to sign-up and process if post"""
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data


        new_user = User.signup(username, password)

        db.session.add(new_user)
        db.session.commit()

        do_login(new_user)

        user_id = session[CURR_USER_KEY]

        flash (f"Welcome to Cicerone {new_user.username}", "success")
        return redirect(f"/user/{user_id}")

    else:   
        return render_template("signup.html", form = form)

@app.route('/login', methods = ["GET","POST"])
def login_page():
    """Show the login form and log in if applicable"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            do_login(user)
            flash(f"Welcome back to Cicerone {user.username}!", "success")
            return redirect(f"/user/{user.id}")

    return render_template("login.html", form = form)

@app.route('/logout')
def logout():

    session.pop(CURR_USER_KEY)
    return redirect("/")

@app.route('/user/<user_id>', methods = ["GET"])
def show_user_page(user_id):

    categories = Category.query.all()

    return render_template('user/show.html',categories = categories)

@app.route('/category/<category_id>', methods = ["GET"])
def show_category_page(category_id):
    """Show a page that has a category name and all styles associated with it"""
    category = Category.query.get(category_id)
    styles = Style.query.filter_by(category_id = category_id).all()

    return render_template("beer/category.html", category = category, styles = styles)

@app.route('/style/<style_id>', methods = ["GET"])
def show_style_page(style_id):
    """Show a page that has a style name and all beers associated with it"""
    style_type = Style.query.get(style_id)
    # beer_ids = Style.query.filter_by(category_id = category_id).all()

    response = requests.get(f"{API_BASE_URL}/beers",
                        params = {'key':API_KEY, 'styleId' : style_id})

    beers = response.json()["data"]

    user_id = session[CURR_USER_KEY]

    tried_beer_ids = [beer.beer_id for beer in TriedBeer.query.filter_by(user_id = user_id).all() ]
    liked_beer_ids = [beer.beer_id for beer in LikedBeer.query.filter_by(user_id = user_id).all() ]
    wished_beer_ids = [beer.beer_id for beer in WishedBeer.query.filter_by(user_id = user_id).all() ]

    return render_template("/beer/style.html", style = style_type, beers = beers, tried_beer_ids = tried_beer_ids, liked_beer_ids = liked_beer_ids, wished_beer_ids = wished_beer_ids)

@app.route('/beer/<beer_id>', methods = ["GET"])
def show_beer_page(beer_id):
    """show a page with details on a beer and the reviews for it"""
    response = requests.get(f"{API_BASE_URL}/beers",
                        params = {'key':API_KEY,'ids':beer_id})
    
    beer = response.json()["data"][0]

    user_id = session[CURR_USER_KEY]

    reviews = Review.query.filter_by(beer_id = beer_id).all()

    tried_beer_ids = [beer.beer_id for beer in TriedBeer.query.filter_by(user_id = user_id).all() ]
    liked_beer_ids = [beer.beer_id for beer in LikedBeer.query.filter_by(user_id = user_id).all() ]
    wished_beer_ids = [beer.beer_id for beer in WishedBeer.query.filter_by(user_id = user_id).all() ]

    return render_template("beer/show.html", beer = beer, reviews = reviews, 
        tried_beer_ids = tried_beer_ids, liked_beer_ids = liked_beer_ids, wished_beer_ids = wished_beer_ids)

@app.route('/beer/review/<beer_id>', methods = ["GET","POST"])
def handle_review_page(beer_id):
    """Page with form to fill out review of beer and submit"""

    form = ReviewForm()
    response = requests.get(f"{API_BASE_URL}/beers",
                        params = {'key':API_KEY,'ids':beer_id})
    
    beer = response.json()["data"][0]


    user_id = session[CURR_USER_KEY]

    if form.validate_on_submit():

        new_review = Review(
            beer_name = beer["name"],
            user_id = user_id,
            beer_id = beer_id,
            rating = form.rating.data,
            text = form.text.data

        )

        db.session.add(new_review)
        db.session.commit()
        

        return redirect(f"/user/{user_id}/reviews")

    else:   
        return render_template("beer/review.html", form = form, beer = beer)

@app.route('/user/<user_id>/reviews', methods = ["GET"])
def show_user_reviews(user_id):
    """show a page with the reviews that a user has written"""

    user_reviews = Review.query.filter_by(user_id = user_id).all()

    return render_template("/user/reviews.html", user_reviews = user_reviews)

@app.route('/user/reviews/<review_id>/delete', methods = ["POST"])
def delete_review(review_id):
    """delete reviews"""

    del_review = Review.query.get(review_id)

    db.session.delete(del_review)
    db.session.commit()

    user_id = session[CURR_USER_KEY]

    return redirect(f"/user/{user_id}/reviews")

@app.route('/user/reviews/<review_id>/edit', methods = ["GET","POST"])
def edit_review(review_id):
    """edit a review"""

    edit_review = Review.query.get(review_id)

    form = ReviewForm(obj = edit_review)

    beer_id = edit_review.beer_id

    response = requests.get(f"{API_BASE_URL}/beers",
                        params = {'key':API_KEY,'ids':beer_id})

    beer = response.json()["data"][0]

    user_id = session[CURR_USER_KEY]

    if form.validate_on_submit():

        edit_review.rating = form.rating.data
        edit_review.text = form.text.data

        db.session.add(edit_review)
        db.session.commit()

        flash("Review Updated","success")

        return redirect(f"/user/{user_id}/reviews")

    else:
        return render_template("beer/editreview.html",form = form, beer = beer)


    

@app.route('/user/<user_id>/tried', methods = ["GET"])
def show_tried_beers(user_id):
    """show a page with the beers a user has tried"""

    tried_beer_ids = [beer.beer_id for beer in TriedBeer.query.filter_by(user_id = user_id).all() ]
    liked_beer_ids = [beer.beer_id for beer in LikedBeer.query.filter_by(user_id = user_id).all() ]
    wished_beer_ids = [beer.beer_id for beer in WishedBeer.query.filter_by(user_id = user_id).all() ]
    
    beers = []

    for beer_id in tried_beer_ids:
        response = requests.get(f"{API_BASE_URL}/beers",
                    params = {'key':API_KEY,'ids':beer_id})
    
        beer = response.json()["data"][0]

        beers.append(beer)

    return render_template("/beer/tried.html", beers = beers, tried_beer_ids = tried_beer_ids, liked_beer_ids = liked_beer_ids, wished_beer_ids = wished_beer_ids)

@app.route('/user/<user_id>/liked', methods = ["GET"])
def show_liked_beers(user_id):
    """show a page with the beers a user has liked"""
    
    tried_beer_ids = [beer.beer_id for beer in TriedBeer.query.filter_by(user_id = user_id).all() ]
    liked_beer_ids = [beer.beer_id for beer in LikedBeer.query.filter_by(user_id = user_id).all() ]
    wished_beer_ids = [beer.beer_id for beer in WishedBeer.query.filter_by(user_id = user_id).all() ]

    beers = []

    for beer_id in liked_beer_ids:
        response = requests.get(f"{API_BASE_URL}/beers",
                    params = {'key':API_KEY,'ids':beer_id})
    
        beer = response.json()["data"][0]

        beers.append(beer)

    return render_template("/beer/liked.html", beers = beers, tried_beer_ids = tried_beer_ids, liked_beer_ids = liked_beer_ids, wished_beer_ids = wished_beer_ids)

@app.route('/user/<user_id>/wished', methods = ["GET"])
def show_wished_beers(user_id):
    """show a page with the beers a user wants to try"""

    tried_beer_ids = [beer.beer_id for beer in TriedBeer.query.filter_by(user_id = user_id).all() ]
    liked_beer_ids = [beer.beer_id for beer in LikedBeer.query.filter_by(user_id = user_id).all() ]
    wished_beer_ids = [beer.beer_id for beer in WishedBeer.query.filter_by(user_id = user_id).all() ]
    
    beers = []

    for beer_id in wished_beer_ids:
        response = requests.get(f"{API_BASE_URL}/beers",
                    params = {'key':API_KEY,'ids':beer_id})
    
        beer = response.json()["data"][0]

        beers.append(beer)

    return render_template("/beer/wished.html", beers = beers, tried_beer_ids = tried_beer_ids, liked_beer_ids = liked_beer_ids, wished_beer_ids = wished_beer_ids)

@app.route("/beer/tried/<beer_id>", methods = ["GET"])
def update_tried_beer(beer_id):
    """ change status of tried beer (remove or update as necessary)"""
    user_id = session[CURR_USER_KEY]

    tried_beer_ids = [beer.beer_id for beer in TriedBeer.query.filter_by(user_id = user_id).all() ]

    print (tried_beer_ids)

    if beer_id in tried_beer_ids:
        tried_beer = TriedBeer.query.filter_by(user_id = user_id, beer_id = beer_id).one()
        print(tried_beer)
        db.session.delete(tried_beer)
        db.session.commit()

    else:
        new_tried_beer = TriedBeer(
            user_id = user_id,
            beer_id = beer_id
        )  
        db.session.add(new_tried_beer)
        db.session.commit()


    return redirect(f"/user/{user_id}/tried")

@app.route("/beer/liked/<beer_id>", methods = ["GET"])
def update_liked_beer(beer_id):
    """ change status of liked beer (remove or update as necessary)"""
    user_id = session[CURR_USER_KEY]

    liked_beer_ids = [beer.beer_id for beer in LikedBeer.query.filter_by(user_id = user_id).all() ]

    print (liked_beer_ids)

    if beer_id in liked_beer_ids:
        liked_beer = LikedBeer.query.filter_by(user_id = user_id, beer_id = beer_id).one()
        print(liked_beer)
        db.session.delete(liked_beer)
        db.session.commit()

    else:
        new_liked_beer = LikedBeer(
            user_id = user_id,
            beer_id = beer_id
        )  
        db.session.add(new_liked_beer)
        db.session.commit()


    return redirect(f"/user/{user_id}/liked")

@app.route("/beer/wished/<beer_id>", methods = ["GET"])
def update_wished_beer(beer_id):
    """ change status of wished beer (remove or update as necessary)"""
    user_id = session[CURR_USER_KEY]

    wished_beer_ids = [beer.beer_id for beer in WishedBeer.query.filter_by(user_id = user_id).all() ]

    print (wished_beer_ids)

    if beer_id in wished_beer_ids:
        wished_beer = WishedBeer.query.filter_by(user_id = user_id, beer_id = beer_id).one()
        print(wished_beer)
        db.session.delete(wished_beer)
        db.session.commit()

    else:
        new_wished_beer = WishedBeer(
            user_id = user_id,
            beer_id = beer_id
        )  
        db.session.add(new_wished_beer)
        db.session.commit()


    return redirect(f"/user/{user_id}/wished")