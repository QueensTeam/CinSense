from flask import request, jsonify
import requests
from dotenv import load_dotenv
import os
from hashlib import sha256
import pymysql
import jwt
from functools import wraps

load_dotenv()

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

def getIMDBid(id):
    link = "https://api.themoviedb.org/3/movie/" + str(id) + "/external_ids?api_key=" + os.environ.get('TMDB_API_KEY')  + "&language=en-US"
    response = requests.get(link)
    return response.json()['imdb_id']

def connectToDB():
    connection = pymysql.connect(host='localhost', user='root', password='', database='cinsense', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection
    
def registerUser(login, email, password):
    print (login)
    print (email)
    print (password)
    conn = connectToDB()
    cursor = conn.cursor()
    if (checkUsernameUniqueness(login) == 0):
        password_salted = os.environ.get('SALT') + password
        psw_hash = sha256(password_salted.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO user (username, email, password) VALUES ('" + login + "', '" + email + "', '" + psw_hash + "')")
        conn.commit()
        conn.close()
    else:
        conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Missing token'}), 401
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
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
    conn.close()
    if (result == 0):
        return -1
    else:
        return str(rez[0]['id'])
    
def checkIfAlreadyInInteractionsTable(userId, movieId):
    conn = connectToDB()
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM interaction WHERE userId=" + str(userId) + " AND movieId=" + str(movieId) + "")
    conn.commit()
    conn.close()
    return result
    
def markAsSeen(userId, movieId):
    conn = connectToDB()
    cursor = conn.cursor()
    query = "INSERT INTO interaction (seen, wantToSee, movieId, userId) VALUES (true, false, " + str(movieId) + ", " + str(userId) + ")"
    cursor.execute(query)
    conn.commit()
    conn.close()

def updateSeen(userId, movieId, seen):
    conn = connectToDB()
    cursor = conn.cursor()
    query = "UPDATE interaction SET seen = " + str(seen) + " WHERE userId=" + str(userId) + " AND movieId=" + str(movieId) + ""
    cursor.execute(query)
    conn.commit()
    conn.close()

def checkIfSeen(userId, movieId):
    conn = connectToDB()
    cursor = conn.cursor()
    query = "SELECT * FROM interaction WHERE userId=" + str(userId) + " AND movieId=" + str(movieId) + " AND seen = 1"
    result = cursor.execute(query)
    conn.close()
    return result

def markAsWantToSee(userId, movieId):
    conn = connectToDB()
    cursor = conn.cursor()
    query = "INSERT INTO interaction (seen, wantToSee, movieId, userId) VALUES (false, true, " + str(movieId) + ", " + str(userId) + ")"
    cursor.execute(query)
    conn.commit()
    conn.close() 

def updateWatchlist(userId, movieId, wantToWatch):
    conn = connectToDB()
    cursor = conn.cursor()
    query = "UPDATE interaction SET wantToSee = " + str(wantToWatch) + " WHERE userId=" + str(userId) + " AND movieId=" + str(movieId) + ""
    cursor.execute(query)
    conn.commit()
    conn.close()

def checkIfInWatchlist(userId, movieId):
    conn = connectToDB()
    cursor = conn.cursor()
    query = "SELECT * FROM interaction WHERE userId=" + str(userId) + " AND movieId=" + str(movieId) + " AND wantToSee = 1"
    result = cursor.execute(query)
    conn.close()
    return result
