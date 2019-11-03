from flask import Flask
from flask import render_template
from flask import *
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
from mysql.connector import errorcode
import smtplib
import os
from werkzeug.utils import secure_filename
import requests
import json
import time
# 1ecb72ea88mshc18e452a731772fp117d4ejsn9a224ad87a11
# rapidAPI
# CDbpXyjBeKv_-58SLLZcLXRsC_jkaTNBE-Cr2gat
# predictQ

# hardcoded address, can be improved (get evemt infomation)


def info():
    ACCESS_TOKEN = "CDbpXyjBeKv_-58SLLZcLXRsC_jkaTNBE-Cr2gat"
    response = requests.get(
        url="https://api.predicthq.com/v1/events",
        headers={
            "Authorization": "Bearer CDbpXyjBeKv_-58SLLZcLXRsC_jkaTNBE-Cr2gat",
            "Accept": "application/json"},
        params={
            "within": "50mi@33.9395909,-84.1952443",
            "start.gt": "2019-11-02",
            "end.ite": "2019-11-09",
        }
    )
    a = response.json()
    b = a.get("results")
    inner = []
    outer = []
    for i in range(5):
        for ii in range(20):
            try:
                inner.append(b[ii].get("title"))
                inner.append(b[ii].get("category"))
                inner.append(b[ii].get("start"))
                inner.append(b[ii].get("end"))
            except IndexError:
                break
    # print(len(inner), len(inner[0]))
    return inner

# hardcoded geolocation for the weather, can be improved (get weather info)


def temp():
    response = requests.get(
        "https://samples.openweathermap.org/data/2.5/forecast?zip=30309&appid=b6907d289e10d714a6e88b30761fae22")
    a = response.json()
    b = a.get("list")
    outer = []
    for i in range(len(b)):
        outer.append((b[i].get("weather")[0].get("description")))
        outer.append(((b[i].get("wind")).get("speed")))
        outer.append(
            round(
                (((b[i].get("main")).get("temp_max")) -
                 273.15) *
                9 /
                5) +
            32)
    # print(outer, len(outer))
    return outer
# get all posts from out database, let user or buyer browse


def posts():
    sql = """select * from posts"""
    mycursor.execute(sql)
    res = mycursor.fetchall()

    inner = []
    for i in range(len(res)):
        for ii in range(len(res[i])):
            try:
                inner.append(res[i][ii])
            except IndexError:
                break

    # print(inner)
    return inner


app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="ncr"
)
print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)
gmail_user = 'fangshion@gmail.com'
gmail_password = 'ragshQiqi7.'
sent_from = 'fangshion@gmail.com'
to = ''
password = ''
subject = ' Message'
body = 'This contains your password:%s\n\n- Retrieve your password'
mail_text = """\
From: %s
To: %s
Subject: %s

%s%s
""" % (sent_from, ", ".join(to), subject, body, password)

sql = """INSERT INTO account VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
sql2 = """select email, password from account where userId=%s and email=%s"""
sql3 = """select userId,password from account where userId=%s and password=%s"""
sql4 = """ INSERT INTO posts VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
sql5 = """SELECT * from posts"""
sql6 = """insert into transactions values (%s,%s,%s,%s,%s)"""
user = ''
userId = ''


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


@app.route('/home', methods=['POST', 'GET'])
def home():
    global user
    global userId
    if request.method == 'POST':
        var = (request.form['username'], request.form['password'])
        print(sql3, var)
        mycursor.execute(sql3, var)
        res = mycursor.fetchall()
        user = var[0]
        userId = var[0]
        if(len(res) == 1):
            print("record exists.")
            print('home.html', var[0])

            return render_template(
                'home.html',
                userName=user,
                user=user,
                userId=userId)
        else:
            return render_template(
                'login.html',
                userName=user,
                user=user,
                userId=userId)
    else:
        return render_template(
            'login.html',
            userName=user,
            user=user,
            userId=userId)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        var = (
            request.form['Username'],
            request.form['password'],
            request.form['email'],
            "NOW()",
            request.form['sname'],
            request.form['street'],
            request.form['city'],
            request.form['state'],
            request.form['zc'],
            request.form['lat'],
            request.form['long'],
            request.form['tob'],
            request.form['cardnumber'],
            request.form['securitycode'],
            request.form['nameoncard'],
            request.form['month'],
            request.form['date'])
        print(sql, var)
        try:
            mycursor.execute(sql, var)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as err:
            print("error risen")
        return render_template(
            'login.html',
            userName=user,
            user=user,
            userId=userId)
    else:
        return render_template(url_for('signup.html'))


@app.route('/signup')
def signup():
    return render_template(
        'signup.html',
        userName=user,
        user=user,
        userId=userId)


@app.route('/Retrieve')
def Retrieve():
    return render_template(
        'retrieve.html',
        userName=user,
        user=user,
        userId=userId)


@app.route('/')
@app.route('/logIn')
def logIn():
    return render_template(
        'login.html',
        userName=user,
        user=user,
        userId=userId)


@app.route('/Home')
def Home():
    return render_template('home.html', userName=user)


@app.route('/retrieve', methods=['POST', 'GET'])
def retrieve():
    if request.method == 'POST':
        var = (request.form['Username'], request.form['email'])
        print(sql, var)
        mycursor.execute(sql2, var)
        res = mycursor.fetchall()
        if(len(res) == 1):
            print("record exists.")
            to = res[0][0]
            password = res[0][1]
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, body)
                server.close()
                print('Email sent!')
            except BaseException:
                print(' failed...')
            return render_template(
                'login.html',
                userName=user,
                user=user,
                userId=userId)
        else:
            print("Your account name or email doesnot exist.")
            return render_template(
                'retrieve.html',
                userName=user,
                user=user,
                userId=userId)
    else:
        return render_template(
            'retrieve.html',
            userName=user,
            user=user,
            userId=userId)


@app.route('/acct')
def acct():
    return render_template(
        'acct.html',
        userName=user,
        user=user,
        userId=userId)


@app.route('/msg')
def msg():
    return render_template('msg.html', userName=user, user=user, userId=userId)


# if (request.method == 'POST'):
# user = request.form['Username']
# return redirect(url_for('home'))
# else:
# user = request.args.get('Username')
# return redirect(url_for('contact'))

@app.route('/bpps', methods=['POST', 'GET'])
def bpps():
    print(userId, ",stored userId , ", user)
    if request.method == 'POST':
                # f = request.files['files[]']
                # f.save(secure_filename(f.filename))
        print("1", request.form['opt'])
        if(request.form['opt'] == "other"):
            var = ("NULL",
                   user,
                   request.form['from'],
                   request.form['to'],
                   request.form['priceI'],
                   request.form['priceA'],
                   'NULL',
                   request.form['cate']
                   )
        else:
            var = ("NULL",
                   user,
                   request.form['from'],
                   request.form['to'],
                   request.form['priceI'],
                   request.form['priceA'],
                   'NULL',
                   request.form['opt']
                   )
        print(sql4, var)
        print("get")
        mycursor.execute(sql4, var)
        mydb.commit()
        # print(
        #    request.form['opt'],
        #    request.form['cat'],
        #    request.form['from'],
        #    request.form['priceI'],
        #    request.files['files[]'])
        # if 'files[]' not in request.files:
       #     return render_template(
       #         'bpp.html',
       #         userName=user,
      #          user=user,
       #         userId=userId)
       # files = request.files.getlist('files[]')
       # for file in files:
       #     if file and allowed_file(file.filename):
        #        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template(
            'bpp.html',
            userName=user,
            user=user,
            userId=userId)
    return render_template('bpp.html', userName=user, user=user, userId=userId)


@app.route('/bpp')
def bpp():
    return render_template('bpp.html', userName=user, user=user, userId=userId)


@app.route('/overlooks')
def overlooks():
    event = info()
    temp1 = temp()
    # print(event)
    # print(len(temp1))
    return render_template(
        'overlook.html',
        r=event,
        len=int(len(event) / 4),
        r1=temp1,
        len1=int(len(temp1) / 16),
        userName=user,
        user=user,
        userId=userId)


@app.route('/transactions', methods=['POST', 'GET'])
def transactions():
    time.sleep(1)
    postInfo = posts()
    time.sleep(3)
    print(userId, ",stored userId,", user)
    if request.method == 'POST':
        f = request.form
        val2 = f.to_dict(flat=True)
        print(val2)
        for i in range(len(val2), 1, -1):
            if(i == 1):
                continue
            else:
                print(val2.popitem())
        updateValue = val2.popitem()
        poster = postInfo[1]
        userIdPoster = updateValue[0]
        qttPoster = updateValue[1]
        print(userIdPoster, qttPoster)
        var = ("NULL", user, poster, qttPoster, "NOW()")
        try:
            mycursor.execute(sql6, var)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as err:
            print("error risen")
#	mycursor.execute(sql6, var)
#       mydb.commit()
        print(
            "accept your values, you login as:",
            user,
            userIdPoster,
            qttPoster)
    else:
        print("Nothing")

    # print(postInfo)
    return render_template(
        'transaction.html',
        userName=user,
        post=postInfo,
        len=int(len(postInfo) / 8),
        user=user,
        userId=userId)


if __name__ == '__main__':
    app.run()
