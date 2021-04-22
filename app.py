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
import cinsense_api as ca

load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY') 
jwt = JWTManager(app)

@app.route("/movie/<id>/seen/<userId>",methods = ['POST'])
def postSeen(id, userId):
    ca.markAsSeen(userId, id)
    return make_response("Success",200)

@app.route("/movie/<id>/seen/<userId>",methods = ['GET'])
def getSeen(id, userId):
    if(ca.checkIfInWatchlist(userId, id) == 1):
        return make_response("Seen",200)
    else:
        return make_response("NotSeen",200)

@app.route("/movie/<id>/watchlist/<userId>",methods = ['POST'])
def postInWatchlist(id, userId):
    ca.markAsWantToSee(userId, id)
    return make_response("Success",200)

@app.route("/movie/<id>/watchlist/<userId>",methods = ['GET'])
def getInWatchlist(id, userId):
    if(ca.checkIfInWatchlist(userId, id) == 1):
        return make_response("In watch list",200)
    else:
        return make_response("Not in watchlist", 200)
        
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

@app.route("/getAll/<page>")
@app.route("/getAll/<genre>/<page>/")
def getAll(page, genre=None):
    if genre:
        movies = json.dumps(ca.getAllMovies(page, genre)["results"])
    else: 
        movies = json.dumps(ca.getAllMovies(page)["results"])
    return movies

@app.route("/register",methods = ['POST'])
def register():
    ca.registerUser(request.values.get("registration_username"), request.values.get("registration_email"), request.values.get("registration_password"))
    return render_template("index.html")

@app.route("/movie/<id>")
def getMovie(id):
    return ca.getOneMovie(id)

@app.route('/login', methods = ['POST'])
def login():
    auth = request.form
    if not auth:
        return make_response('User could not be verified', 401, {'WWW-Authenticate' : 'Basic realm = "User does not exist"'})
    user = ca.verifyUser(auth.get('password'), auth.get('username'), auth.get('email'))
    if (user == -1):
        return make_response('User could not be identified. Please check your login/email and password.', 401, {'WWW-Authenticate' : 'Basic realm = "Data problem"'})
    else:
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)      

@app.route('/deleteAccount', methods = ['DELETE'])
@jwt_required()
def deleteAccount():
    user = get_jwt_identity()
    conn = ca.connectToDB()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id=" + str(user))
    conn.commit()
    conn.close()
    return make_response('User successfully deleted', 200)

@app.route('/updateAccount', methods = ['PUT'])
@jwt_required()
def updateAccount():
    data = request.form
    query = "UPDATE user SET"
    if data.get('username'):
        query += " username='" + data.get('username') + "'"
    if data.get('email'): 
        query += " email='" + data.get('email') + "'"
    if data.get('password'):
        query += " password='" + data.get('password') + "'"
    query += " WHERE id=" + str(get_jwt_identity())  
    conn = ca.connectToDB()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    return make_response('Test successful', 200)