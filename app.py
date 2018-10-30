from flask import Flask, render_template, request, redirect,url_for,session
import mysql.connector
import os

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Pasbalis1",
    database = "OnlineMandi"
)

mycursor = mydb.cursor()

app.secret_key = os.urandom(24)

@app.route('/')
def home_page():
    return render_template("login_signup.html")

@app.route('/signup', methods= ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user = request.form
        username = user.get("username")
        uemail = user.get("user_email")
        upassword = user.get("user_password1")
        age = int(user.get("user_age"))
        gender = user.get("user_gender")
        sql = "INSERT INTO user(email, password, username, age, gender) VALUES (%s, %s, %s, %s, %s)"
        val = (uemail, upassword, username, age, gender)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("signup_success.html")

@app.route('/verify', methods= ['POST', 'GET'])
def loginuser():
    if request.method == 'POST':
        result = request.form
        uemail = result.get("login_email")
        upass = result.get("login_password")
        sql = "SELECT * FROM user WHERE email= %s and password= %s;"
        mycursor.execute(sql, (uemail, upass))
        res = mycursor.fetchone()
        if res :
            sql = "SELECT username FROM user WHERE email= %s;"
            mycursor.execute(sql, (uemail,))
            res = mycursor.fetchall()
            session['user']= uemail
            return render_template("dashboard.html", result = res)
            #flash('Logged in Succesfully..!')

        else:
            return render_template("login_signup.html")
            #flash('Invalid Credentials.. Please try again..!!')


@app.route('/dashboard_to_chat')
def dash_to_chat():
    if 'user' in session:
        return render_template("reviews.html")
    else:
        return render_template("login_signup.html")

@app.route('/chat', methods=['POST','GET'])
def reviews():
    if 'user' in session:
        if request.method == 'POST':
            input = request.form
            uemail = session['user']
            umsg = input.get("input_val")
            sql = "INSERT INTO chat(email, msg) VALUES(%s, %s);"
            mycursor.execute(sql, (uemail, umsg))
            mydb.commit()
            sql = "SELECT email, msg FROM chat;"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            return render_template("reviews.html", result= result)
    else:
        return render_template("login_signup.html")

@app.route('/load_chat', methods=['POST', 'GET'])
def load_chat():
    if user in session:
        if request.method == 'GET':
            last_chat_id = request.form.get("last_chat_id")
            sql = "SELECT * FROM chat WHERE cid>%s;"
            mycursor.execute(sql, (last_chat_id, ))
            result = mycursor.fetchall()


@app.route('/tologin')
def tologin():
    session.pop('user', None)
    return render_template("after_logout.html")

@app.route('/send_msg')
def send_msg():
    if user in session:

        return render_template("reviews.html")
    else:
        return render_template("login_signup.html")



if __name__ == '__main__':
    app.run(host='192.168.100.16', port='8000', debug=True)