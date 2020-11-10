import os
from unittest import TestCase
from sqlalchemy import exc
from flask_debugtoolbar import DebugToolbarExtension

from models import db, TriedBeer, Category, Style, LikedBeer, WishedBeer, Review, User

os.environ['DATABASE_URL'] = "postgresql:///cicerone_test"


#import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup("emma@dog.com","password")
        self.user1.id = 11111

        self.user2 = User.signup("bojack@horse.com","horseman")
        self.user2.id = 22222

        db.session.commit()

        cat3 = Category(id = 3, name = "North American Origin Ales")
        cat1 = Category(id = 1, name = "British Origin Ales")

        db.session.add_all([cat3,cat1])
        db.session.commit()

        style1 = Style(id = 35 ,category_id = 3, name = "American-Style Wheat Wine Ale")
        style2 = Style(id = 5 ,category_id = 1, name = "Extra Special Bitter")
        style3 = Style(id = 25 ,category_id = 3, name = "American-Style Pale Ale")

        db.session.add_all([style1, style2, style3])
        db.session.commit()

        tb3 = TriedBeer(user_id = 11111, beer_id = "UJGpVS")

        lb1 = LikedBeer(user_id = 11111, beer_id = "xwYSL2")

        wb1 = WishedBeer(user_id = 11111, beer_id = "zfP2fK")
        db.session.add_all([tb3, lb1, wb1])
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic user model work"""

        review1 = Review(
            beer_name = "15th Anniversary Ale",
            user_id = 11111,
            beer_id = "xwYSL2",
            rating = 3,
            text = "Test Review",
            id = 99999
        )

        db.session.add(review1)
        db.session.commit()

        self.assertEqual(len(self.user1.reviews),1)
        self.assertEqual(self.user1.reviews[0].text,"Test Review")

    def test_signup(self):
        """test the signup classmethod"""
        user_test = User.signup("test@user.com","password")
        db.session.commit()

        ut_id = 12345
        user_test.id = ut_id
        user_test = User.query.get(ut_id)
        self.assertEqual(user_test.username,"test@user.com")

    def test_welcome_page(self):
        """test that the welcome page shows up when not logged in"""
        with self.client as client:
            url = "/"
            resp = client.get(url)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<a href="/category/3">North American Origin Ales</a>',html)

    def test_welcome_page_logged_in(self):
        """test that the welcome page shows up when not logged in"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            url = "/"
            resp = client.get(url)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<a href="/user/11111/reviews">REVIEWS</a>',html)  

    def test_beer_review_logged_in(self):
        """test that the beer review page loads properly when logged in"""

        self.test_user_model()

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            url = "/user/11111/reviews"
            resp = client.get(url)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<p>Rating: 3</p>',html)   

    def test_tried_beer_logged_in(self):
        """test that the tried beer page loads properly when logged in"""

        self.test_user_model()

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            url = "/user/11111/tried"
            resp = client.get(url)
            html = resp.get_data(as_text=True)
            # print(html)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<a href="/beer/liked/UJGpVS">',html) 

    def test_delete_review_not_logged_in(self):
        """test that a user cannot delete a review when not logged in"""

        self.test_user_model()

        with self.client as client:
            # with client.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.user1.id
            
            url = "/user/reviews/99999/delete"
            resp = client.get(url, follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Must be logged-in',html) 

    def test_delete_review_not_author(self):
        """test that a user cannot delete a review when not author of post"""

        self.test_user_model()

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user2.id
            
            url = "/user/reviews/99999/delete"
            resp = client.get(url, follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Only author can edit or delete posts!',html) 


    
