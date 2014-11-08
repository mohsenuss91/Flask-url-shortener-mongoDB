from pymongo import *
from flask import Flask
from flask import request
from flask import render_template
from random import randrange
from flask import redirect

chars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ"
app=Flask(__name__)


client = MongoClient('mongoDBLinkHere/urls')
db = client['urls']
collection = db['urls']


@app.route("/")
@app.route("/index")
def my_form():
	return render_template("/my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text'].replace(".","[dot]")
	count = collection.find()
	for element in count:
		if text in element:
			return "URL = <a href = '"+element[text]+"' > Here</a>"
    
	shortenedUrl="";
	for i in range(5):
		shortenedUrl = shortenedUrl + chars[randrange(len(chars))]
	
	collection.insert({text:shortenedUrl})
	return "URL = <a href = '"+shortenedUrl+"' > Here</a>"

@app.route('/<path:path>',methods=['GET'])
def catch(path):
	listOfQuery = collection.find()
	for item in listOfQuery:
		if path in item.values():
			return redirect("http://"+item.keys()[0].replace("[dot]","."), code=302)

if __name__ == "__main__":
	app.run(debug=True)
