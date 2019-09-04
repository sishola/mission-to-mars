from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars")

# connect to mongo db and collection



@app.route("/")
def index():
    mars = mongo.db.mars_info.find_one()
    #print(mars.news_p)
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars_info = scrape_mars.scrape()
    print(mars_info)
    #collection.update({}, mars_info, upsert=True)
    mongo.db.mars_info.drop() # Drops collection if available to remove duplicates
    collection = mongo.db.mars_info
    collection.insert_many(mars_info)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
