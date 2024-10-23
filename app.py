import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
from chatbot import chatbot
from flask import Flask, render_template, request,session,logging,url_for,redirect,flash
import logging
from flask_recaptcha import ReCaptcha
import mysql.connector
import os

app = Flask(__name__)

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)

recaptcha = ReCaptcha(app=app)
app.secret_key=os.urandom(24)
app.static_folder = 'static'


app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L",
    RECAPTCHA_SECRET_KEY = "6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee"
))

recaptcha=ReCaptcha()
recaptcha.init_app(app)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'

#database connectivity
conn=mysql.connector.connect(host='localhost',port='3306',user='root',password='root',database='register')
cur=conn.cursor()
def get_links(category, subcategory):
    # This function should query your database for links based on the category and subcategory
    cur.execute("SELECT link, description FROM links WHERE category=%s AND subcategory=%s", (category, subcategory))
    return cur.fetchall()



# Google recaptcha - site key : 6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L
# Google recaptcha - secret key : 6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee

@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cur.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        flash('You were successfully logged in')
        return redirect('/index')
    else:
        flash('Invalid credentials !!!')
        return redirect('/')
    # return "The Email is {} and the Password is {}".format(email,password)
    # return render_template('register.html')

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('name') 
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    #cur.execute("UPDATE users SET password='{}'WHERE name = '{}'".format(password, name))
    cur.execute("""INSERT INTO  users(name,email,password) VALUES('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cur.fetchall()
    flash('You have successfully registered!')
    session['id']=myuser[0][0]
    return redirect('/index')

@app.route('/suggestion',methods=['POST'])
def suggestion():
    email=request.form.get('uemail')
    suggesMess=request.form.get('message')

    cur.execute("""INSERT INTO  suggestion(email,message) VALUES('{}','{}')""".format(email,suggesMess))
    conn.commit()
    flash('You suggestion is succesfully sent!')
    return redirect('/index')

@app.route('/add_user',methods=['POST'])
def register():
    if recaptcha.verify():
        flash('New User Added Successfully')
        return redirect('/register')
    else:
        flash('Error Recaptcha') 
        return redirect('/register')


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')


def parse_input(user_text):
    # Normalize the input text
    user_text = user_text.strip().lower()  # Strip whitespace and convert to lowercase

    # Initialize category and subcategory
    category = None
    subcategory = None

    # Check for specific user group keywords
    if user_text in ["1", "student's section enquiry", "students"]:
        category = "Students"
        subcategory = "Enquiry"
    elif user_text in ["2", "faculty section enquiry", "faculty"]:
        category = "Faculty"
        subcategory = "Enquiry"
    elif user_text in ["3", "parent's section enquiry", "parents"]:
        category = "Parents"
        subcategory = "Enquiry"
    elif user_text in ["4", "visitor's section enquiry", "visitors"]:
        category = "Visitors"
        subcategory = "Enquiry"

    return category, subcategory


def format_links_response(links):
    if not links:
        return "No links found for the specified category and subcategory."

    response = "<h5>The Following are the top search results:</h5>"
    for index, (link, description) in enumerate(links, start=1):
        response += f"<div>{index}. <a href='{link}' target='_blank'>{description}</a></div>"
    return response




@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    logging.info(f"User: {userText}")  # Log the user's message

    # Parse the input for category and subcategory
    category, subcategory = parse_input(userText)
    logging.info(f"Parsed Category: {category}, Subcategory: {subcategory}")

    # Get the chatbot response
    chatbot_response = chatbot.get_response(userText)

    # Check if the category/subcategory is valid and the chatbot confidence is high enough
    if category and subcategory:
        links = get_links(category, subcategory)
        if links:
            response = format_links_response(links)
        else:
            response = "No links found for the specified category and subcategory."
    elif chatbot_response.confidence > 0.5:
        response = str(chatbot_response)
    else:
        response = "Sorry, I couldn't understand your request."

    logging.info(f"Bot: {response}")  # Log the bot's response
    return response


if __name__ == "__main__":
    # app.secret_key=""
    app.run() 
