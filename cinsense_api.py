from flask import request, jsonify
import requests
from dotenv import load_dotenv
import os
from hashlib import sha256
import pymysql
import jwt
from functools import wraps
import random

load_dotenv()

genres = ["28a", "12a", "16a", "35a", "99a", "18a", "14a", "27a", "10402a", "10749a", "878a", "53a"]
decades = ["1910a", "1920a", "1930a", "1940a", "1950a", "1960a", "1970a", "1980a", "1990a", "2000a", "2010a", "2020a"] 
avgvotes = ["0a", "6a", "8a"]
votecnts = ["5000a", "10000a", "50000a"]

def getAllMovies(page, filter=None):
    link = "https://api.themoviedb.org/3/discover/movie?api_key=" + os.environ.get('TMDB_API_KEY') + "&sort_by=popularity.desc&page=" + str(page)
    if filter:
        for dec in decades:
            if dec in filter: link += "&release_date.gte=" + dec[:-1] + "&release_date.lte=" + str(int(dec[:-1]) + 9)
        for avg in avgvotes:
            if avg in filter:
                if avg == "0a": link += "&vote_average.lte=6&vote_average.gte=0"
                elif avg == "6a": link += "&vote_average.gte=6&vote_average.lte=8"
                elif avg == "8a": link += "&vote_average.gte=8"
        for cnt in votecnts:
            if cnt in filter:
                if cnt == "5000a": link +="&vote_count.gte=0&vote_count.lte=5000"
                elif cnt == "10000a": link += "&vote_count.gte=5000&vote_count.lte=10000"
                elif cnt == "50000a": link += "&vote_count.gte=50000"
        for genre in genres:
            if genre in filter: link += "&with_genres=" + str(genre[:-1])   
    response = requests.get(link)
    return response.json()

def getOneMovie(id): 
    response = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + os.environ.get('TMDB_API_KEY')  + "&language=en-US")
    return response.json()

def getIMDBid(id):
    link = "https://api.themoviedb.org/3/movie/" + str(id) + "/external_ids?api_key=" + os.environ.get('TMDB_API_KEY')  + "&language=en-US"
    response = requests.get(link)
    return response.json()['imdb_id']

def getRandomMovie():
    rand = random.randint(0, 20)
    return getAllMovies(1)['results'][rand]

def connectToDB():
    connection = pymysql.connect(host='localhost', user='root', password='', database='cinsense', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection
    
def registerUser(login, email, password):
    print (login + " " + email + " " + password)
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
