from app import db
from models import User, Review, TriedBeer, LikedBeer, WishedBeer, Category, Style
from data import styledata

db.drop_all()
db.create_all()

User.signup("emmadoodles","password")

db.session.commit()

tb1 = TriedBeer(user_id = 1, beer_id = "c4f2KE")
tb2 = TriedBeer(user_id = 1, beer_id = "xwYSL2")
tb3 = TriedBeer(user_id = 1, beer_id = "UJGpVS")

lb1 = LikedBeer(user_id = 1, beer_id = "xwYSL2")

wb1 = WishedBeer(user_id = 1, beer_id = "zfP2fK")

db.session.add_all([tb1, tb2, tb3, lb1, wb1])
db.session.commit()

review1 = Review(user_id = 1, beer_id = "xwYSL2", beer_name = "15th Anniversary Ale", rating = 4, text = "I really liked this beer")
db.session.add(review1)
db.session.commit()

cat1 = Category(id = 1, name = "British Origin Ales")
cat2 = Category(id = 2, name = "Irish Origin Ales")
cat3 = Category(id = 3, name = "North American Origin Ales")
cat4 = Category(id = 4, name = "German Origin Ales")
cat5 = Category(id = 5, name = "Belgian & French Origin Ales")
cat6 = Category(id = 6, name = "International Ale Styles")
cat7 = Category(id = 7, name = "European-Germanic Lager")
cat8 = Category(id = 8, name = "North American lager")
cat9 = Category(id = 9, name = "Other Lager")
cat10 = Category(id = 10, name = "International Styles")
cat11 = Category(id = 11, name = "Hybrid / Mixed Beer")
cat12 = Category(id = 12, name = "Mead, Cider, & Perry")
cat13 = Category(id = 13, name = "Other Origin")
cat14 = Category(id = 14, name = "Malternative Beverages")

db.session.add_all([cat1,cat2,cat3,cat4,cat5,cat6,cat7,cat8,cat9,cat10,cat11,cat12,cat12,cat13,cat14])
db.session.commit()

i = 0
while i < len(styledata):
    new_style = Style(id = styledata[i][0],category_id = styledata[i][1], name = styledata[i][2])
    db.session.add(new_style)
    db.session.commit()
    i +=1
