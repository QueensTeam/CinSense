from flask import Flask, render_template, request, jsonify, make_response
import requests
import mysql.connector
import uuid
from dotenv import load_dotenv
import os
from hashlib import sha256
import pymysql
import json
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, get_jwt, jwt_required, set_access_cookies, unset_access_cookies

load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY') # Change this!
jwt = JWTManager(app)

def getAllMovies(page, genre=None):
    link = "https://api.themoviedb.org/3/discover/movie?api_key=" + os.environ.get('TMDB_API_KEY') + "&sort_by=popularity.desc&page=" + str(page)
    if genre:
        link += "&with_genres=" + str(genre)
    response = requests.get(link)
    return response.json()

def getOneMovie(id): 
    link = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + os.environ.get('TMDB_API_KEY')  + "&language=en-US"  
    response = requests.get(link)
    return response.json()

def getFilteredMovies(page, genre):
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + os.environ.get('TMDB_API_KEY') + "&sort_by=popularity.desc&page=" + str(page) + "&with_genres=" + str(genre))
    return response.json()

def getGenres():
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=" + os.environ.get('TMDB_API_KEY') + "&language=en-US")
    print(response.json())

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
        conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print(token)
        if not token:
            return jsonify({'message': 'Missing token'}), 401
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            print (data)
            conn = connectToDB()
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM user WHERE id=" + str(data['public_id']))
            conn.close()
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f()
    return decorated

def checkUsernameUniqueness(login):
    conn = connectToDB()
    cursor = conn.cursor()    
    result = cursor.execute("SELECT * FROM user WHERE username='" + login + "'")
    conn.close()
    return result

def verifyUser(password, login = None, email = None):
    conn = connectToDB()
    cursor = conn.cursor()    
    password_salted = os.environ.get('SALT') + password
    psw_hash = sha256(password_salted.encode('utf-8')).hexdigest()
    query = "SELECT * FROM user WHERE "
    if (login):
        query += "username='" + login 
    elif (email):
        query += "email='" + email
    query += "' and password='" + psw_hash + "'"
    result = cursor.execute(query)
    rez = cursor.fetchall()
    if (result == 0):
        return -1
    else:
        return str(rez[0]['id'])
    
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

@app.route("/getAll/<page>")
@app.route("/getAll/<genre>/<page>/")
def getAll(page, genre=None):
    if genre:
        movies = json.dumps(getAllMovies(page, genre)["results"])
    else: 
        movies = json.dumps(getAllMovies(page)["results"])
    return movies

@app.route("/genre/<genre>/<page>")
def getGenre(genre, page):
    movies = json.dumps(getFilteredMovies(page, genre)["results"])
    return movies

@app.route("/register",methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        print(request.values.get("registration_username") + " " + request.values.get("registration_email") + " " + request.values.get("registration_password"))
        registerUser(request.values.get("registration_username"), request.values.get("registration_email"), request.values.get("registration_password"))
        return render_template("index.html")

@app.route("/movie/<id>")
def getMovie(id):
    return getOneMovie(id)

@app.route("/allUsers", methods = ['GET'])
@jwt_required()
def get_all_users():
    conn = connectToDB()
    cursor = conn.cursor()
    result = cursor.execute("SELECT id, username, email FROM user")
    rez = cursor.fetchall()
    output = []
    print(rez)
    for row in rez:
        output.append({'id': row['id'], 'username': row['username'], 'email': row['email']})
    conn.close()
    return jsonify({'users': output})

@app.route('/login', methods = ['POST'])
def login():
    auth = request.form
    if not auth:
        return make_response('User could not be verified', 401, {'WWW-Authenticate' : 'Basic realm = "User does not exist"'})
    user = verifyUser(auth.get('password'), auth.get('username'), auth.get('email'))
    if (user == -1):
        return make_response('User could not be identified. Please check your login/email and password.', 401, {'WWW-Authenticate' : 'Basic realm = "Data problem"'})
    else:
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)      

@app.route('/deleteAccount', methods = ['DELETE'])
@jwt_required()
def deleteAccount():
    user = get_jwt_identity()
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id=" + str(user))
    conn.commit()
    conn.close()
    return make_response('User successfully deleted', 200)