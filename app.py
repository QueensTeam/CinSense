from flask import Flask, render_template
import requests
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def getAllMovies():
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=cff76c61f7621b5ebb8bdf5b5fe35694&sort_by=popularity.desc&page=1")
    print(response.json())

def getGenres():
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=cff76c61f7621b5ebb8bdf5b5fe35694&language=en-US")
    print(response.json())

def connectToDB():
    myconn = mysql.connector.connect(host = HOSTNAME, user = "root",passwd = "")  
    print(myconn)  

app = Flask(__name__)

@app.route("/index.html")
def home():    
    return render_template("index.html") 

@app.route("/films.html")
def films():
    return render_template("films.html")

@app.route("/account.html")
def account():
    return render_template("account.html")

@app.route("/about.html")
def aboutus():
    return render_template("about.html")

@app.route("/recommend.html")
def recommend():
    return render_template("recommend.html")

@app.route("/filmPage.html")
def indFilm():
    return render_template("filmPage.html")