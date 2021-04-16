from flask import Flask, render_template
import requests
import mysql.connector
from dotenv import load_dotenv
import os
from hashlib import sha256
import pymysql
import json

load_dotenv()

def getAllMovies():
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + os.environ.get('TMDB_API_KEY') + "&sort_by=release_date.desc&page=1")
    return response.json()

def parseMovies():
    movies = getAllMovies()["results"]
    for movie in movies:
        title = movie['title']
        poster = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + movie['poster_path']
        backdrop = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + movie['backdrop_path']
        overview = movie['overview']
        release_year = str(movie['release_date'][0:4])
        vote_avg = str(movie['vote_average'])
        genres = movie['genre_ids'][0]

def getGenres():
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=" + os.environ.get('TMDB_API_KEY') + "&language=en-US")

def connectToDB():
    connection = pymysql.connect(host='localhost', user='root', password='', database='cinsense', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection
    
def registerUser(login, email, password):
    conn = connectToDB()
    cursor = conn.cursor()
    if (checkUsernameUniqueness(login) == 0):
        password_salted = os.environ.get('SALT') + password
        psw_hash = sha256(password_salted.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO user (username, email, password) VALUES ('" + login + "', '" + email + "', '" + psw_hash + "')")
        conn.commit()
        conn.close()
    else:
        print('This user already exists')

def checkUsernameUniqueness(login):
    conn = connectToDB()
    cursor = conn.cursor()    
    result = cursor.execute("SELECT * FROM user WHERE username='" + login + "'")
    conn.close()
    return result

def loginUserWithUName(login, password):
    conn = connectToDB()
    cursor = conn.cursor()    
    password_salted = os.environ.get('SALT') + password
    psw_hash = sha256(password_salted.encode('utf-8')).hexdigest()
    result = cursor.execute("SELECT * FROM user WHERE username='" + login + "' and password='" + psw_hash + "'")
    if (result == 0):
        print('Error occured: password and username do not match')
    else:
        print('You lucky boi, go on')
    
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

@app.route("/getAll")
def getAll():
    movies = getAllMovies()["results"]
    return movies