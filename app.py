
from flask import *
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
import pymongo
import os
from dotenv import load_dotenv

# loading environment from .env file

app_path = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(app_path, '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = "SomeSecret"
Bootstrap(app)
mongo = PyMongo(app)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        user = {}
        if len(request.form['password']) < 8:
            flash("Invalid Credentials - Password must be atleast 8 characters long")
            return redirect("/register")
        for field in request.form:
            if request.form[field] == "":
                flash("Invalid Credentials - Please fill each input")
                return redirect("/register")
            user[field] = request.form[field]
        mongo.db.loginsysusers.insert_one(user)
        flash("Registration successfull, now login to get access")
        return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        user = mongo.db.loginsysusers.find_one({'email': request.form['email'], 'password' : request.form['password']})
        if not user:
            flash('email and password mismatch')
            return redirect('/login')
        session['userInfo'] = {'fname' : user['fname'], 'lname' : user['lname'], 'email': user['email']}
        return redirect('/home')

@app.route('/home')
def home():
    if 'userInfo' in session:
        return render_template('home.html', userInfo = session['userInfo'])
    else:
        flash('Login to get access')
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('userInfo')
    flash('logout successful')
    return redirect('/login')

@app.route('/')
def main_path():
    return redirect('/home')

if __name__ == '__main__':
    app.run(debug = True)