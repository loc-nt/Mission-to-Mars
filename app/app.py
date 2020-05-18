from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# set up Flask:
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the “mars” collection in our database, which we will create when we convert our Jupyter scraping code to Python Script
   return render_template("index.html", mars=mars) # return an HTML template using an index.html file, and use mars collection

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True) # upsert=True, which tells Mongo to create a new document if one doesn’t already exist.
   return "Scraping Successful!"

@app.route("/hemi1")
def hemi1():
   mars = mongo.db.mars.find_one()
   return render_template("hemi1.html", mars=mars)

@app.route("/hemi2")
def hemi2():
   mars = mongo.db.mars.find_one()
   return render_template("hemi2.html", mars=mars)

@app.route("/hemi3")
def hemi3():
   mars = mongo.db.mars.find_one()
   return render_template("hemi3.html", mars=mars)

@app.route("/hemi4")
def hemi4():
   mars = mongo.db.mars.find_one()
   return render_template("hemi4.html", mars=mars)

if __name__ == "__main__":
   app.run()