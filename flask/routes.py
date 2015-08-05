from random import shuffle
import random
import json
import os
import conjunctions as ConjunctionClass
import coordinatingConjunctions as CoordinatingConjunctionClass
import dialog as DialogClass
import ginger_python2_new as ginger
import ginger_python2 as Grammar
import check_tense as TenseClass
import socket
import keywords
import en
import webbrowser
from threading import Thread
import pyttsx

from nltk.corpus import brown

from ansi2html import Ansi2HTMLConverter
from flask import Flask, render_template, url_for, redirect
from flask import request, flash, session, escape
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymsgbox import *
from flask.ext.mail import Mail, Message
from nltk.tokenize import RegexpTokenizer


import MySQLdb
from MySQLdb import escape_string

import numpy
import nltk
from nltk import pos_tag, word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize

import notice
import invitation
import note

from flask import jsonify

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='englishbuddy.edu@gmail.com',
    MAIL_PASSWORD='00000444',
))

mail = Mail(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Set secret key
app.config['SECRET_KEY'] = 'F34TF$($e34D';

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# Open database connection
db = MySQLdb.connect("localhost", "root", "00000444", "english_buddy")


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])

    return render_template('login.html')


# ------------------------------------- Sign up -----------------------------------------------

# # Register ##
@app.route('/register')
def register():
    return render_template('register.html')


# # Register new user ##
@app.route('/save', methods=['POST'])
def register_user():
    if request.method == 'POST':

        fName = request.form['txtFirstName']
        lName = request.form['txtLastName']
        email = request.form['txtEmail']
        password = request.form['txtPassword']
        confirm_password = request.form['txtConPassword']
        phone = request.form['txtPhone']
        role = request.form['listRole']
        if role != 'Parent':
            school = request.form['txtSchool']


        sql = """SELECT email FROM users where email=%s"""
        try:
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute(sql, [email])

            # fetch a single row using fetchone() method.
            data = cursor.fetchone()

            if data:
                error = 'You have been alreay registered!'
                flash(error)
                return render_template('register.html', error=error)
            else:
                hashPassword = generate_password_hash(password)  #create password hash

                cursor = db.cursor()

                if role != 'Parent':
                    sql = """INSERT INTO users (email,fName,lName,password,phone,school,role,placement_test) VALUES(%s,%s,%s,%s,%s,%s,%s,'false')"""
                else:
                    sql = """INSERT INTO users (email,fName,lName,password,phone,role,placement_test) VALUES(%s,%s,%s,%s,%s,%s,'false')"""

                try:
                    # Execute the SQL command
                    if role != 'Parent':
                        cursor.execute(sql, [email, fName, lName, hashPassword, phone, school, role])
                    else:
                        cursor.execute(sql, [email, fName, lName, hashPassword, phone, role])

                    # Commit your changes in the database
                    db.commit()

                except:
                    # Rollback in case there is any error
                    db.rollback()

                    # disconnect from server
                    db.close()

                # Commit your changes in the database
                db.commit()

        except:
            # Rollback in case there is any error
            db.rollback()

    alert(text='User Registered Successfully !', title='English Buddy', button='OK')

    if check_internet_connection():
        ## Send email ##
        msg = Message('English Buddy', sender="englishbuddy.edu@gmail.com")
        msg.recipients = [email]
        msg.html = "<body bgcolor='#DCEEFC'><center>===============================<br><br><b>Hi,</b> <br><b>Welcome to English Buddy !</b><br><br>Sign in to get started:<br><br><font color='blue'>User name: " + email + " </font><br><br>Have fun!<br>English Buddy Team<br><br><a href='http://127.0.0.1:5000/'>Sign in Now</a><br><br>===============================<br></center></body>"
        mail.send(msg)

    #redirect to login page
    return render_template('login.html')


# ---------------------------------- Sign in -----------------------------------------------

## login ##
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        userName = request.form['txtEmail']
        password = request.form['txtPassword']

        # Open database connection
        db = MySQLdb.connect("localhost", "root", "00000444", "english_buddy")

        cursor = db.cursor()
        sql = """SELECT password,placement_test,role,fName,image FROM users where email=%s"""
        try:
            # Execute the SQL command
            cursor.execute(sql, [userName])

            # fetch a single row using fetchone() method.
            data = cursor.fetchall()
            for row in data:
                dbPassword = row[0]
                placementTestStatus = row[1]
                role = row[2]
                fName = row[3]
                image = row[4]
                #print(placementTestStatus)

            userCheck = check_password_hash(dbPassword, password)

            if userCheck:
                session['username'] = userName
                session['role'] = role
                session['profilePic'] = image
                session['level'] = placementTestStatus
                session['fName'] = fName
                #login_user(data)
                data = {'username': userName, 'role': role, 'level': placementTestStatus, 'fName': fName}

                query = getSenderData(userName)
                count = getCount(userName)

                if session['role'] == "Teacher":
                    # Get student subscribe request count
                    count=student_subscribe_request_count()

                    # Get student subscribe request details
                    query=display_student_subscribe_request_details()

                    return render_template('home_teacher.html',query=query,count=count)

                if session['role'] == "Parent":
                    AcceptedList = getAcceptedData(userName)
                    return render_template('home_parent.html', List=AcceptedList)

                if session['role'] == "Student":

                    if placementTestStatus == "false":
                        return render_template('home_pt.html', data=data)
                    elif placementTestStatus == "Elementary":
                        return render_template('home_1.html', data=data, query=query, count=count)
                    elif placementTestStatus == "Preliminary":
                        return render_template('home_2.html', data=data, query=query, count=count)
                    elif session['level'] == "Intermediate":
                        return render_template('home_3.html', data=data, query=query, count=count)
                    elif session['level'] == "Advanced":
                        return render_template('home_4.html', data=data, query=query, count=count)
            else:
                flash('Invalid Username or Password !')

            # Commit your changes in the database
            db.commit()

        except:
            # Rollback in case there is any error
            db.rollback()
            flash('Invalid Username or Password !')

    return render_template('login.html', error=error,)



## Get student subscribe request count ##
def student_subscribe_request_count():
    cursor = db.cursor()
    sql = """SELECT COUNT(status) as count FROM subscribe_teacher WHERE teacher=%s AND status='pending'"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        # fetch a single row using fetchone() method.
        data = cursor.fetchall()
        for row in data:
            requests = row[0]
        session['subscribe_requests'] = requests
    except:
        # Rollback in case there is any error
        db.rollback()

    return data

## Get student subscribe request details ##
def display_student_subscribe_request_details():
    cursor = db.cursor()
    sql = """SELECT u.fName,u.lName,u.school,u.image,u.placement_test,s.status,s.student FROM users u, subscribe_teacher s WHERE u.email=s.student AND s.status='pending' AND s.teacher=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()

    return result


# ---------------------------------------- log out ---------------------------------------------

## logout ##
@app.route('/logout')
def logout():

    session.clear()

    # del session['username']
    # del session['profilePic']
    # del session['level']
    # del session['fName']
    #
    # if session['role'] == 'Teacher':
    #     del session['subscribe_requests']
    #
    # del session['role']

    return redirect(url_for('login'))


# -------------------------------------------- Reset Password ----------------------------------------- #

## Forgot password ##
@app.route('/view_forgot_password', methods=['GET', 'POST'])
def view_forgot_password():
    return render_template('forgot_password.html')


## Forgot password ##
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':

        email = request.form['txtEmail']

        status = check_email_exists(email)

        if status:
            send_reset_password_email(email, status)
            data = {'email': email}

            return render_template('forgot_password_success.html', data=data)

    return redirect(url_for('login'))


## Check email exists ##
def check_email_exists(email):
    cursor = db.cursor()

    sql = """SELECT fName FROM users where email=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [email])
        # fetch a single row using fetchone() method.
        data = cursor.fetchall()
        for row in data:
            fName = row[0]
        if data:
            return fName
    except:
        # Rollback in case there is any error
        db.rollback()

    return False


## Send reset password email ##
def send_reset_password_email(email, firstname):
    email_code = generate_password_hash(app.secret_key + firstname)

    ## Send email ##
    msg = Message('English Buddy - Reset Password', sender="englishbuddy.edu@gmail.com")
    msg.recipients = [email]
    msg.html = "<body bgcolor='#DCEEFC'><center>===============================<br><br><b><b>Dear, " + firstname + "</b><br><br><p>Please <strong><a href='http://127.0.0.1:5000/reset_password_form/?email=" + email + "&email_code=" + email_code + "'> click here</a></strong>&nbsp;to reset your password.</p><p>Thank you!</p><br>English Buddy Team<br><br><a href='http://127.0.0.1:5000/'>Sign in Now</a><br><br>===============================<br></center></body>"
    mail.send(msg)


## Reset password ##
@app.route('/reset_password_form/', methods=['GET'])
def reset_password_form():
    email = request.args.get('email')
    email_code = request.args.get('email_code')

    print "send emial_code: " + email_code

    verified = verify_reset_password_code(email, email_code)

    if verified:
        email_hash = email + email_code
        data = {'email_hash': email_hash, 'email_code': email_code, 'email': email}

        return render_template('reset_password.html', data=data)

    return redirect(url_for('login'))


## Verify reset password ##
def verify_reset_password_code(email, code):
    cursor = db.cursor()
    sql = """SELECT fName FROM users where email=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [email])
        # fetch a single row using fetchone() method.
        data = cursor.fetchall()
        for row in data:
            fName = row[0]
            print "fName:" + fName
        if data:
            generated_code = app.secret_key + fName
            send_code = check_password_hash(code, generated_code)

            if send_code:
                return True
            else:
                return False
    except:
        # Rollback in case there is any error
        db.rollback()

    return False


## Update New Password ##
@app.route('/update_password', methods=['POST'])
def update_password():
    if request.method == 'POST':

        email = request.form['txtEmail']
        password = request.form['txtNewPassword']
        confirm_password = request.form['txtComfirmPassword']

        if password != confirm_password:
            error = "Password didn't match"
            flash(error)
            return render_template('reset_password.html', error=error)

        hashPassword = generate_password_hash(password)  #create password hash

        cursor = db.cursor()
        sql = """UPDATE users SET password=%s WHERE email=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [hashPassword, email])
            # Commit your changes in the database
            db.commit()
            alert(text='Password Updated Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('login'))


# ------------------------------------------- User Profile -------------------------------------------- #

## View profile details ##
@app.route('/view_profile')
def view_profile():
    userName = session['username']

    query = ""
    cursor = db.cursor()
    sql = """SELECT * FROM users where email=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [userName])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    if session['role']=='Teacher':
        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query1=display_student_subscribe_request_details()

        return render_template('profile.html', data=query, query=query1, count=count)
    else:
        return render_template('profile.html', data=query)


## pass profile data to the modal ##
@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    username = session['username']

    cursor = db.cursor()
    sql = """SELECT * FROM users where email=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [username])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            fname = row[1]
            lname = row[2]
            phone = row[4]
            school = row[5]
            role = row[7]
    except:
        db.rollback()

    return json.dumps(dict(fname=fname, lname=lname, phone=phone, school=school))


## edit profile data ##
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    id = request.form['id']

    cursor = db.cursor()
    sql = """update users set fName=%s,lName=%s,phone=%s where email=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [fname, lname, phone, id])
        # Commit your changes in the database
        db.commit()
        #flash('Successfully Updated !')
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('view_profile'))


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


## Update profile picture ##
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file

        cursor = db.cursor()
        sql = """update users set image=%s where email=%s"""
        try:
            # Execute the SQL command
            cursor.execute(sql, [filename, session['username']])
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        return redirect(url_for('view_profile'))


# ------------------------------------- home ---------------------------------------------------

## Home ##
@app.route('/home')
def home():
    if session['role'] == "Teacher":
        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()

        return render_template('home_teacher.html',query=query, count=count)

    elif session['role'] == "Parent":
        AcceptedList = getAcceptedData(session['username'])
        return render_template("home_parent.html", List=AcceptedList)

    elif session['level'] == "false":
        return render_template('home_pt.html')
    elif session['level'] == "Elementary":
        query = getSenderData(session['username'])
        count = getCount(session['username'])
        return render_template('home_1.html', query=query, count=count)
    elif session['level'] == "Preliminary":
        query = getSenderData(session['username'])
        count = getCount(session['username'])
        return render_template('home_2.html', query=query, count=count)
    elif session['level'] == "Intermediate":
        query = getSenderData(session['username'])
        count = getCount(session['username'])
        return render_template('home_3.html', query=query, count=count)
    elif session['level'] == "Advanced":
        query = getSenderData(session['username'])
        count = getCount(session['username'])
        return render_template('home_4.html', query=query, count=count)

    return render_template('login.html')


## Level 1  ##
@app.route('/level1')
def level1():
    if session['role'] == "Teacher":
        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()

        return render_template('home_1.html',query=query, count=count)


## Level 2  ##
@app.route('/level2')
def level2():
    if session['role'] == "Teacher":
        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()

        return render_template('home_2.html',query=query, count=count)


## Level 3  ##
@app.route('/level3')
def level3():
    if session['role'] == "Teacher":
        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()

        return render_template('home_3.html',query=query, count=count)


## Level 4  ##
@app.route('/level4')
def level4():
    if session['role'] == "Teacher":
        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()

        return render_template('home_4.html',query=query, count=count)


## Teacher Home  ##
@app.route('/home_teacher')
def home_teacher():

    # Get student subscribe request count
    count=student_subscribe_request_count()
    # Get student subscribe request details
    query=display_student_subscribe_request_details()

    return render_template('home_teacher.html',query=query, count=count)



# -------------------------------- Placement Test -----------------------------------------

## Placement Test ##
@app.route('/Placement_T')
def Placement_T():

    print Level_One_Questions()
    print Level_Two_Questions()
    print Level_Three_Questions()
    print Level_Four_Questions()

    return render_template('PlacementTest.html', data_level1=Level_One_Questions(),data_level2=Level_Two_Questions(),data_level3=Level_Three_Questions(),data_level4=Level_Four_Questions())

## question level 1 , 10 quetsions in random ##
def Level_One_Questions():

    cursor = db.cursor()
    sql = """ SELECT * FROM tbl_placement_test_dc WHERE qno between 1 and 30 order by rand() limit 10"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(escape_string(sql.decode('cp1250', 'ignore')))
        # fetch rows using fetchall() method.

        stringSet = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return stringSet

## question level 2 , 10 quetsions in random ##
def Level_Two_Questions():

    cursor = db.cursor()
    sql = """ SELECT * FROM tbl_placement_test_dc WHERE qno between 31 and 60 order by rand() limit 10"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(escape_string(sql.decode('cp1250', 'ignore')))
        # fetch rows using fetchall() method.

        stringSet = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return stringSet

## question level 3 , 5 quetsions in random ##
def Level_Three_Questions():

    cursor = db.cursor()
    sql = """ SELECT * FROM tbl_placement_test_dc WHERE qno between 61 and 80 order by rand() limit 5"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(escape_string(sql.decode('cp1250', 'ignore')))
        # fetch rows using fetchall() method.

        stringSet = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return stringSet

## question level 4 , 5 quetsions in random ##
def Level_Four_Questions():

    cursor = db.cursor()
    sql = """ SELECT * FROM tbl_placement_test_dc WHERE qno between 81 and 100 order by rand() limit 5"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(escape_string(sql.decode('cp1250', 'ignore')))
        # fetch rows using fetchall() method.

        stringSet = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return stringSet


## Evaluate Placement Test
@app.route('/Placement_Report', methods=['POST'])
def Placement_Report():
    if request.method == 'POST':
        count = 0;
        level = ''
        select1 = request.form['select1']
        select2 = request.form['select2']
        select3 = request.form['select3']
        select4 = request.form['select4']
        select5 = request.form['select5']
        print select1

        select6 = request.form['select6']
        select7 = request.form['select7']
        select8 = request.form['select8']
        select9 = request.form['select9']
        select10 = request.form['select10']

        select11 = request.form['select11']
        select12 = request.form['select12']
        select13 = request.form['select13']
        select14 = request.form['select14']
        select15 = request.form['select15']

        select16 = request.form['select16']
        select17 = request.form['select17']
        select18 = request.form['select18']
        select19 = request.form['select19']
        select20 = request.form['select20']

        select21 = request.form['select21']
        select22 = request.form['select22']
        select23 = request.form['select23']
        select24 = request.form['select24']
        select25 = request.form['select25']

        select26 = request.form['select26']
        select27 = request.form['select27']
        select28 = request.form['select28']
        select29 = request.form['select29']
        select30 = request.form['select30']

        print request.form['answer1']
        if select1 == request.form['answer1']:
            count = count + 1

        if (select2 == request.form['answer2']):
            count = count + 1

        if (select3 == request.form['answer3']):
            count = count + 1

        if (select4 == request.form['answer4']):
            count = count + 1

        if (select5 == request.form['answer5']):
            count = count + 1

        if (select6 == request.form['answer6']):
            count = count + 1

        if select7 == request.form['answer7']:
            count = count + 1

        if (select8 == request.form['answer8']):
            count = count + 1

        if (select9 == request.form['answer9']):
            count = count + 1

        if (select10 == request.form['answer10']):
            count = count + 1

        if (select11 == request.form['answer11']):
            count = count + 1

        if (select12 == request.form['answer12']):
            count = count + 1
        if select13 == request.form['answer13']:
            count = count + 1

        if (select14 == request.form['answer14']):
            count = count + 1

        if (select15 == request.form['answer15']):
            count = count + 1

        if (select16 == request.form['answer16']):
            count = count + 1

        if (select17 == request.form['answer17']):
            count = count + 1

        if (select18 == request.form['answer18']):
            count = count + 1
        if select19 == request.form['answer19']:
            count = count + 1

        if (select20 == request.form['answer20']):
            count = count + 1

        if (select21 == request.form['answer21']):
            count = count + 1

        if (select22 == request.form['answer22']):
            count = count + 1

        if (select23 == request.form['answer23']):
            count = count + 1

        if (select24 == request.form['answer24']):
            count = count + 1
        if (select25 == request.form['answer25']):
            count = count + 1

        if (select26 == request.form['answer26']):
            count = count + 1

        if (select27 == request.form['answer27']):
            count = count + 1

        if (select28 == request.form['answer28']):
            count = count + 1

        if (select29 == request.form['answer29']):
            count = count + 1

        if (select30 == request.form['answer30']):
            count = count + 1

        if count < 7:
            level = 'Elementary'
        elif 7 <= count and count < 13:
            level = 'Preliminary'

        elif 13 <= count and count < 23:
            level = 'Intermediate'

        elif 23 < count and count <= 30:
            level = 'Advanced'

        session['level'] = level

        data = {'count': count, 'level': level}

        cursor = db.cursor()
        sql = """update users set placement_test=%s where email=%s"""

        try:
            cursor.execute(sql, [level, session['username']])
            db.commit()

        except:
            db.rollback()
        return render_template('Placement_Report.html', data=data)


## ------------------------------------- Add Questions Main Page ---------------------------------- ##

@app.route('/view_addQuestions')
def view_addQuestions():
    # Get student subscribe request count
    count=student_subscribe_request_count()
    # Get student subscribe request details
    query=display_student_subscribe_request_details()

    return render_template('AddQuestions.html', query=query, count=count)


## ------------------------------ LEVEL 1 - ELEMENTARY LEVEL -----------------------------------


# ------------------------ Level 1 - Conjunctions -----------------------------------------------

## Conjunction Questions for level 1 NEW ##
@app.route('/add_conjunction_questions_new')
def add_conjunction_questions_new():
    return render_template('add_conjunction_questions_new.html')


## Add conjunction question for level 1 NEW ##
@app.route('/save_conjunction_question_new', methods=['POST'])
def save_conjunction_question_new():
    if request.method == 'POST':

        question1 = request.form['question_1']
        question2 = request.form['question_2']
        question3 = request.form['question_3']
        answer1 = request.form['answer_1']
        answer2 = request.form['answer_2']
        answer3 = request.form['answer_3']
        author = session['username']

        question1_exist=False
        question2_exist=False
        question3_exist=False

        cursor = db.cursor()
        sql = """SELECT * FROM conjunctions WHERE question=%s OR question=%s OR question=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3])
            result = cursor.fetchall()

            if result:
                for row in result:
                    if row[2]==question1:
                        question1_exist=True
                    elif row[2]==question2:
                        question2_exist=True
                    elif row[2]==question3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'question1':question1, 'question2':question2, 'question3':question3, 'answer1':answer1, 'answer2':answer2, 'answer3':answer3, 'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('add_conjunction_questions_new.html', errors=errors)
            #flash('Question successfully added !')

        except:
            # Rollback in case there is any error
            db.rollback()


        rows = []
        if question1 != '' and answer1 != '':
            rows.append((question1, answer1, author))
        if question2 != '' and answer2 != '':
            rows.append((question2, answer2, author))
        if question3 != '' and answer3 != '':
            rows.append((question3, answer3, author))

        cursor = db.cursor()
        sql = """INSERT INTO conjunctions (level,question,answer,author) VALUES('level1',%s,%s,%s)"""

        try:
            # Execute the SQL command
            cursor.executemany(sql, rows)
            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Questions Added Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('add_conjunction_questions_new'))


## Display all conjunction questions ##
@app.route('/display_conjunction_questions/', methods=['GET'])
def display_conjunction_questions():

    level = request.args.get('level')

    cursor = db.cursor()
    if level=='level1':
        sql = """SELECT * FROM conjunctions WHERE author=%s AND level=%s"""
    elif level=='level3':
        sql = """SELECT * FROM level3_conjunctions WHERE author=%s AND level=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], level])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    levelData={'level':level}

    return render_template('display_conjunction_questions.html', data=result, levelData=levelData)


## Edit level 1 conjunction questions ##
@app.route('/edit_conjunction', methods=['GET', 'POST'])
def edit_conjunction():
    qNo = request.args.get('qNo')
    level = request.args.get('level')
    cursor = db.cursor()
    sql = """SELECT * FROM conjunctions where level=%s and author=%s and qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [level, session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[2]
            answer = row[3]
    except:
        db.rollback()

    return json.dumps(
        dict(question=question, answer=answer))


## Save edited conjunction question for level 1 ##
@app.route('/save_edited_conjunction_question', methods=['POST'])
def save_edited_conjunction_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        level = request.form['level']
        question = request.form['question_1']

        if level=='level1':
            answer = request.form['answer_1']

        cursor = db.cursor()

        if level=='level1':
            sql = """UPDATE conjunctions SET question=%s,answer=%s WHERE qNo=%s"""
        elif level=='level3':
            sql = """UPDATE level3_conjunctions SET question=%s WHERE qNo=%s"""

        try:
            # Execute the SQL command
            if level=='level1':
                cursor.execute(sql, [question, answer, qNo])
            elif level=='level3':
                cursor.execute(sql, [question, qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

        url='/display_conjunction_questions/?level='+level

    return redirect(url)


## Delete conjunction questions ##
@app.route('/delete_conjunction_questions/', methods=['GET'])
def delete_conjunction_questions():
    qNo = request.args.get('qNo')
    level = request.args.get('level')

    cursor = db.cursor()
    if level=='level1':
        sql = """DELETE FROM conjunctions WHERE qNo=%s"""
    elif level=='level3':
        sql = """DELETE FROM level3_conjunctions WHERE qNo=%s"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    url='/display_conjunction_questions/?level='+level

    return redirect(url)


## Level 1 Conjunctions Activity NEW##
@app.route('/level1_conjunctions_new')
def level1_conjunctions_new():
    array=[]

    cursor = db.cursor()
    sql = """SELECT * FROM conjunctions where level='level1' order by rand() limit 5 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            answer = row[3]
            array.append(answer)
    except:
        # Rollback in case there is any error
        db.rollback()

    shuffle(array)
    shuffledData = {'shuffledArray': array}

    return render_template('level1_conjunctions_new.html', data=result, shuffledData=shuffledData)


## Evaluate level1 conjunction question answers NEW ##
@app.route('/evaluate_level1_conjunctions_new', methods=['POST'])
def evaluate_level1_conjunctions_new():
    if request.method == 'POST':
        marks = 0

        question1=request.form['question1']
        question2=request.form['question2']
        question3=request.form['question3']
        question4=request.form['question4']
        question5=request.form['question5']
        correctAnswer1 = request.form['correctAnswer1']
        correctAnswer2 = request.form['correctAnswer2']
        correctAnswer3 = request.form['correctAnswer3']
        correctAnswer4 = request.form['correctAnswer4']
        correctAnswer5 = request.form['correctAnswer5']
        pa1 = request.form['one']
        pa2 = request.form['two']
        pa3 = request.form['three']
        pa4 = request.form['four']
        pa5 = request.form['five']

        data = [['','',question1],['','',question2],['','',question3],['','',question4],['','',question5]]

        array=[correctAnswer1, correctAnswer2, correctAnswer3, correctAnswer4, correctAnswer5]
        shuffle(array)
        shuffledData = {'shuffledArray': array}

        if correctAnswer1 == pa1:
            a1_status = "Correct"
            marks = marks + 1
        else:
            a1_status = "Wrong"

        if correctAnswer2 == pa2:
            a2_status = "Correct"
            marks = marks + 1
        else:
            a2_status = "Wrong"

        if correctAnswer3 == pa3:
            a3_status = "Correct"
            marks = marks + 1
        else:
            a3_status = "Wrong"

        if correctAnswer4 == pa4:
            a4_status = "Correct"
            marks = marks + 1
        else:
            a4_status = "Wrong"

        if correctAnswer5 == pa5:
            a5_status = "Correct"
            marks = marks + 1
        else:
            a5_status = "Wrong"


        data_array = {'pa1': pa1, 'pa2': pa2, 'pa3': pa3, 'pa4': pa4, 'pa5': pa5, 'a1': correctAnswer1, 'a2': correctAnswer2, 'a3': correctAnswer3, 'a4': correctAnswer4, 'a5': correctAnswer5,
                      'a1_status': a1_status, 'a2_status': a2_status, 'a3_status': a3_status,
                      'a4_status': a4_status, 'a5_status': a5_status, 'marks': marks}

        return render_template('level1_conjunctions_new.html', answer_data=data_array, shuffledData=shuffledData,data=data)

    return redirect(url_for('level1_conjunctions_new'))


# ---------------------------- Adjectives -------------------------------------

#view AddQues_adjective page ##
@app.route('/AddQues_adjectives')
def AddQues_adjectives():
    return render_template('AddQues_adjectives.html')


## Level 1 Adjectives Add Questions ##
@app.route('/Save_adjectives', methods=['POST'])
def Save_adjectives():
    question = request.form['txtQuestion']
    a = request.form['txtAnswer1']
    b = request.form['txtAnswer2']
    c = request.form['txtAnswer3']
    answer = request.form['txtCorrectAnswer']
    author = session['username']

    question_exit = False

    cursor = db.cursor()

    sql = """SELECT * FROM level_1_adjectives where question=%s"""

    try:
        cursor.execute(sql, [question])
        result = cursor.fetchall()
        # Commit your changes in the database
        print sql

        if result:
            for row in result:
                if row[1] == question:
                    question_exit = True

            alert(text='Questions Already exists !', title='English Buddy', button='OK')

            errors = {'question': question, 'a': a, 'b': b, 'c': c, 'answer': answer, 'questionStatus': question_exit}
            return render_template('AddQues_adjectives.html', errors=errors)
    #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    cursor = db.cursor()
    sql = """INSERT INTO level_1_adjectives(question,a,b,c,answer,author) VALUES(%s,%s,%s,%s,%s,%s)"""

    try:
        # Execute the SQL command
        cursor.execute(sql, [question, a, b, c, answer, author])
        # Commit your changes in the database
        db.commit()
        #flash('Question successfully added !')
        alert(text='Questions Added Successfully !', title='English Buddy', button='OK')
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('AddQues_adjectives.html')


## Display all adjectives questions ##
@app.route('/Update_adjectives')
def Update_adjectives():
    cursor = db.cursor()

    sql = """SELECT qno,question,a,b,c,answer FROM level_1_adjectives where author=%s """
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return render_template('Update_adjectives.html', data=query)


## get data to display in modal in edit adjective question ##
@app.route('/edit_adjectives', methods=['GET', 'POST'])
def edit_adjectives():
    qno = request.args['qno']

    cursor = db.cursor()
    sql = """SELECT * FROM level_1_adjectives where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [qno])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            question = row[1]
            a = row[2]
            b = row[3]
            c = row[4]
            answer = row[5]
    except:
        db.rollback()

    return json.dumps(dict(question=question, a=a, b=b, c=c, answer=answer))


## Save Edited adjectives question ##
@app.route('/save_edited_adjectives', methods=['POST'])
def save_edited_adjectives():
    qno = request.form['qno']
    question = request.form['inputQues']
    a = request.form['Answer1']
    b = request.form['Answer2']
    c = request.form['Answer3']
    answer = request.form['Answer']

    cursor = db.cursor()
    sql = """update level_1_adjectives set question=%s,a=%s,b=%s,c=%s,answer=%s where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [question, a, b, c, answer, qno])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('Update_adjectives'))


## Delete adjectives question ##
@app.route('/delete_adjectives/', methods=['GET'])
def delete_adjectives():
    qno = request.args.get('qNo')

    cursor = db.cursor()
    sql = """delete from level_1_adjectives where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [qno])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('Update_adjectives'))


## Level 1 Adjectives Activity ##
@app.route('/level_1_adjectives')
def level_1_adjectives():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_1_adjectives order by rand() limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch rows using fetchall() method.
        query = cursor.fetchall()

    except:
        db.rollback()

    return render_template('level_1_adjectives.html', data=query)


## ------------------------------------------ Prepositions ---------------------------------------- ##

## View Add prepositions question ##
@app.route('/add_prepositions_question')
def add_prepositions_question():
    return render_template('add_preposition_questions.html')



## Add prepositions question ##
@app.route('/addPrepositions', methods=['POST'])
def addPrepositions():
      question1 = request.form['question_1']
      question2 = request.form['question_2']
      question3 = request.form['question_3']
      Q1correct = request.form['Q1_txtCorrect']
      Q1answer1 = request.form['Q1_txtAnswer1']
      Q1answer2 = request.form['Q1_txtAnswer2']
      Q1answer3 = request.form['Q1_txtAnswer3']

      Q2correct = request.form['Q2_txtCorrect']
      Q2answer1 = request.form['Q2_txtAnswer1']
      Q2answer2 = request.form['Q2_txtAnswer2']
      Q2answer3 = request.form['Q2_txtAnswer3']

      Q3correct = request.form['Q3_txtCorrect']
      Q3answer1 = request.form['Q3_txtAnswer1']
      Q3answer2 = request.form['Q3_txtAnswer2']
      Q3answer3 = request.form['Q3_txtAnswer3']

      author =session['username']

      question1_exist=False
      question2_exist=False
      question3_exist=False

      cursor = db.cursor()
      sql = """SELECT * FROM prepositions WHERE question=%s OR question=%s OR question=%s"""

      try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3])
            result = cursor.fetchall()

            if result:
                for row in result:
                    if row[1]==question1:
                        question1_exist=True
                    elif row[1]==question2:
                        question2_exist=True
                    elif row[1]==question3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'question1':question1, 'question2':question2, 'question3':question3, 'correct1':Q1correct, 'Q1answer1':Q1answer1, 'Q1answer2':Q1answer2,'Q1answer3':Q1answer3,'correct2':Q2correct, 'Q2answer1':Q2answer1, 'Q2answer2':Q2answer2,'Q2answer3':Q2answer3,'correct3':Q3correct, 'Q3answer1':Q3answer1, 'Q3answer2':Q3answer2,'Q3answer3':Q3answer3, 'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('add_preposition_questions.html', errors=errors)
                #flash('Question successfully added !')

      except:
            # Rollback in case there is any error
            db.rollback()

      rows = []
      if question1 != '' and Q1correct != '' and Q1answer1 != '' and Q1answer2 != '' and Q1answer3 != '':
            array = [Q1correct, Q1answer1, Q1answer2, Q1answer3]
            shuffle(array)
            rows.append((array[0],array[1],array[2],array[3],Q1correct,question1,author))

      if question2 != '' and Q2correct != '' and Q2answer1 != '' and Q2answer2 != '' and Q2answer3 != '':
            array = [Q2correct, Q2answer1, Q2answer2, Q2answer3]
            shuffle(array)
            rows.append((array[0],array[1],array[2],array[3],Q2correct,question2,author))

      if question3 != '' and Q3correct != '' and Q3answer1 != '' and Q3answer2 != '' and Q3answer3 != '':
            array = [Q3correct, Q3answer1, Q3answer2, Q3answer3]
            shuffle(array)
            rows.append((array[0],array[1],array[2],array[3],Q3correct,question3,author))

      cursor = db.cursor()
      sql = """INSERT INTO prepositions (answer1,answer2,answer3,answer4,correct,question,author) VALUES(%s,%s,%s,%s,%s,%s,%s)"""

      try:
            # Execute the SQL command
            cursor.executemany(sql, rows)
            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Question Added Successfully !', title='English Buddy', button='OK')
      except:
            # Rollback in case there is any error
            db.rollback()

      return render_template('add_preposition_questions.html')


##View all Preposition Questions
@app.route('/editPreQuestions')
def editPreQuestions():
    cursor = db.cursor()

    sql = """SELECT id,question FROM prepositions where author=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()
    return render_template('EditPreQuestion.html', data=query)


## Edit preposition ##
@app.route('/edit_preposition', methods=['GET', 'POST'])
def edit_preposition():
    id = request.args['id']

    cursor = db.cursor()
    sql = """SELECT * FROM prepositions where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [id])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            question = row[1]
            correct = row[2]
            answer1 = row[3]
            answer2 = row[4]
            answer3 = row[5]
            answer4 = row[6]
    except:
        db.rollback()

    return json.dumps(
        dict(question=question, correct=correct, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4))


## Save edited prepositions question ##
@app.route('/save_edited_preposition', methods=['POST'])
def save_edited_preposition():
    id = request.form['id']
    question = request.form['inputQues']
    correct = request.form['correct']
    Answer1 = request.form['Answer1']
    Answer2 = request.form['Answer2']
    Answer3 = request.form['Answer3']
    Answer4 = request.form['Answer4']

    cursor = db.cursor()
    sql = """update prepositions set question=%s,correct=%s,answer1=%s,answer2=%s,answer3=%s,answer4=%s where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [question, correct, Answer1, Answer2, Answer3, Answer4, id])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('editPreQuestions'))


## Delete Preposition Question ##
@app.route('/delete_preposition/', methods=['GET'])
def delete_preposition():
    id = request.args.get('qNo')

    cursor = db.cursor()
    sql = """delete from prepositions where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [id])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('editPreQuestions'))


## level 1 prepositions activity ##
@app.route('/viewPrepositions')
def viewPrepositions():
    cursor = db.cursor()
    sql = """SELECT * FROM prepositions order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return render_template('prepositions.html', data=query)


## ------------------------------------------ Articles ---------------------------------------- ##

## Articles Questions for level 1 ##
@app.route('/add_articles_questions')
def add_articles_questions():
    return render_template('add_articles_questions.html')


## Add Articles question for level 1 ##
@app.route('/save_articles_questions', methods=['POST'])
def save_articles_questions():
    if request.method == 'POST':

        question1 = request.form['question_1']
        question2 = request.form['question_2']
        question3 = request.form['question_3']
        answer1 = request.form['answer_1']
        answer2 = request.form['answer_2']
        answer3 = request.form['answer_3']
        author = session['username']

        question1_exist=False
        question2_exist=False
        question3_exist=False

        cursor = db.cursor()
        sql = """SELECT * FROM level1_articles WHERE question=%s OR question=%s OR question=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3])
            result = cursor.fetchall()

            if result:
                for row in result:
                    if row[1]==question1:
                        question1_exist=True
                    elif row[1]==question2:
                        question2_exist=True
                    elif row[1]==question3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'question1':question1, 'question2':question2, 'question3':question3, 'answer1':answer1, 'answer2':answer2, 'answer3':answer3, 'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('add_articles_questions.html', errors=errors)
            #flash('Question successfully added !')

        except:
            # Rollback in case there is any error
            db.rollback()

        rows = []
        if question1 != '' and answer1 != '':
            rows.append((question1, answer1, author))
        if question2 != '' and answer2 != '':
            rows.append((question2, answer2, author))
        if question3 != '' and answer3 != '':
            rows.append((question3, answer3, author))

        print rows
        cursor = db.cursor()
        sql = """INSERT INTO level1_articles (question,answer,author,level) VALUES(%s,%s,%s,'level1')"""

        try:
            # Execute the SQL command
            cursor.executemany(sql, rows)

            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Question Added Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('add_articles_questions'))


## Display all article questions ##
@app.route('/display_article_questions')
def display_article_questions():
    cursor = db.cursor()
    sql = """SELECT * FROM level1_articles where author=%s """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_article_questions.html', data=result)


## Edit article questions ##
@app.route('/edit_article', methods=['GET', 'POST'])
def edit_article():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """SELECT * FROM level1_articles where level='level1' and author=%s and articleId=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[1]
            answer = row[2]

    except:
        db.rollback()

    return json.dumps(dict(question=question, answer=answer))


## Save edited article question for level 1 ##
@app.route('/save_edited_article_question', methods=['POST'])
def save_edited_article_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        question = request.form['question']
        answer = request.form['answer']
        author = session['username']
        #print author

        cursor = db.cursor()
        sql = """UPDATE level1_articles SET question=%s,answer=%s WHERE articleId=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question, answer, qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('display_article_questions'))


## Delete article questions ##
@app.route('/delete_article_questions/', methods=['GET'])
def delete_article_questions():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """DELETE FROM level1_articles where articleId=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_article_questions'))


## Level 1 Article Activity ##
@app.route('/Level1article')
def Level1article():
    cursor = db.cursor()
    sql = """SELECT * FROM level1_articles order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return render_template('Level1article.html', data=query)



## Level 1 Test ##
@app.route('/level1_test')
def level1_test():

    #Conjunction Question
    array=[]
    cursor = db.cursor()
    sql = """SELECT * FROM conjunctions where level='level1' order by rand() limit 5 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        conjunctionResult = cursor.fetchall()
        for row in conjunctionResult:
            answer = row[3]
            array.append(answer)
    except:
        # Rollback in case there is any error
        db.rollback()

    shuffle(array)
    shuffledData = {'shuffledArray': array}


    #Article Question
    cursor = db.cursor()
    sql = """SELECT * FROM level1_articles order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch a single row using fetchone() method.
        articleResult = cursor.fetchall()
    except:
        db.rollback()


    #Preposition Question
    cursor = db.cursor()
    sql = """SELECT * FROM prepositions order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch a single row using fetchone() method.
        prepositionResult = cursor.fetchall()
    except:
        db.rollback()


    #Adjective Question
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_1_adjectives order by rand() limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        adjectiveResult = cursor.fetchall()
    except:
        db.rollback()


    return render_template('level1_test.html', conjunctionData=conjunctionResult, shuffledData=shuffledData, articleData=articleResult, prepositionData=prepositionResult, adjectiveData=adjectiveResult)


## Evaluate level1 test ##
@app.route('/evaluate_level1_test', methods=['POST'])
def evaluate_level1_test():
    if request.method == 'POST':
        marks = 0

        #Conjunction
        conjunction_provided_answer1=request.form['conjunction_provided_answer1']
        conjunction_provided_answer2=request.form['conjunction_provided_answer2']
        conjunction_provided_answer3=request.form['conjunction_provided_answer3']
        conjunction_provided_answer4=request.form['conjunction_provided_answer4']
        conjunction_provided_answer5=request.form['conjunction_provided_answer5']

        conjunction_correct_answer1=request.form['conjunction_correct_answer1']
        conjunction_correct_answer2=request.form['conjunction_correct_answer2']
        conjunction_correct_answer3=request.form['conjunction_correct_answer3']
        conjunction_correct_answer4=request.form['conjunction_correct_answer4']
        conjunction_correct_answer5=request.form['conjunction_correct_answer5']

        #Articles
        article_provided_answer1=request.form['article_provided_answer1']
        article_provided_answer2=request.form['article_provided_answer2']
        article_provided_answer3=request.form['article_provided_answer3']
        article_provided_answer4=request.form['article_provided_answer4']
        article_provided_answer5=request.form['article_provided_answer5']

        article_correct_answer1=request.form['article_correct_answer1']
        article_correct_answer2=request.form['article_correct_answer2']
        article_correct_answer3=request.form['article_correct_answer3']
        article_correct_answer4=request.form['article_correct_answer4']
        article_correct_answer5=request.form['article_correct_answer5']

        #Prepositions
        preposition_provided_answer1=request.form['preposition_provided_answer1']
        preposition_provided_answer2=request.form['preposition_provided_answer2']
        preposition_provided_answer3=request.form['preposition_provided_answer3']
        preposition_provided_answer4=request.form['preposition_provided_answer4']
        preposition_provided_answer5=request.form['preposition_provided_answer5']

        preposition_correct_answer1=request.form['preposition_correct_answer1']
        preposition_correct_answer2=request.form['preposition_correct_answer2']
        preposition_correct_answer3=request.form['preposition_correct_answer3']
        preposition_correct_answer4=request.form['preposition_correct_answer4']
        preposition_correct_answer5=request.form['preposition_correct_answer5']

        #Adjectives
        adjectives_provided_answer1=request.form['adjectives_provided_answer1']
        adjectives_provided_answer2=request.form['adjectives_provided_answer2']
        adjectives_provided_answer3=request.form['adjectives_provided_answer3']
        adjectives_provided_answer4=request.form['adjectives_provided_answer4']
        adjectives_provided_answer5=request.form['adjectives_provided_answer5']

        adjectives_correct_answer1=request.form['adjectives_correct_answer1']
        adjectives_correct_answer2=request.form['adjectives_correct_answer2']
        adjectives_correct_answer3=request.form['adjectives_correct_answer3']
        adjectives_correct_answer4=request.form['adjectives_correct_answer4']
        adjectives_correct_answer5=request.form['adjectives_correct_answer5']

        if conjunction_provided_answer1==conjunction_correct_answer1:
            marks=marks+1
        if conjunction_provided_answer2==conjunction_correct_answer2:
            marks=marks+1
        if conjunction_provided_answer3==conjunction_correct_answer3:
            marks=marks+1
        if conjunction_provided_answer4==conjunction_correct_answer4:
            marks=marks+1
        if conjunction_provided_answer5==conjunction_correct_answer5:
            marks=marks+1

        if article_provided_answer1==article_correct_answer1:
            marks=marks+1
        if article_provided_answer2==article_correct_answer2:
            marks=marks+1
        if article_provided_answer3==article_correct_answer3:
            marks=marks+1
        if article_provided_answer4==article_correct_answer4:
            marks=marks+1
        if article_provided_answer5==article_correct_answer5:
            marks=marks+1

        if preposition_provided_answer1==preposition_correct_answer1:
            marks=marks+1
        if preposition_provided_answer2==preposition_correct_answer2:
            marks=marks+1
        if preposition_provided_answer3==preposition_correct_answer3:
            marks=marks+1
        if preposition_provided_answer4==preposition_correct_answer4:
            marks=marks+1
        if preposition_provided_answer5==preposition_correct_answer5:
            marks=marks+1

        if adjectives_provided_answer1==adjectives_correct_answer1:
            marks=marks+1
        if adjectives_provided_answer2==adjectives_correct_answer2:
            marks=marks+1
        if adjectives_provided_answer3==adjectives_correct_answer3:
            marks=marks+1
        if adjectives_provided_answer4==adjectives_correct_answer4:
            marks=marks+1
        if adjectives_provided_answer5==adjectives_correct_answer5:
            marks=marks+1

        marks_percentage=float(marks)/20*100

        if marks_percentage>=75:
            level='Preliminary'

            if session['level']=='Elementary':
                cursor = db.cursor()
                sql = """update users set placement_test=%s where email=%s"""
                try:
                    cursor.execute(sql, [level, session['username']])
                    db.commit()
                except:
                    db.rollback()
        else:
            level='Elementary'

        data = {'marks': marks, 'level': level}

    return render_template('level1_test_report.html', data=data)




## ----------------------------------- LEVEL 2 - PRELIMINARY LEVEL ----------------------------------


# ----------------------- Level 2 - Dialog ----------------------------------------------------------

## Dialog Questions for level 2 ##
@app.route('/add_dialog_questions')
def add_dialog_questions():
    return render_template('add_dialog_questions.html')


## Add dialog question for level 2 ##
@app.route('/save_dialog_question', methods=['POST'])
def save_dialog_question():
    if request.method == 'POST':

        question = request.form['question']
        answers = request.form['answers']
        a1 = request.form['answer1']
        a2 = request.form['answer2']
        a3 = request.form['answer3']
        a4 = request.form['answer4']
        a5 = request.form['answer5']
        author = session['username']

        cursor = db.cursor()
        sql = """INSERT INTO dialogs (level,question,answers,a1,a2,a3,a4,a5,author) VALUES('level2',%s,%s,%s,%s,%s,%s,%s,%s)"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question, answers, a1, a2, a3, a4, a5, author])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    alert(text='Question Added Successfully !', title='English Buddy', button='OK')
    return redirect(url_for('add_dialog_questions'))


## Display all dialog questions ##
@app.route('/display_dialog_questions/', methods=['GET'])
def display_dialog_questions():

    level = request.args.get('level')

    cursor = db.cursor()
    if level=='level2':
        sql = """SELECT * FROM dialogs where author=%s AND level=%s"""
        try:
            # Execute the SQL command select all rows
            cursor.execute(sql, [session['username'], level])
            # fetch rows using fetchall() method.
            result = cursor.fetchall()
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        return render_template('display_dialog_questions.html', data=result)

    elif level=='level4':
        sql = """SELECT * FROM level4_dialogs where author=%s"""
        try:
            # Execute the SQL command select all rows
            cursor.execute(sql, [session['username']])
            # fetch rows using fetchall() method.
            result = cursor.fetchall()
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        return render_template('display_dialog_questions_level4.html', data=result)


## Edit dialog questions ##
@app.route('/edit_dialog', methods=['GET', 'POST'])
def edit_dialog():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """SELECT * FROM dialogs where level='level2' and author=%s and qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[2]
            answer = row[3]
            a1 = row[4]
            a2 = row[5]
            a3 = row[6]
            a4 = row[7]
            a5 = row[8]
    except:
        db.rollback()

    session['level2DialogQuestion']=question
    session['level2DialogAnswer']=answer

    return json.dumps(dict(question=question, answer=answer, a1=a1, a2=a2, a3=a3, a4=a4, a5=a5))


## Save edited dialog question for level 2 ##
@app.route('/save_edited_dialog_question', methods=['POST'])
def save_edited_dialog_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        question = request.form['question']
        answers = request.form['answers']
        a1 = request.form['answer1']
        a2 = request.form['answer2']
        a3 = request.form['answer3']
        a4 = request.form['answer4']
        a5 = request.form['answer5']

        cursor = db.cursor()
        sql = """UPDATE dialogs SET question=%s,answers=%s,a1=%s,a2=%s,a3=%s,a4=%s,a5=%s WHERE qNo=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question, answers, a1, a2, a3, a4, a5, qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('display_dialog_questions'))


## Delete dialog questions ##
@app.route('/delete_dialog_questions/', methods=['GET'])
def delete_dialog_questions():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """DELETE FROM dialogs where qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_dialog_questions'))


## Level 2 dialog Activity ##
@app.route('/level1_dialogs')
def level1_dialogs():
    cursor = db.cursor()
    sql = """SELECT * FROM dialogs where level='level2' order by rand() limit 1 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('level1_dialogs.html', data=result)


## Evaluate level2 dialog question answers ##
@app.route('/evaluate_level1_dialogs', methods=['POST'])
def evaluate_level1_dialogs():
    if request.method == 'POST':
        marks = 0
        qNo = request.form['qNo']
        pa1 = request.form['one']
        pa2 = request.form['two']
        pa3 = request.form['three']
        pa4 = request.form['four']
        pa5 = request.form['five']

        cursor = db.cursor()
        sql = """SELECT * FROM dialogs where qNo=%s"""
        try:
            # Execute the SQL command
            cursor.execute(sql, [qNo])

            # fetch a single row using fetchone() method.
            data = cursor.fetchall()
            for row in data:
                a1 = row[4]
                a2 = row[5]
                a3 = row[6]
                a4 = row[7]
                a5 = row[8]
                question = row[2]
                answers = row[3]

            if a1 == pa1:
                a1_status = "Correct"
                marks = marks + 1
            else:
                a1_status = "Wrong"

            if a2 == pa2:
                a2_status = "Correct"
                marks = marks + 1
            else:
                a2_status = "Wrong"

            if a3 == pa3:
                a3_status = "Correct"
                marks = marks + 1
            else:
                a3_status = "Wrong"

            if a4 == pa4:
                a4_status = "Correct"
                marks = marks + 1
            else:
                a4_status = "Wrong"

            if a5 == pa5:
                a5_status = "Correct"
                marks = marks + 1
            else:
                a5_status = "Wrong"

            #print marks

            data_array = {'qNo': qNo, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'question': question,
                          'pa1': pa1, 'pa2': pa2, 'pa3': pa3, 'pa4': pa4, 'pa5': pa5, 'a1_status': a1_status, 'a2_status': a2_status, 'a3_status': a3_status,
                          'a4_status': a4_status, 'a5_status': a5_status, 'marks': marks,
                          'answers': answers}

            return render_template('level1_dialogs_answers.html', data=data_array)

            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('level1_dialogs'))


## Show level2 dialog question answers ##
@app.route('/display_level1_dialog_answers')
def display_level1_dialog_answers():
    return render_template('level1_dialogs_answers.html')


#------------------------------------ Pronouns ----------------------------

## Display Add pronoun question question page ##
@app.route('/AddQues_pronoun')
def AddQues_pronoun():
    return render_template('AddQues_pronoun.html')


## Add pronoun question ##
@app.route('/Save_pronoun', methods=['POST'])
def Save_pronoun():
    question1 = request.form['txtQuestion1']
    question2 = request.form['txtQuestion2']
    question3 = request.form['txtQuestion3']
    answer1 = request.form['txtAnswer1']
    answer2 = request.form['txtAnswer2']
    answer3 = request.form['txtAnswer3']
    author = session['username']

    question1_exist = False
    question2_exist = False
    question3_exist = False

    cursor = db.cursor()
    sql = """SELECT * FROM level_2_pronoun WHERE question=%s OR question=%s OR question=%s"""

    try:
        # Execute the SQL command
        cursor.execute(sql, [question1, question2, question3])
        result = cursor.fetchall()

        if result:
            for row in result:
                if row[1] == question1:
                    question1_exist = True
                elif row[1] == question2:
                    question2_exist = True
                elif row[1] == question3:
                    question3_exist = True

            alert(text='Questions Already exists !', title='English Buddy', button='OK')
            errors = {'question1': question1, 'question2': question2, 'question3': question3, 'answer1': answer1,
                      'answer2': answer2, 'answer3': answer3, 'question1Status': question1_exist,
                      'question2Status': question2_exist, 'question3Status': question3_exist}

            return render_template('AddQues_pronoun.html', errors=errors)
            #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    rows = []
    if question1 != '' and answer1 != '':
        rows.append((question1, answer1, author))
    if question2 != '' and answer2 != '':
        rows.append((question2, answer2, author))
    if question3 != '' and answer3 != '':
        rows.append((question3, answer3, author))

    cursor = db.cursor()
    sql = """INSERT INTO level_2_pronoun (question,answer,author) VALUES(%s,%s,%s)"""

    try:
        # Execute the SQL command
        cursor.executemany(sql, rows)
        # Commit your changes in the database
        db.commit()
        #flash('Question successfully added !')
        alert(text='Questions Added Successfully !', title='English Buddy', button='OK')
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('AddQues_pronoun'))


## View all pronoun questions ##
@app.route('/Update_pronoun')
def Update_pronoun():
    cursor = db.cursor()

    sql = """SELECT qno,question,answer FROM level_2_pronoun where author=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()
    return render_template('Update_pronoun.html', data=query)


## Edit pronoun question ##
@app.route('/edit_pronoun', methods=['GET', 'POST'])
def edit_pronoun():
    qno = request.args['qno']

    cursor = db.cursor()
    sql = """SELECT * FROM level_2_pronoun where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [qno])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            question = row[1]
            answer = row[2]

    except:
        db.rollback()

    return json.dumps(dict(question=question, answer=answer))


## Save updated pronoun question data in the database ##
@app.route('/save_edited_pronoun', methods=['POST'])
def save_edited_pronoun():
    qno = request.form['qno']
    question = request.form['question']
    answer = request.form['answer']

    cursor = db.cursor()
    sql = """UPDATE level_2_pronoun SET question=%s,answer=%s WHERE qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [question, answer, qno])
        db.commit()
        # fetch a single row using fetchone() method.
    except:
        db.rollback()

    return redirect(url_for('Update_pronoun'))


## Delete pronoun question ##
@app.route('/delete_pronoun/', methods=['GET'])
def delete_pronoun():
    qno = request.args.get('qNo')

    cursor = db.cursor()
    sql = """delete from level_2_pronoun where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [qno])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('Update_pronoun'))


## Level 2 Pronouns Activity
@app.route('/level_2_pronoun')
def level_2_pronoun():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_2_pronoun order by rand() limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        query = cursor.fetchall()
    except:
        db.rollback()
        db.close()

    return render_template('level_2_pronoun.html', data=query)


# --------------------------------------- Level 2 Match (Synonyms) ------------------------------------------

## Matching Words Questions for level 1 ##
@app.route('/add_matching_words_questions')
def add_matching_words_questions():
    return render_template('add_matching_words_questions.html')


## Add Matching Words question for level 1 ##
@app.route('/save_matching_words_questions', methods=['POST'])
def save_matching_words_questions():
    if request.method == 'POST':

        question1 = request.form['question_1']
        question2 = request.form['question_2']
        question3 = request.form['question_3']
        answer1 = request.form['answer_1']
        answer2 = request.form['answer_2']
        answer3 = request.form['answer_3']
        author = session['username']

        question1_exist=False
        question2_exist=False
        question3_exist=False

        cursor = db.cursor()
        sql = """SELECT * FROM level2_match WHERE question=%s OR question=%s OR question=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3])
            result = cursor.fetchall()

            if result:
                for row in result:
                    if row[1]==question1:
                        question1_exist=True
                    elif row[1]==question2:
                        question2_exist=True
                    elif row[1]==question3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'question1':question1, 'question2':question2, 'question3':question3, 'answer1':answer1, 'answer2':answer2, 'answer3':answer3, 'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('add_matching_words_questions.html', errors=errors)
            #flash('Question successfully added !')

        except:
            # Rollback in case there is any error
            db.rollback()

        rows = []
        if question1 != '' and answer1 != '':
            rows.append((question1, answer1, author))
        if question2 != '' and answer2 != '':
            rows.append((question2, answer2, author))
        if question3 != '' and answer3 != '':
            rows.append((question3, answer3, author))

        #print rows
        cursor = db.cursor()
        sql = """INSERT INTO level2_match (level,question,answer,author) VALUES('level2',%s,%s,%s)"""

        try:
            # Execute the SQL command
            cursor.executemany(sql, rows)
            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Question Added Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('add_matching_words_questions'))


## Display all matchWords questions ##
@app.route('/display_match_words_questions')
def display_match_words_questions():
    cursor = db.cursor()
    sql = """SELECT * FROM level2_match where author=%s """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_match_words_questions.html', data=result)


## Edit matchWords questions ##
@app.route('/edit_match_words', methods=['GET', 'POST'])
def edit_match_words():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """SELECT * FROM level2_match where level='level2' and author=%s and matchId=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[1]
            answer = row[2]

    except:
        db.rollback()

    return json.dumps(dict(question=question, answer=answer))


## Save edited matchWords question for level 1 ##
@app.route('/save_edited_match_words_question', methods=['POST'])
def save_edited_match_words_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        question = request.form['question']
        answer = request.form['answer']
        author = session['username']
        #print author

        cursor = db.cursor()
        sql = """UPDATE level2_match SET question=%s,answer=%s WHERE matchId=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question, answer, qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('display_match_words_questions'))


## Delete matchWords questions ##
@app.route('/delete_match_words_questions/', methods=['GET'])
def delete_match_words_questions():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """DELETE FROM level2_match where matchId=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_match_words_questions'))


## Level 2 Match (Synonyms) Activity ##
@app.route('/Level2Match')
def Level2Match():
    cursor = db.cursor()
    sql = """SELECT * FROM level2_match order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return render_template('Level2Match.html', data=query)


## ------------------------------------------ Jumble Sentences ---------------------------------------- ##

## Display Add jumble sentences question ##
@app.route('/add_jumble_sentences')
def add_jumble_sentences():
    return render_template('Add_JumbleSentences.html')


## Add jumble sentences question ##
@app.route('/AddJumbleSentences', methods=['POST'])
def AddJumbleSentences():

    wrongSentence1 = request.form['txtWrong1']
    correctSentence1 = request.form['txtCorrect1']
    wrongSentence2 = request.form['txtWrong2']
    correctSentence2 = request.form['txtCorrect2']
    wrongSentence3 = request.form['txtWrong3']
    correctSentence3 = request.form['txtCorrect3']

    question1_exist=False
    question2_exist=False
    question3_exist=False

    cursor = db.cursor()
    sql ="""SELECT * FROM jumblesentences WHERE wrong_sentence=%s OR wrong_sentence=%s OR wrong_sentence=%s"""
    try:    # Execute the SQL command
             cursor.execute(sql,[wrongSentence1,wrongSentence2,wrongSentence3])
             result = cursor.fetchall()

             print(cursor.fetchall())
             if result:
                for row in result:
                    if row[1]==wrongSentence1:
                        question1_exist=True
                    elif row[1]== wrongSentence2:
                        question2_exist=True
                    elif row[1]==wrongSentence3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'wrongsentence1':wrongSentence1, 'wrongsentence2':wrongSentence2, 'wrongsentence3':wrongSentence3, 'correctSentence1':correctSentence1, 'correctSentence2':correctSentence2, 'correctSentence3':correctSentence3,'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('Add_JumbleSentences.html', errors=errors)
                #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    rows = []
    if request.form.get('txtWrong1') != '' and request.form.get('txtCorrect1') != '':
        wrongSentence1 = request.form['txtWrong1']
        correctSentence1 = request.form['txtCorrect1']
        rows.append(( wrongSentence1.strip(), correctSentence1.strip(), session['username']))
    if request.form.get('txtWrong2') != '' and request.form.get('txtCorrect2') != '':
        wrongSentence2 = request.form['txtWrong2']
        correctSentence2 = request.form['txtCorrect2']
        rows.append(( wrongSentence2.strip(), correctSentence2.strip(), session['username']))
    if request.form.get('txtWrong3') != '' and request.form.get('txtCorrect3') != '':
        wrongSentence3 = request.form['txtWrong3']
        correctSentence3 = request.form['txtCorrect3']
        rows.append(( wrongSentence3.strip(), correctSentence3.strip(), session['username']))
    cursor = db.cursor()
    sql = """INSERT INTO jumblesentences (wrong_sentence,correct_sentence,author) VALUES(%s,%s,%s)"""

    try:
        # Execute the SQL command
        #cursor.execute(sql,[qusetion1,answer1])
        print 'add'
        cursor.executemany(sql, rows)
        db.commit()
    except:
        db.rollback()
    return render_template('Add_JumbleSentences.html')


## Show all jumble sentences questions ##
@app.route('/editJumbleQuestions')
def editJumbleQuestions():
    cursor = db.cursor()
    sql = """SELECT * FROM jumblesentences where author=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return render_template('EditJumbleSentences.html', data=query)


## Edit jumble sentences question ##
@app.route('/edit_jumbleSentences', methods=['GET', 'POST'])
def edit_jumbleSentences():
    id = request.args['id']

    cursor = db.cursor()
    sql = """SELECT * FROM jumblesentences where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [id])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            wrong = row[1]
            correct = row[2]
    except:
        db.rollback()

    return json.dumps(dict(wrong=wrong, correct=correct))


## Save edited jumble sentences question ##
@app.route('/save_edited_jumblesentences', methods=['POST'])
def save_edited_jumbleSentences():
    id = request.form['id']
    wrong = request.form['wrong']
    correct = request.form['correct']

    cursor = db.cursor()
    sql = """update jumblesentences set wrong_sentence=%s,correct_sentence=%s where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [wrong, correct, id])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('editJumbleQuestions'))


## Delete jumble sentences question ##
@app.route('/delete_jumbleSentences/', methods=['GET'])
def delete_jumbleSentences():
    id = request.args.get('qNo')

    cursor = db.cursor()
    sql = """delete from jumblesentences  where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [id])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('editJumbleQuestions'))


## Level 2 Jumble Sentences Activity ##
@app.route('/viewJumbleSentences')
def viewJumbleSentences():
    cursor = db.cursor()
    sql = """SELECT * FROM jumblesentences order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return render_template('JumbleSentences.html', data=query)



## Level 2 Test##
@app.route('/level2_test')
def level2_test():

    #Pronoun Question
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_2_pronoun order by rand() limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        pronounResult = cursor.fetchall()
    except:
        db.rollback()

    #Jumble Sentences Question
    cursor = db.cursor()
    sql = """SELECT * FROM jumblesentences order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch a single row using fetchone() method.
        jumbleSentenceResult = cursor.fetchall()
    except:
        db.rollback()

    #Match words Question
    cursor = db.cursor()
    sql = """SELECT * FROM level2_match order by rand()limit 5"""
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch a single row using fetchone() method.
        matchWordsResult = cursor.fetchall()
    except:
        db.rollback()

    #Dialogue Question
    cursor = db.cursor()
    sql = """SELECT * FROM dialogs where level='level2' order by rand() limit 1 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        dialogResult = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('level2_test.html', pronounData=pronounResult, jumbleSentenceData=jumbleSentenceResult, matchWordsData=matchWordsResult, dialogData=dialogResult)


## Evaluate level2 test ##
@app.route('/evaluate_level2_test', methods=['POST'])
def evaluate_level2_test():
    if request.method == 'POST':
        marks = 0
        #pronuon
        pronoun_correct_answer1=request.form['pronoun_correct_answer1']
        pronoun_correct_answer2=request.form['pronoun_correct_answer2']
        pronoun_correct_answer3=request.form['pronoun_correct_answer3']
        pronoun_correct_answer4=request.form['pronoun_correct_answer4']
        pronoun_correct_answer5=request.form['pronoun_correct_answer5']

        pronoun_provided_answer1=request.form['pronoun_provided_answer1']
        pronoun_provided_answer2=request.form['pronoun_provided_answer2']
        pronoun_provided_answer3=request.form['pronoun_provided_answer3']
        pronoun_provided_answer4=request.form['pronoun_provided_answer4']
        pronoun_provided_answer5=request.form['pronoun_provided_answer5']


        #jumble Sentences
        jumbleSentences_correct1=request.form['jumbleSentence_correct_answer1']
        jumbleSentences_correct2=request.form['jumbleSentence_correct_answer2']
        jumbleSentences_correct3=request.form['jumbleSentence_correct_answer3']
        jumbleSentences_correct4=request.form['jumbleSentence_correct_answer4']
        jumbleSentences_correct5=request.form['jumbleSentence_correct_answer5']

        jumbleSentence_provided_answer1=request.form['jumbleSentence_provided_answer1']
        jumbleSentence_provided_answer2=request.form['jumbleSentence_provided_answer2']
        jumbleSentence_provided_answer3=request.form['jumbleSentence_provided_answer3']
        jumbleSentence_provided_answer4=request.form['jumbleSentence_provided_answer4']
        jumbleSentence_provided_answer5=request.form['jumbleSentence_provided_answer5']

        #dialogs

        dialog_provided_answer1=request.form['dialog_provided_answer1']
        dialog_provided_answer2=request.form['dialog_provided_answer2']
        dialog_provided_answer3=request.form['dialog_provided_answer3']
        dialog_provided_answer4=request.form['dialog_provided_answer4']
        dialog_provided_answer5=request.form['dialog_provided_answer5']

        dialog_correct_answer1=request.form['dialog_correct_answer1']
        dialog_correct_answer2=request.form['dialog_correct_answer2']
        dialog_correct_answer3=request.form['dialog_correct_answer3']
        dialog_correct_answer4=request.form['dialog_correct_answer4']
        dialog_correct_answer5=request.form['dialog_correct_answer5']

        matchMarks=request.form['matchMarks']
        print matchMarks

        if pronoun_provided_answer1==pronoun_correct_answer1:
            marks=marks+1

        if pronoun_provided_answer2==pronoun_correct_answer2:
            marks=marks+1

        if pronoun_provided_answer3==pronoun_correct_answer3:
            marks=marks+1

        if pronoun_provided_answer4==pronoun_correct_answer4:
            marks=marks+1

        if pronoun_provided_answer5==pronoun_correct_answer5:
            marks=marks+1

        if jumbleSentence_provided_answer1.strip()==jumbleSentences_correct1:
            marks=marks+1

        if jumbleSentence_provided_answer2.strip()==jumbleSentences_correct2:
            marks=marks+1

        if jumbleSentence_provided_answer3.strip()==jumbleSentences_correct3:
            marks=marks+1

        if jumbleSentence_provided_answer4.strip()==jumbleSentences_correct4:
            marks=marks+1

        if jumbleSentence_provided_answer5.strip()==jumbleSentences_correct5:
            marks=marks+1

        if dialog_provided_answer1==dialog_correct_answer1:
            marks=marks+1

        if dialog_provided_answer2==dialog_correct_answer2:
            marks=marks+1

        if dialog_provided_answer3==dialog_correct_answer3:
            marks=marks+1

        if dialog_provided_answer4==dialog_correct_answer4:
            marks=marks+1

        if dialog_provided_answer5==dialog_correct_answer5:
            marks=marks+1

        newMarks=marks+int(matchMarks)
        
        marks_out_of_100=float(newMarks)/20*100


        if marks_out_of_100>=75:
            level='Intermediate'

            if session['level']=='Preliminary':
                cursor = db.cursor()
                sql = """update users set placement_test=%s where email=%s"""
                try:
                    cursor.execute(sql, [level, session['username']])
                    db.commit()
                except:
                    db.rollback()
        else:
            level='Preliminary'

        data = {'marks': marks_out_of_100, 'level': level, 'correct': newMarks}

    return render_template('level2_test_report.html', data=data)




## ------------------------------------- Level 3 ----------------------------------------------- ##

# ------------------------ Level 3 - Conjunctions ----------------------------------------------- #

## Display Add Conjunction Questions for level 3 ##
@app.route('/level3_add_conjunction_questions')
def level3_add_conjunction_questions():
    return render_template('level3_add_conjunction_questions.html')


## Add conjunction question for level 3 ##
@app.route('/level3_save_conjunction_question', methods=['POST'])
def level3_save_conjunction_question():
    if request.method == 'POST':

        question1 = request.form['question_1']
        question2 = request.form['question_2']
        question3 = request.form['question_3']
        author = session['username']

        rows = []
        if question1 != '':
            rows.append((question1, author))
        if question2 != '':
            rows.append((question2, author))
        if question3 != '':
            rows.append((question3, author))

        cursor = db.cursor()
        sql = """INSERT INTO level3_conjunctions (level,question,author) VALUES('level3',%s,%s)"""

        try:
            # Execute the SQL command
            cursor.executemany(sql, rows)
            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Question Added Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('level3_add_conjunction_questions'))


# # Edit level 3 conjunction questions ##
@app.route('/level3_edit_conjunction', methods=['GET', 'POST'])
def level3_edit_conjunction():
    qNo = request.args.get('qNo')
    level = 'level3'
    cursor = db.cursor()
    sql = """SELECT * FROM level3_conjunctions where level=%s and author=%s and qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [level, session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[2]
    except:
        db.rollback()

    return json.dumps(dict(question=question))


## Level 3 Conjunctions Activity ##
@app.route('/level3_conjunctions_activity')
def level3_conjunctions_activity():

    cursor = db.cursor()
    sql = """SELECT * FROM level3_conjunctions where level='level3' order by rand() limit 5 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('level3_conjunctions_activity.html', data=result)


## Level 3 Conjunction Evaluate Answers ##
@app.route('/evaluate_level3_conjunction_activity', methods=['POST'])
def evaluate_level3_conjunction_activity():

    if request.method == 'POST':

        marks = 0

        question1=request.form['question1']
        question2=request.form['question2']
        question3=request.form['question3']
        question4=request.form['question4']
        question5=request.form['question5']

        pa1 = request.form['one'].strip()
        pa2 = request.form['two'].strip()
        pa3 = request.form['three'].strip()
        pa4 = request.form['four'].strip()
        pa5 = request.form['five'].strip()

        #Capitalize the first letter of the question
        if question1.split(" ")[0]=='#,' or question1.split(" ")[0]=='#':
            pa1=pa1.capitalize()
        if question2.split(" ")[0]=='#,' or question2.split(" ")[0]=='#':
            pa2=pa2.capitalize()
        if question3.split(" ")[0]=='#,' or question3.split(" ")[0]=='#':
            pa3=pa3.capitalize()
        if question4.split(" ")[0]=='#,' or question4.split(" ")[0]=='#':
            pa4=pa4.capitalize()
        if question5.split(" ")[0]=='#,' or question5.split(" ")[0]=='#':
            pa5=pa5.capitalize()


        #Complete questions with provided answer
        complete_question1=question1.split("#")[0]+pa1+question1.split("#")[1]
        complete_question2=question2.split("#")[0]+pa2+question2.split("#")[1]
        complete_question3=question3.split("#")[0]+pa3+question3.split("#")[1]
        complete_question4=question4.split("#")[0]+pa4+question4.split("#")[1]
        complete_question5=question5.split("#")[0]+pa5+question5.split("#")[1]


        data = [['','',question1],['','',question2],['','',question3],['','',question4],['','',question5]]

        question1_suggestion=''
        question2_suggestion=''
        question3_suggestion=''
        question4_suggestion=''
        question5_suggestion=''


        # if ConjunctionClass.check(complete_question1, pa1):
        #     marks = marks + 1
        #     question1_status = "Correct"
        # else:
        #     question1_suggestion=ConjunctionClass.find_correct_conjunction(question1)
        #     question1_status = "Wrong"
        #
        # if ConjunctionClass.check(complete_question2, pa2):
        #     marks = marks + 1
        #     question2_status = "Correct"
        # else:
        #     question2_suggestion=ConjunctionClass.find_correct_conjunction(question2)
        #     question2_status = "Wrong"
        #
        # if ConjunctionClass.check(complete_question3, pa3):
        #     marks = marks + 1
        #     question3_status = "Correct"
        # else:
        #     question3_suggestion=ConjunctionClass.find_correct_conjunction(question3)
        #     question3_status = "Wrong"
        #
        # if ConjunctionClass.check(complete_question4, pa4):
        #     marks = marks + 1
        #     question4_status = "Correct"
        # else:
        #     question4_suggestion=ConjunctionClass.find_correct_conjunction(question4)
        #     question4_status = "Wrong"
        #
        # if ConjunctionClass.check(complete_question5, pa5):
        #     marks = marks + 1
        #     question5_status = "Correct"
        # else:
        #     question5_suggestion=ConjunctionClass.find_correct_conjunction(question5)
        #     question5_status = "Wrong"

        if CoordinatingConjunctionClass.check(complete_question1, pa1):
            marks = marks + 1
            question1_status = "Correct"
        else:
            question1_suggestion=CoordinatingConjunctionClass.find_correct_conjunction(question1)
            question1_status = "Wrong"

        if CoordinatingConjunctionClass.check(complete_question2, pa2):
            marks = marks + 1
            question2_status = "Correct"
        else:
            question2_suggestion=CoordinatingConjunctionClass.find_correct_conjunction(question2)
            question2_status = "Wrong"

        if CoordinatingConjunctionClass.check(complete_question3, pa3):
            marks = marks + 1
            question3_status = "Correct"
        else:
            question3_suggestion=CoordinatingConjunctionClass.find_correct_conjunction(question3)
            question3_status = "Wrong"

        if CoordinatingConjunctionClass.check(complete_question4, pa4):
            marks = marks + 1
            question4_status = "Correct"
        else:
            question4_suggestion=CoordinatingConjunctionClass.find_correct_conjunction(question4)
            question4_status = "Wrong"

        if CoordinatingConjunctionClass.check(complete_question5, pa5):
            marks = marks + 1
            question5_status = "Correct"
        else:
            question5_suggestion=CoordinatingConjunctionClass.find_correct_conjunction(question5)
            question5_status = "Wrong"


        data_array = {'pa1': pa1, 'pa2': pa2, 'pa3': pa3, 'pa4': pa4, 'pa5': pa5, 'a1': question1_suggestion, 'a2': question2_suggestion, 'a3': question3_suggestion, 'a4': question4_suggestion, 'a5': question5_suggestion,
                          'a1_status': question1_status, 'a2_status': question2_status, 'a3_status': question3_status,
                          'a4_status': question4_status, 'a5_status': question5_status, 'marks': marks}


        return render_template('level3_conjunctions_activity.html', answer_data=data_array, data=data)

    return redirect(url_for('level3_conjunctions_activity'))



# ------------------------ Level 3 - Notice/Invitation ----------------------------------------------- #
#Darani
## Notice or invitation Questions for level 1 ##
@app.route('/add_notice_invitation_questions')
def add_notice_invitation_questions():
    return render_template('add_notice_invitation_questions.html')


## Add notice or invitation question for level 1 ##
@app.route('/save_notice_invitation_questions', methods=['POST'])
def save_notice_invitation_questions():
    if request.method == 'POST':

        question1 = request.form['question_1']
        question2 = request.form['question_2']
        question3 = request.form['question_3']
        type1 = request.form['notice1']
        type2 = request.form['notice2']
        type3 = request.form['notice3']
        author = session['username']

        question1_exist=False
        question2_exist=False
        question3_exist=False

        cursor = db.cursor()
        sql = """SELECT * FROM level3_notice_invitation WHERE question=%s OR question=%s OR question=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3])
            result = cursor.fetchall()

            if result:
                for row in result:
                    if row[1]==question1:
                        question1_exist=True
                    elif row[1]==question2:
                        question2_exist=True
                    elif row[1]==question3:
                        question3_exist=True

                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'question1':question1, 'question2':question2, 'question3':question3, 'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('add_notice_invitation_questions.html', errors=errors)
            #flash('Question successfully added !')

        except:
            # Rollback in case there is any error
            db.rollback()
        if type1 == 'notice':
            type1_ = 'N'
        else :
            type1_ = 'I'

        if type2 == 'notice':
            type2_ = 'N'
        else :
            type2_ = 'I'

        if type3 == 'notice':
            type3_ = 'N'
        else :
            type3_ = 'I'

        rows = []
        if question1 != '' :
            rows.append((question1, author, type1_))
        if question2 != '' :
            rows.append((question2, author, type2_))
        if question3 != '' :
            rows.append((question3, author, type3_))

        print rows
        cursor = db.cursor()
        sql = """INSERT INTO level3_notice_invitation (question,author,type) VALUES(%s,%s,%s)"""

        try:
            # Execute the SQL command
            cursor.executemany(sql, rows)

            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Question Added Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('add_notice_invitation_questions'))


## Display all notice or invitation questions ##
@app.route('/display_notice_invitation_questions')
def display_notice_invitation_questions():
    cursor = db.cursor()
    sql = """SELECT * FROM level3_notice_invitation where author=%s """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database

        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_notice_invitation_questions.html', data=result)


## Edit notice or invitation questions ##
@app.route('/edit_notice_invitation', methods=['GET', 'POST'])
def edit_notice_invitation():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """SELECT * FROM level3_notice_invitation where author=%s and NI_Id=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[1]



    except:
        db.rollback()

    return json.dumps(dict(question=question))


## Save edited notice or invitation question for level 1 ##
@app.route('/save_edited_notice_invitation_question', methods=['POST'])
def save_edited_notice_invitation_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        question = request.form['question']
        author = session['username']
        #print author

        cursor = db.cursor()
        sql = """UPDATE level3_notice_invitation SET question=%s WHERE NI_Id=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question,qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('display_notice_invitation_questions'))


## Delete notice or invitation questions ##
@app.route('/delete_notice_invitation_questions/', methods=['GET'])
def delete_notice_invitation_questions():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """DELETE FROM level3_notice_invitation where NI_Id=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_notice_invitation_questions'))



## Level 3 Notice_Invitation Activity NEW##
@app.route('/level3_Notice_Invitation')
def level3_Notice_Invitation():

    cursor = db.cursor()
    sql = """SELECT * FROM level3_notice_invitation order by rand() limit 1"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        print result
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('level3_Notice_Invitation.html', data=result)


## Level 3 evaluate Notice_Invitation Activity NEW##
@app.route('/evaluate_level3_Notice_Invitation' , methods=['POST'])
def evaluate_level3_Notice_Invitation():

    question = request.form['question']
    answer = request.form['answer']
    type = request.form['type']

    struct_total = 0
    grammar_total = 0
    name = ''
    address = ''
    statusN = ''
    statusI = ''
    showtime = ''
    showdate = ''
    showvenue = ''

    #count senetences
    sent_count = 0
    sentences_qus= sent_tokenize(answer)

    for sentence_qus in sentences_qus:
        sent_count = sent_count+1

    if type == 'N':
        count1,name,address =notice.designation(answer, question)
        count2,statusN = notice.checkTypeWordCount(answer,question)
        count3,showtime,showdate,showvenue = notice.dateTimeVenue(answer)
        count4 = notice.includes(answer,question)
        if sent_count <= 2:
         struct_total = 0
        else :
         struct_total = count1+count2+count3+count4



    else:
        count1,name,address = invitation.designation(answer, question)
        count2,statusI = invitation.checkTypeWordCount(answer,question)
        count3,showtime,showdate,showvenue = invitation.dateTimeVenue(answer)
        count4 = invitation.includes(answer,question)

        if sent_count <= 2:
         struct_total = 0.0
        else :
         struct_total = count1+count2+count3+count4


    conv =Ansi2HTMLConverter()
    array=[]

    array=ginger.main(" ".join(answer.split()))
    original_text=conv.convert(array[0])
    fixed_text=conv.convert(array[1])
    wrong_count = array[2]


    if fixed_text=='Good English..!!' or wrong_count <=2 :
        grammar_total=grammar_total+2.5
    elif wrong_count >2 and wrong_count <= 4 :
        grammar_total=grammar_total+1.0
    elif sent_count <= 2 :
        grammar_total=grammar_total+0.0
    else:
        grammar_total=grammar_total+0.5

    print 'wrong',wrong_count
    print 'tot_grama',grammar_total
    print 'tot_struct',struct_total
    print 'ans = '," ".join(answer.split())

    total = struct_total+grammar_total
    print 'total = ',total
    return render_template('level3_N_I_grammar_spelling.html ' ,ans = answer, qus = question ,tot= total, struc_tot = struct_total ,grammar_tot=grammar_total,post = name , add = address ,statN = statusN, statI = statusI , date = showdate , time = showtime , venue = showvenue, original = original_text, fixed = fixed_text  )

@app.route('/structure_evaluation',methods=['POST'] )
def structure_evaluation():

    answer = request.form['answer']
    question = request.form['question']
    struct_total = request.form['total']
    grammar_total = request.form['grammar_total']
    total_cal = request.form['total_val']
    name = request.form['name']
    address = request.form['address']
    statusN = request.form['statusN']
    statusI = request.form['statusI']
    showdate = request.form['showdate']
    showtime = request.form['showtime']
    showvenue = request.form['showvenue']


    return render_template('level3_Notice_Invitation_evaluation.html',ans = answer, qus = question , total = total_cal,tot = struct_total ,gramm_tot = grammar_total, post = name , add = address ,statN = statusN, statI = statusI , date = showdate , time = showtime , venue = showvenue )

# ------------------------ Level 3 - Notice/Invitation ----------------------------------------------- #


#--------------------------------Grammar-------------------------
#Display Add grammar question
@app.route('/add_grammar_questions')
def add_grammar_questions():
    return render_template('add_grammar_questions.html')


# Add grammar questions
@app.route('/save_grammar', methods=['POST'])
def save_grammar():
    question1 = request.form['txtQuestion1']
    question2 = request.form['txtQuestion2']
    question3 = request.form['txtQuestion3']
    type1 = request.form['type1']
    type2 = request.form['type2']
    type3 = request.form['type3']
    author = session['username']

    question1_exist = False
    question2_exist = False
    question3_exist = False

    cursor = db.cursor()
    sql = """SELECT * FROM level_3_grammar WHERE question=%s OR question=%s OR question=%s"""

    try:
        # Execute the SQL command
        cursor.execute(sql, [question1, question2, question3])
        result = cursor.fetchall()

        if result:
            for row in result:
                if row[1] == question1:
                    question1_exist = True
                elif row[1] == question2:
                    question2_exist = True
                elif row[1] == question3:
                    question3_exist = True

            alert(text='Questions Already exists !', title='English Buddy', button='OK')
            errors = {'question1': question1, 'question2': question2, 'question3': question3, 'type1': type1,
                      'type2': type2, 'type3': type3, 'question1Status': question1_exist,
                      'question2Status': question2_exist, 'question3Status': question3_exist}

            return render_template('add_grammar_questions.html', errors=errors)
            #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    rows = []
    if question1 != '' and type1 != '':
        rows.append((question1, type1, author))
    if question2 != '' and type2 != '':
        rows.append((question2, type2, author))
    if question3 != '' and type3 != '':
        rows.append((question3, type3, author))

    cursor = db.cursor()
    sql = """INSERT INTO level_3_grammar (question,type,author) VALUES(%s,%s,%s)"""

    try:
        # Execute the SQL command
        cursor.executemany(sql, rows)
        # Commit your changes in the database
        db.commit()
        #flash('Question successfully added !')
        alert(text='Questions Added Successfully !', title='English Buddy', button='OK')
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('add_grammar_questions'))


#---------------update grammar question------

#--- View all grammar questions-----
@app.route('/Update_grammar_questions')
def Update_grammar_questions():
    cursor = db.cursor()

    sql = """SELECT qno,question,type FROM level_3_grammar where author=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()
    return render_template('Update_grammar_questions.html', data=query)


## Edit grammar question ##
@app.route('/edit_grammar', methods=['GET', 'POST'])
def edit_grammar():
    qno = request.args['qno']

    cursor = db.cursor()
    sql = """SELECT * FROM level_3_grammar where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [qno])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            question = row[1]
            type = row[2]

    except:
        db.rollback()

    return json.dumps(dict(question=question, type=type))


## Save updated grammar question data in the database ##
@app.route('/save_edited_grammar', methods=['POST'])
def save_edited_grammar():
    qno = request.form['qno']
    question = request.form['question']
    type = request.form['type']

    cursor = db.cursor()
    sql = """UPDATE level_3_grammar SET question=%s,type=%s WHERE qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [question, type, qno])
        db.commit()
        # fetch a single row using fetchone() method.
    except:
        db.rollback()

    return redirect(url_for('Update_grammar_questions'))


## Delete grammar question ##
@app.route('/delete_grammar/', methods=['GET'])
def delete_grammar():
    qno = request.args.get('qNo')

    cursor = db.cursor()
    sql = """delete from level_3_grammar where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [qno])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('Update_grammar_questions'))


#--------display grammar questions---------------------------

@app.route('/level3_grammar_activity')
def level3_grammar_activity():
    print 'heloo = ', Present_Tense()
    print Past_Tense()
    print Present_Continuous()
    print Past_Continuous()
    print Future_Tense()
    print Future_Continuous()

    return render_template('level3_grammar_activity.html', data_Present_Tense=Present_Tense(),
                           data_Past_Tense=Past_Tense(), data_Future_Tense=Future_Tense(),
                           data_Present_Continuous=Present_Continuous(), data_Past_Continuous=Past_Continuous(),
                           data_Future_Continuous=Future_Continuous())


def Present_Tense():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_3_grammar where type='Present Tense' order by rand() limit 2 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.

        query = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return query


# get past tense data
def Past_Tense():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_3_grammar where type='Past Tense' order by rand() limit 2 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.

        query = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return query


# get Future tense data
def Future_Tense():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_3_grammar where type='Future Tense' order by rand() limit 2 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.

        query = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return query


#get Present Continuous Tense data
def Present_Continuous():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_3_grammar where type='Present Continuous Tense' order by rand() limit 2 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.

        query = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return query


#get Past Continuous Tense data
def Past_Continuous():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_3_grammar where type='Past Continuous Tense' order by rand() limit 2 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.

        query = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return query


#get Future Continuous Tense data
def Future_Continuous():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_3_grammar where type='Future Continuous Tense' order by rand() limit 2 """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.

        query = cursor.fetchall()

    except:
        # Rollback in case there is any error
        db.rollback()
        request.form

    return query


#---------------------------Evaluate grammar question answers-----

@app.route('/evaluate_level3_grammar', methods=['POST'])
def evaluate_level3_grammar():
    count = 0
    data_set = []
    question1 = request.form['question1']
    question3 = request.form['question3']
    question4 = request.form['question4']
    answer1 = request.form['txtAnswerSet1']
    answer3 = request.form['txtAnswerSet3']
    answer4 = request.form['txtAnswerSet4']

    past_participle1 = ''
    past_participle2 = ''
    past_participle3 = ''
    past_participle4 = ''
    present_simple1=''
    present_simple2=''
    present_simple3=''
    present_simple4=''
    present_simple5=''
    present2 = ''
    present3 = ''
    present4 = ''
    past_plural_1 = ''
    past_plural_2 = ''
    past_singular_1 = ''
    past_singular_2 = ''
    Future_tense1 = ''
    Future_tense2 = ''
    Future_continous_1=''
    Future_continous_2=''
    present_participle1 = ''
    present_participle2 = ''
    present_participle3 = ''
    present_participle4 = ''
    present_participle5 = ''
    present_participle6 = ''


    text = nltk.word_tokenize(question1)
    tagged_sent = nltk.pos_tag(text)
    print tagged_sent

    print'#--------------------present tense----------------------------------------'
    if [word for word, pos in tagged_sent if pos == '#']:
        tok = [word for word, pos in tagged_sent if pos == '#']
        token = tok[0], '#'

        # to get the current position of '#'
        current_position = tagged_sent.index(token)
        # PRP Personal pronoun and RB Adverb
        pnoun= tagged_sent[current_position - 1][0]
        pnoun2=tagged_sent[current_position - 2][0]
        ptag=tagged_sent[current_position - 1][1]
        ptag2=tagged_sent[current_position - 2][1]
        print 'pnoun = ',pnoun

        if ptag == 'RB':
            print 'pnoun2 = ',pnoun2
            if pnoun2 == 'I' or pnoun2=='We' or pnoun2=='You' or pnoun2=='They' or ptag2=='NNS':
                verb = tagged_sent[current_position + 2][0]
                present_simple1 = en.verb.present(verb, person=1)

            elif pnoun2=='He' or pnoun2=='She' or pnoun2=='It' or ptag2=='NN' or ptag2=='NNP':
                print 'pnoun2 = ',pnoun2
                verb = tagged_sent[current_position + 2][0]
                # simple present tense
                present_simple2 = en.verb.present(verb, person=3)

        elif ptag =='NNP' or ptag=='NNS':
            if pnoun == 'I' or pnoun=='We' or pnoun=='You' or pnoun=='They' or ptag=='NNS':
                verb = tagged_sent[current_position + 2][0]
                present_simple1 = en.verb.present(verb, person=1)

            elif pnoun=='He' or pnoun=='She' or pnoun=='It' or ptag=='NN' or ptag=='NNP':
                verb = tagged_sent[current_position + 2][0]
                # simple present tense
                present_simple2 = en.verb.present(verb, person=3)

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        token = tok[0], 'VBP'

        current_position = tagged_sent.index(token)
        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]
        print 'pnoun = ',pnoun

        # Verb, non-2nd person singular
        if pnoun== 'You' or pnoun=='We' or pnoun=='They' or pnoun=='These' or pnoun=='Those' or ptag=='NNS' :
            verb = tagged_sent[current_position + 2][0]
            present_simple3 = en.verb.present(verb, person=2)
        # Verb, non-3rd person singular
        elif pnoun == 'He' or pnoun=='She' or pnoun=='It'or pnoun=='This' or pnoun=='That' or ptag=='NN' :
            verb = tagged_sent[current_position + 2][0]
            present_simple4= en.verb.present(verb, person=3)
        elif pnoun == 'I':
            verb=tagged_sent[current_position+2][0]
            print verb
            if verb=='be':
                present_t='am'
                present_simple5 =present_t
            else:
                present_t=en.verb.present(verb)
                present_simple5 =present_t

        if present_simple1 == answer1:
            count = count + 1
            print 'Correct present1'
        elif present_simple2 == answer1:
            count = count + 1
            print 'Correct present2'
        elif present_simple3 == answer1:
            count = count + 1
            print 'Correct present3'
        elif present_simple4 == answer1:
            count = count + 1
            print 'Correct present4'
        elif present_simple5 == answer1:
            count = count + 1
            print 'Correct present5'
        else:
            print 'Wrong presentx'

    else:
        print 'Wrong Answer'

    print '# --------------past tense-----------------------'
    question2 = request.form['question2']
    answer2 = request.form['txtAnswerSet2']

    text = nltk.word_tokenize(question2)
    tagged_sent = nltk.pos_tag(text)
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == '#']:
        tok = [word for word, pos in tagged_sent if pos == '#']
        token = tok[0], '#'

        # to get the current position of '#'
        current_position = tagged_sent.index(token)

        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]
        print 'pnoun = ',pnoun

        #NN-Noun, singular or mass,NNP-Proper noun, singular
        if pnoun == 'I' or pnoun=='He' or pnoun=='he' or pnoun=='She' or pnoun=='she' or pnoun=='It' or pnoun=='it' or ptag=='NNP' or ptag=='NN':
            verb = tagged_sent[current_position + 2][0]
            past_singular_1 = en.verb.past(verb, person=3)
        #RB-Adverb,NNS-Plural,Verb, 3rd person singular present
        elif pnoun=='We' or pnoun=='we' or pnoun=='You' or pnoun=='you' or pnoun=='They' or pnoun=='they'or pnoun=='Those' or ptag=='NNS' or ptag== 'VBZ'or ptag=='RB':
            verb = tagged_sent[current_position + 2][0]
            past_plural_1 = en.verb.past(verb, person=2)

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        token = tok[0], 'VBP'

        current_position = tagged_sent.index(token)
        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]

        if pnoun=='We' or pnoun=='we' or pnoun=='You' or pnoun=='you' or pnoun=='They' or pnoun=='they'or pnoun=='Those' or ptag=='NNS' or ptag== 'VBZ':
            verb = tagged_sent[current_position + 2][0]
            past_plural_2 = en.verb.past(verb, person=2)
        # Verb, non-3rd past singular
        elif pnoun == 'I' or pnoun=='He' or pnoun=='he' or pnoun=='She' or pnoun=='she' or pnoun=='It' or pnoun=='it' or ptag=='NNP' or ptag=='NN' or ptag=='RB':
            verb = tagged_sent[current_position + 2][0]
            past_singular_2 = en.verb.past(verb, person=3)


    if past_singular_1 == answer2:
        count = count + 1
        print 'Correct1'
    elif past_singular_2 == answer2:
        count = count + 1
        print 'Correct 2'
    elif past_plural_1 == answer2:
        count = count + 1
        print 'Correct '
    elif past_plural_2 == answer2:
        count = count + 1
        print 'Correct '
    else:
        print 'Wrong presentx'


    print '# ----------Present Continuous--------------------------------------'

    text = nltk.word_tokenize(question3)
    tagged_sent = nltk.pos_tag(text)
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == '#']:
        tok = [word for word, pos in tagged_sent if pos == '#']
        token = tok[0], '#'

        # to get the current position of 'VBP'
        current_position = tagged_sent.index(token)

        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]
        print 'pnoun = ',pnoun

        if pnoun == 'She' or pnoun=='she' or pnoun=='He' or pnoun=='he' or pnoun=='It' or pnoun=='it' or ptag=='NN' or ptag=='NNP':
            verb = tagged_sent[current_position + 2][0]
            # present continuous tense
            present1 = en.verb.present_participle(verb)
            present_participle1 = 'is ' + present1

        elif pnoun == 'We' or pnoun=='we' or pnoun=='You' or pnoun=='you' or pnoun=='They' or pnoun=='they' or ptag=='NNS':
            verb = tagged_sent[current_position + 2][0]
            # present continuous tense
            present2 = en.verb.present_participle(verb)
            present_participle2 = 'are ' + present2

        elif pnoun == 'I':
            verb = tagged_sent[current_position + 2][0]
            # present continuous tense
            present3 = en.verb.present_participle(verb)
            present_participle3 = 'am ' + present3
        else:
            print 'wrong'

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        token = tok[0], 'VBP'
        # to get the current position of 'VBP'
        current_position = tagged_sent.index(token)
        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]
        print 'pnoun = ',pnoun

        if pnoun == 'She' or pnoun=='she' or pnoun=='He' or pnoun=='he' or pnoun=='It' or pnoun=='it' or ptag=='NN' or ptag=='NNP':
            verb = tagged_sent[current_position + 2][0]
            # present continuous tense
            present4 = en.verb.present_participle(verb)
            present_participle4 = 'is ' + present4

        elif pnoun=='We' or pnoun=='we' or pnoun=='You' or pnoun=='you' or pnoun=='They' or pnoun=='they' or ptag=='NNS':
            verb = tagged_sent[current_position + 2][0]
            # present continuous tense
            present5 = en.verb.present_participle(verb)
            present_participle5 = 'are ' + present5

        elif pnoun=='I':
            verb = tagged_sent[current_position + 2][0]
            # present continuous tense
            present6 = en.verb.present_participle(verb)
            present_participle6 = 'am ' + present6
        else:
            print 'wrong'
    else:
        print 'Wrong Present Continuous'

    if present_participle1 == answer3:
        count = count + 1
        print 'Correct1'
    elif present_participle2 == answer3:
        count = count + 1
        print 'Correct 2'
    elif present_participle3 == answer3:
        count = count + 1
        print 'Correct '
    elif present_participle4 == answer3:
        count = count + 1
        print 'Correct '
    elif present_participle5 == answer3:
        count = count + 1
        print 'Correct '
    elif present_participle6 == answer3:
        count = count + 1
        print 'Correct '
    else:
        print 'Wrong presentx'

    print'# -----------------------------Past continuous tense------------------------------------------------------'

    text = nltk.word_tokenize(question4)
    tagged_sent = nltk.pos_tag(text)
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == '#']:
        tok = [word for word, pos in tagged_sent if pos == '#']
        token = tok[0], '#'

        # to get the current position of 'VBP'
        current_position = tagged_sent.index(token)

        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]
        print 'pnoun = ',pnoun

        if pnoun == 'She' or pnoun=='she' or pnoun=='He' or pnoun=='he' or pnoun=='It' or pnoun=='I' or pnoun=='it' or ptag=='NN' or ptag=='NNP':
            verb = tagged_sent[current_position + 2][0]
            past = en.verb.present_participle(verb)
            past_participle1 = 'was ' + past
            print 'x'

        elif pnoun == 'We' or pnoun=='we' or pnoun=='You' or pnoun=='you' or pnoun=='They' or pnoun=='they' or ptag=='NNS':
            verb = tagged_sent[current_position + 2][0]
            # past continuous tense
            past = en.verb.present_participle(verb)
            past_participle2 = 'were ' + past
            print 'y'
        else:
            print 'error'

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        token = tok[0], 'VBP'

        # to get the current position of 'VBP'
        current_position = tagged_sent.index(token)

        pnoun= tagged_sent[current_position - 1][0]
        ptag=tagged_sent[current_position - 1][1]

        if  pnoun == 'She' or pnoun=='I' or pnoun=='she' or pnoun=='He' or pnoun=='he' or pnoun=='It' or pnoun=='it' or ptag=='NN' or ptag=='NNP':
            verb = tagged_sent[current_position + 2][0]
            past = en.verb.present_participle(verb)
            past_participle3 = 'was ' + past
            print 'z'

        elif pnoun == 'We' or pnoun=='we' or pnoun=='You' or pnoun=='you' or pnoun=='They' or pnoun=='they' or ptag=='NNS':
            verb = tagged_sent[current_position + 2][0]
            past = en.verb.present_participle(verb)
            past_participle4 = 'were ' + past
            print 'zz'

    else:
        print 'Wrong past Continuous'

    if past_participle1 == answer4:
        count = count + 1
        print 'Correct1'
    elif past_participle2 == answer4:
        count = count + 1
        print 'Correct 2'
    elif past_participle3 == answer4:
        count = count + 1
        print 'Correct '
    elif past_participle4 == answer4:
        count = count + 1
        print 'Correct '
    else:
        print 'Wrong presentx'

    print'#--------------Future tense---------------------------------------------------#'

    question5 = request.form['question5']
    answer5 = request.form['txtAnswerSet5']

    text = nltk.word_tokenize(question5)
    tagged_sent = nltk.pos_tag(text)
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == '#']:
        tok = [word for word, pos in tagged_sent if pos == '#']
        token = tok[0], '#'

        # to get the current position of '#'
        current_position = tagged_sent.index(token)

        verb = tagged_sent[current_position + 2][0]
        Future1 = en.verb.infinitive(verb)
        Future_tense1 = 'will ' + Future1


    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        token = tok[0], 'VBP'

            # to get the current position of '#'
        current_position = tagged_sent.index(token)

        verb = tagged_sent[current_position + 2][0]

        Future2 = en.verb.infinitive(verb)
        Future_tense2 = 'will ' + Future2

    if Future_tense1 == answer5:
        count = count + 1
        print 'Correct1'
    elif Future_tense2 == answer5:
        count = count + 1
        print 'Correct 2'
    else:
        print 'Wrong presentx'

    print'#-----------------------Future Continuous Tense-------------------------'

    question6 = request.form['question6']
    answer6 = request.form['txtAnswerSet6']

    text = nltk.word_tokenize(question6)
    tagged_sent = nltk.pos_tag(text)
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == '#']:
        tok = [word for word, pos in tagged_sent if pos == '#']
        token = tok[0], '#'

        # to get the current position of '#'
        current_position = tagged_sent.index(token)

        verb = tagged_sent[current_position + 2][0]
        Future_c = en.verb.present_participle(verb)
        Future_continous_1 = 'will be ' + Future_c

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        token = tok[0], 'VBP'

        # to get the current position of '#'
        current_position = tagged_sent.index(token)

        verb = tagged_sent[current_position + 2][0]
        Future4 = en.verb.present_participle(verb)
        Future_continous_2 = 'will be ' + Future4

        print 'count:',count
        #return 'sucess'
    if Future_continous_1 == answer6:
        count = count + 1
        print 'Correct1'
    elif Future_continous_2 == answer6:
        count = count + 1
        print 'Correct 2'
    else:
        print 'Wrong presentx'

    data_set = {'question1':question1 ,'question2':question2,'question3':question3,'question4':question4,'question5':question5,'question6':question6,
                'answer1': answer1,'answer2': answer2,'answer3': answer3,'answer4': answer4,'answer5': answer5,'answer6': answer6,
                'past_singular_1': past_singular_1,'past_plural_1': past_plural_1,'past_plural_2':past_plural_2,'past_singular_2': past_singular_2,
                'present_participle1':present_participle1,'present_participle2':present_participle2,'present_participle3':present_participle3,
                'present_participle4':present_participle4,'present_participle5':present_participle5,'present_participle6':present_participle6,
                'Future_continous_1':Future_continous_1,'Future_continous_2':Future_continous_2,'Future_tense1':Future_tense1,'Future_tense2':Future_tense2,
                'past_participle1':past_participle1,'past_participle2':past_participle2,'past_participle3':past_participle3,'past_participle4':past_participle4,
                'count':count,'present_simple1':present_simple1,'present_simple2':present_simple2,'present_simple3':present_simple3,'present_simple4':present_simple4,'present_simple5':present_simple5}


    return render_template('level3_grammar_evaluate.html', data_set=data_set)
    #return redirect(url_for('level3_grammar_activity'))
#--------------------------------Grammar-------------------------

## ------------------------------------- Level 4 ----------------------------------------------- ##


# ----------------------- Level 4 - Dialog ----------------------------------------------------------

## View Add Dialog Questions for level 4 ##
@app.route('/level4_add_dialog_questions')
def level4_add_dialog_questions():
    return render_template('level4_add_dialog_questions.html')


## Add dialog question for level 4 ##
@app.route('/level4_save_dialog_question', methods=['POST'])
def level4_save_dialog_question():
    if request.method == 'POST':

        question1 = request.form['question1']
        answer1 = request.form['answer1']
        question2 = request.form['question2']
        answer2 = request.form['answer2']
        question3 = request.form['question3']
        answer3 = request.form['answer3']
        question4 = request.form['question4']
        answer4 = request.form['answer4']
        question5 = request.form['question5']
        answer5 = request.form['answer5']
        question6 = request.form['question6']
        author = session['username']

        cursor = db.cursor()
        sql = """INSERT INTO level4_dialogs (q1,a1,q2,a2,q3,a3,q4,a4,q5,a5,q6,author) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, answer1, question2, answer2, question3, answer3, question4, answer4, question5, answer5, question6, author])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    alert(text='Question Added Successfully !', title='English Buddy', button='OK')
    return redirect(url_for('level4_add_dialog_questions'))


## Edit level 4 dialog questions ##
@app.route('/edit_level4_dialog', methods=['GET', 'POST'])
def edit_level4_dialog():
    qNo = request.args.get('qNo')

    cursor = db.cursor()
    sql = """SELECT * FROM level4_dialogs WHERE author=%s and qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()

        for row in result:
            q1 = row[1]
            a1 = row[2]
            q2 = row[3]
            a2 = row[4]
            q3 = row[5]
            a3 = row[6]
            q4 = row[7]
            a4 = row[8]
            q5 = row[9]
            a5 = row[10]
            q6 = row[11]
    except:
        db.rollback()

    return json.dumps(dict(q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, a1=a1, a2=a2, a3=a3, a4=a4, a5=a5))


## Save edited level4 dialog question ##
@app.route('/save_edited_level4_dialog_question', methods=['POST'])
def save_edited_level4_dialog_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        question1 = request.form['question1']
        answer1 = request.form['answer1']
        question2 = request.form['question2']
        answer2 = request.form['answer2']
        question3 = request.form['question3']
        answer3 = request.form['answer3']
        question4 = request.form['question4']
        answer4 = request.form['answer4']
        question5 = request.form['question5']
        answer5 = request.form['answer5']
        question6 = request.form['question6']

        cursor = db.cursor()
        sql = """UPDATE level4_dialogs SET q1=%s,q2=%s,q3=%s,q4=%s,q5=%s,q6=%s,a1=%s,a2=%s,a3=%s,a4=%s,a5=%s WHERE qNo=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3, question4, question5, question6, answer1, answer2, answer3, answer4, answer5, qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    url='/display_dialog_questions/?level=level4'

    return redirect(url)


## Delete dialog questions ##
@app.route('/delete_level4_dialog_questions/', methods=['GET'])
def delete_level4_dialog_questions():
    qNo = request.args.get('qNo')

    cursor = db.cursor()
    sql = """DELETE FROM level4_dialogs where qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    url='/display_dialog_questions/?level=level4'

    return redirect(url)


## Level 4 Dialog Activity ##
@app.route('/level4_dialogs_activity')
def level4_dialogs_activity():
    cursor = db.cursor()
    sql = """SELECT * FROM level4_dialogs order by rand() limit 1"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('level4_dialogs_activity.html', data=result)


## Level 4 Dialog Evaluate Answers ##
@app.route('/evaluate_level4_dialog_activity', methods=['POST'])
def evaluate_level4_dialog_activity():

    qNo=request.form['qNo']
    question_1=request.form['question1'].strip()
    question_2=request.form['question2'].strip()
    question_3=request.form['question3'].strip()
    question_4=request.form['question4'].strip()
    question_5=request.form['question5'].strip()

    if request.form['question6'] != None:
        question_6=request.form['question6'].strip()

    answer_1=request.form['one'].strip()
    answer_2=request.form['two'].strip()
    answer_3=request.form['three'].strip()
    answer_4=request.form['four'].strip()
    answer_5=request.form['five'].strip()


    # for keyword in keywordClass.test(question_1):
    #     if keyword in answer_1:
    #         count=count+1
    #         print(count)
    # print(count)
    #
    # for keyword in en.content.keywords(question_1):
    #     if keyword in answer_1:
    #         count=count+1
    #         print count


    # # Answer 1 evaluation
    # answer1_content_marks = 0
    # question1_key_words = en.content.keywords(question_1)
    # # answer1_key_words = en.content.keywords(answer_1)
    # answer1_key_words = answer_1.split(" ")
    #
    # print question1_key_words
    # print answer1_key_words
    #
    # for word in question1_key_words:
    #     for answer in answer1_key_words:
    #         if (answer.upper().find(word[1])!=-1) or (answer.lower().find(word[1])!=-1):
    #             answer1_content_marks=answer1_content_marks+1
    # print "Answer 1 Content Marks : "+str(answer1_content_marks)
    #
    #
    # # Answer 2 evaluation
    # answer2_content_marks = 0
    # question2_key_words = en.content.keywords(question_2)
    # answer2_key_words = answer_2.split(" ")
    #
    # print question2_key_words
    # print answer2_key_words
    #
    # for word in question2_key_words:
    #     for answer in answer2_key_words:
    #         if (answer.upper().find(word[1])!=-1) or (answer.lower().find(word[1])!=-1):
    #             answer2_content_marks=answer2_content_marks+1
    # print "Answer 2 Content Marks : "+str(answer2_content_marks)
    #
    #
    # # Answer 3 evaluation
    # answer3_content_marks = 0
    # question3_key_words = en.content.keywords(question_3)
    # answer3_key_words = answer_3.split(" ")
    #
    # print question3_key_words
    # print answer3_key_words
    #
    # for word in question3_key_words:
    #     for answer in answer3_key_words:
    #         if (answer.upper().find(word[1])!=-1) or (answer.lower().find(word[1])!=-1):
    #             answer3_content_marks=answer3_content_marks+1
    # print "Answer 3 Content Marks : "+str(answer3_content_marks)
    #
    #
    # # Answer 4 evaluation
    # answer4_content_marks = 0
    # question4_key_words = en.content.keywords(question_4)
    # answer4_key_words = answer_4.split(" ")
    #
    # print question4_key_words
    # print answer4_key_words
    #
    # for word in question4_key_words:
    #     for answer in answer4_key_words:
    #         if (answer.upper().find(word[1])!=-1) or (answer.lower().find(word[1])!=-1):
    #             answer4_content_marks=answer4_content_marks+1
    # print "Answer 4 Content Marks : "+str(answer4_content_marks)
    #
    #
    # # Answer 5 evaluation
    # answer5_content_marks = 0
    # question5_key_words = en.content.keywords(question_5)
    # answer5_key_words = answer_5.split(" ")
    #
    # print question5_key_words
    # print answer5_key_words
    #
    # for word in question5_key_words:
    #     for answer in answer5_key_words:
    #         if (answer.upper().find(word[1])!=-1) or (answer.lower().find(word[1])!=-1):
    #             answer5_content_marks=answer5_content_marks+1
    # print "Answer 5 Content Marks : "+str(answer5_content_marks)


    # return "Answer 1 Content Marks : " + str(answer1_content_marks) + " | " + "Answer 2 Content Marks : " + str(
    #     answer2_content_marks) + " | " + "Answer 3 Content Marks : " + str(
    #     answer3_content_marks) + " | " + "Answer 4 Content Marks : " + str(answer4_content_marks)+ " | " +"Answer 5 Content Marks : "+str(answer5_content_marks)

    a1_status = 0
    a2_status = 0
    a3_status = 0
    a4_status = 0
    a5_status = 0
    marks = 0

    a1_wrong_grammar = ''
    a2_wrong_grammar = ''
    a3_wrong_grammar = ''
    a4_wrong_grammar = ''
    a5_wrong_grammar = ''
    a1_corrected_grammar = ''
    a2_corrected_grammar = ''
    a3_corrected_grammar = ''
    a4_corrected_grammar = ''
    a5_corrected_grammar = ''


    conv = Ansi2HTMLConverter()

    if answer_1 != '':
        # Content Checking
        a1_status = DialogClass.check(question_1, answer_1)

        if a1_status == 0:
            a1_status = DialogClass.check(answer_1, question_2)

        # Tence Checking
        # if TenseClass.check_tense(question_1,answer_1):

        # Grammar Checking
        grammar_status = ginger.main(answer_1)
        if grammar_status[1] =="Good English":
            if a1_status != 0:
                marks = marks + 2
                a1_wrong_grammar = 'none'
                a1_corrected_grammar = 'none'
            else:
                a1_wrong_grammar = conv.convert(grammar_status[0])
                a1_corrected_grammar = conv.convert(grammar_status[1])

    if answer_2 != '':
        a2_status = DialogClass.check(question_2, answer_2)

        if a2_status == 0:
            a2_status = DialogClass.check(answer_2, question_3)

        grammar_status = ginger.main(answer_2)
        if grammar_status[1] =="Good English":
            if a2_status != 0:
                marks = marks + 2
            a2_wrong_grammar = 'none'
            a2_corrected_grammar = 'none'
        else:
            a2_wrong_grammar = conv.convert(grammar_status[0])
            a2_corrected_grammar = conv.convert(grammar_status[1])

    if answer_3 != '':
        a3_status = DialogClass.check(question_3, answer_3)

        if a3_status == 0:
            a3_status = DialogClass.check(answer_3, question_4)

        grammar_status = ginger.main(answer_3)
        if grammar_status[1] =="Good English":
            if a3_status != 0:
                marks = marks + 2
            a3_wrong_grammar = 'none'
            a3_corrected_grammar = 'none'
        else:
            a3_wrong_grammar = conv.convert(grammar_status[0])
            a3_corrected_grammar = conv.convert(grammar_status[1])

    if answer_4 != '':
        a4_status = DialogClass.check(question_4, answer_4)

        if a4_status == 0:
            a4_status = DialogClass.check(answer_4, question_5)

        grammar_status = ginger.main(answer_4)
        if grammar_status[1] =="Good English":
            if a4_status != 0:
                marks = marks + 2
            a4_wrong_grammar = 'none'
            a4_corrected_grammar = 'none'
        else:
            a4_wrong_grammar = conv.convert(grammar_status[0])
            a4_corrected_grammar = conv.convert(grammar_status[1])

    if answer_5 != '':
        a5_status = DialogClass.check(question_5, answer_5)

        if a5_status == 0 and question_6 != '':
            a5_status = DialogClass.check(answer_5, question_6)

        grammar_status = ginger.main(answer_5)
        if grammar_status[1] =="Good English":
            if a5_status != 0:
                marks = marks + 2
            a5_wrong_grammar = 'none'
            a5_corrected_grammar = 'none'
        else:
            a5_wrong_grammar = conv.convert(grammar_status[0])
            a5_corrected_grammar = conv.convert(grammar_status[1])


    data_array = {'pa1': answer_1, 'pa2': answer_2, 'pa3': answer_3, 'pa4': answer_4, 'pa5': answer_5,
                  'a1_status': a1_status, 'a2_status': a2_status, 'a3_status': a3_status,
                  'a4_status': a4_status, 'a5_status': a5_status, 'marks': marks,
                  'a1_wrong_grammar':a1_wrong_grammar, 'a1_corrected_grammar':a1_corrected_grammar,
                  'a2_wrong_grammar':a2_wrong_grammar, 'a2_corrected_grammar':a2_corrected_grammar,
                  'a3_wrong_grammar':a3_wrong_grammar, 'a3_corrected_grammar':a3_corrected_grammar,
                  'a4_wrong_grammar':a4_wrong_grammar, 'a4_corrected_grammar':a4_corrected_grammar,
                  'a5_wrong_grammar':a5_wrong_grammar, 'a5_corrected_grammar':a5_corrected_grammar}

    cursor = db.cursor()
    sql = """SELECT * FROM level4_dialogs WHERE qNo=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql,[qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()


    return render_template('level4_dialogs_activity.html', answer_data=data_array,  data=result)


# ------------------------ Level 4 - Note ----------------------------------------------- #
#Darani
## Note Questions for level 1 ##
@app.route('/add_note_questions')
def add_note_questions():
    return render_template('add_note_questions.html')


## Add note question for level 1 ##
@app.route('/save_note_questions', methods=['POST'])
def save_note_questions():
    if request.method == 'POST':

        question1 = request.form['question_1']
        question2 = request.form['question_2']
        question3 = request.form['question_3']
        author = session['username']

        question1_exist=False
        question2_exist=False
        question3_exist=False

        cursor = db.cursor()
        sql = """SELECT * FROM level4_note WHERE question=%s OR question=%s OR question=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question1, question2, question3])
            result = cursor.fetchall()

            if result:
                for row in result:
                    if row[1]==question1:
                        question1_exist=True
                    elif row[1]==question2:
                        question2_exist=True
                    elif row[1]==question3:
                        question3_exist=True

                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'question1':question1, 'question2':question2, 'question3':question3, 'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('add_note_questions.html', errors=errors)
            #flash('Question successfully added !')

        except:
            # Rollback in case there is any error
            db.rollback()

        rows = []
        if question1 != '' :
            rows.append((question1, author))
        if question2 != '' :
            rows.append((question2, author))
        if question3 != '' :
            rows.append((question3, author))

        print rows
        cursor = db.cursor()
        sql = """INSERT INTO level4_note (question,author) VALUES(%s,%s)"""

        try:
            # Execute the SQL command
            print cursor.executemany(sql, rows)

            # Commit your changes in the database
            db.commit()
            #flash('Question successfully added !')
            alert(text='Question Added Successfully !', title='English Buddy', button='OK')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('add_note_questions'))


## Display all note questions ##
@app.route('/display_note_questions')
def display_note_questions():
    cursor = db.cursor()
    sql = """SELECT * FROM level4_note where author=%s """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_note_questions.html', data=result)


## Edit note questions ##
@app.route('/edit_note', methods=['GET', 'POST'])
def edit_note():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """SELECT * FROM level4_note where author=%s and noteId=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], qNo])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        for row in result:
            question = row[1]


    except:
        db.rollback()

    return json.dumps(dict(question=question))


## Save edited note question for level 1 ##
@app.route('/save_edited_note_question', methods=['POST'])
def save_edited_note_question():
    if request.method == 'POST':

        qNo = request.form['qNo']
        question = request.form['question']
        author = session['username']
        #print author

        cursor = db.cursor()
        sql = """UPDATE level4_note SET question=%s WHERE noteId=%s"""

        try:
            # Execute the SQL command
            cursor.execute(sql, [question,qNo])
            # Commit your changes in the database
            db.commit()

            #flash('Question successfully added !')
        except:
            # Rollback in case there is any error
            db.rollback()

    return redirect(url_for('display_note_questions'))


## Delete note questions ##
@app.route('/delete_note_questions/', methods=['GET'])
def delete_note_questions():
    qNo = request.args.get('qNo')
    cursor = db.cursor()
    sql = """DELETE FROM level4_note where noteId=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [qNo])
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_note_questions'))



## Level 3 note Activity NEW##
@app.route('/level4_Note')
def level4_Note():

    cursor = db.cursor()
    sql = """SELECT * FROM level4_note order by rand() limit 1"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('level4_Note.html', data=result)


## Level 3 evaluate note Activity NEW##
@app.route('/evaluate_level4_Note' , methods=['POST'])
def evaluate_level4_Note():

    answer = request.form['answer']
    question = request.form['question']

    struct_total = 0
    grammar_total =0
    status_write = ''
    status_receiver = ''
    status_your = ''

    sent_count = 0
    sentences_qus= sent_tokenize(answer)

    for sentence_qus in sentences_qus:
        sent_count = sent_count+1

    count1 = note.word_count(answer,question)
    count2,status_receiver = note.note_receiver(answer)
    count3,status_write,status_your = note.note_writer(answer)
    count4 = note.note_body(answer,question)


    if sent_count <= 2:
         struct_total = 0.0
    else :
         struct_total = count1+count2+count3+count4

    conv =Ansi2HTMLConverter()
    array=[]

    array=ginger.main(" ".join(answer.split()))
    original_text=conv.convert(array[0])
    fixed_text=conv.convert(array[1])
    wrong_count = array[2]


    if fixed_text=='Good English..!!' or wrong_count <=2 :
        grammar_total = 2.5
    elif wrong_count >2 and wrong_count <= 4 :
        grammar_total = 1.0
    elif sent_count <= 2 :
        grammar_total = 0.0
    else:
        grammar_total = 0.5

    print 'wrong',wrong_count
    print 'tot_grama',grammar_total
    print 'tot_struct',struct_total
    print 'ans = '," ".join(answer.split())

    total = struct_total+ grammar_total
    print 'total = ',total

    return render_template('level4_Note_grammar_spelling.html', ans = answer,qus = question,tot = total,struct_tot = struct_total,grammar_tot = grammar_total,stat_writer = status_write,stat_receiver = status_receiver,stat_your = status_your,original = original_text, fixed = fixed_text )


@app.route('/structure_evaluation_note',methods=['POST'] )
def structure_evaluation_note():

    answer = request.form['answer']
    question = request.form['question']
    struct_total = request.form['total']
    writer = request.form['writer']
    receiver = request.form['receiver']
    your = request.form['yours']
    grammar_total = request.form['grammar_total']
    total = request.form['total_val']

    return render_template('level4_Note_evaluation.html',ans = answer,qus = question,tot = total,gramm_tot = grammar_total,struct_tot = struct_total,stat_writer = writer,stat_receiver = receiver,stat_your = your )

# ------------------------ Level 4 - Note ----------------------------------------------- #

#-------------------------------CHAMIKA----------------------------------------------------------


#----------------level 4 Active Passive-CHAMIKA---------------

# Level 4 Active Passive
@app.route('/level4_active_passive')
def level4_active_passive():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_4_activepassive where type='Active Voice' order by rand() limit 3"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        query = cursor.fetchall()
    except:
        db.rollback()
        db.close()

    return render_template('level4_active_passive.html', data=query)


# Level 4 Passive Active
@app.route('/level4_passive_active')
def level4_passive_active():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level_4_activepassive where type='Passive Voice' order by rand() limit 3"""
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        query = cursor.fetchall()
    except:
        db.rollback()
        db.close()

    return render_template('level4_passive_active.html', data=query)


#Display Add active passive question
@app.route('/add_active_passive_questions')
def add_active_passive_questions():
    return render_template('add_active_passive_questions.html')


# Add active passive questions
@app.route('/save_active_passive', methods=['POST'])
def save_active_passive():
    question1 = request.form['txtQuestion1']
    question2 = request.form['txtQuestion2']
    question3 = request.form['txtQuestion3']
    type1 = request.form['type1']
    type2 = request.form['type2']
    type3 = request.form['type3']
    author = session['username']

    question1_exist = False
    question2_exist = False
    question3_exist = False

    cursor = db.cursor()
    sql = """SELECT * FROM level_4_activepassive WHERE question=%s OR question=%s OR question=%s"""

    try:
        # Execute the SQL command
        cursor.execute(sql, [question1, question2, question3])
        result = cursor.fetchall()

        if result:
            for row in result:
                if row[1] == question1:
                    question1_exist = True
                elif row[1] == question2:
                    question2_exist = True
                elif row[1] == question3:
                    question3_exist = True

            alert(text='Questions Already exists !', title='English Buddy', button='OK')
            errors = {'question1': question1, 'question2': question2, 'question3': question3, 'type1': type1,
                      'type2': type2, 'type3': type3, 'question1Status': question1_exist,
                      'question2Status': question2_exist, 'question3Status': question3_exist}

            return render_template('add_active_passive_questions.html', errors=errors)
            #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    rows = []
    if question1 != '' and type1 != '':
        rows.append((question1, type1, author))
    if question2 != '' and type2 != '':
        rows.append((question2, type2, author))
    if question3 != '' and type3 != '':
        rows.append((question3, type3, author))

    cursor = db.cursor()
    sql = """INSERT INTO level_4_activepassive (question,type,author) VALUES(%s,%s,%s)"""

    try:
        # Execute the SQL command
        cursor.executemany(sql, rows)
        # Commit your changes in the database
        db.commit()
        #flash('Question successfully added !')
        alert(text='Questions Added Successfully !', title='English Buddy', button='OK')
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('add_active_passive_questions'))


#---------------update active passive question------

#--- View all active passive questions-----
@app.route('/Update_active_passive')
def Update_active_passive():
    cursor = db.cursor()

    sql = """SELECT qno,question,type FROM level_4_activepassive where author=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()
    return render_template('Update_active_passive.html', data=query)


## Edit active passive question ##
@app.route('/edit_active_passive', methods=['GET', 'POST'])
def edit_active_passive():
    qno = request.args['qno']

    cursor = db.cursor()
    sql = """SELECT * FROM level_4_activepassive where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [qno])
        # fetch a single row using fetchone() method.
        query = cursor.fetchall()
        for row in query:
            question = row[1]
            type = row[2]

    except:
        db.rollback()

    return json.dumps(dict(question=question, type=type))


## Save active passive question data in the database ##
@app.route('/save_edited_active_passive', methods=['POST'])
def save_edited_active_passive():
    qno = request.form['qno']
    question = request.form['question']
    type = request.form['type']

    cursor = db.cursor()
    sql = """UPDATE level_4_activepassive SET question=%s,type=%s WHERE qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [question, type, qno])
        db.commit()
        # fetch a single row using fetchone() method.
    except:
        db.rollback()

    return redirect(url_for('Update_active_passive'))


## Delete Active passive question ##
@app.route('/delete_active_passive/', methods=['GET'])
def delete_active_passive():
    qno = request.args.get('qNo')

    cursor = db.cursor()
    sql = """delete from level_4_activepassive where qno=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [qno])
        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('Update_active_passive'))

#----------------------Evaluate active passive--------------------------
# This is the fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
    ])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is the semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP"] = "NNP"
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
cfg["AT+NN"] = "NNT"
cfg["AT+NNS"] = "NNS"
cfg["AT+NNP"] = "NP"
#############################################################################

class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into single words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN" or t[1] == "NNS" or t[1] == "NP" or t[1] == "NNT":
                matches.append(t[0])
        return matches


@app.route('/evaluate_level4_active_passive', methods=['POST'])
def evaluate_level4_active_passive():
    sentence1 = request.form['question1']
    answer1 = request.form['answer1']
    answer2 = request.form['answer2']
    answer3 = request.form['answer3']
    sentence2 = request.form['question2']
    sentence3 = request.form['question3']
    count=0
    p1=''
    p2=''
    p3=''
    p4=''
    p5=''
    p6=''
    p7=''
    p8=''
    s1=''
    s2=''
    s3=''
    s4=''
    s5=''
    s6=''
    s7=''
    s8=''
    t1=''
    t2=''
    t3=''
    t4=''
    t5=''
    t6=''
    t7=''
    t8=''

    print '---------------------------------1------------------------------------'
    text = nltk.word_tokenize(sentence1)
    tagged_sent = nltk.pos_tag(text)
    print 'tagged_sent:',tagged_sent

    np_extractor = NPExtractor(sentence1)
    result = np_extractor.extract()

    print "result:"
    print result
    sub = result[0]
    obj = result[-1]
    object = obj.capitalize()

    if [word for word, pos in tagged_sent if pos == 'NNP']:
        subject = sub.capitalize()
    else:
        subject = sub.lower()

    print "subject:" + subject
    print "object:" + object
    result_sent = nltk.pos_tag(result)
    print 'result_sent:',result_sent

    if [word for word, pos in tagged_sent if pos == 'VBD']:
        tok = [word for word, pos in tagged_sent if pos == 'VBD']
        verb = ''.join(tok)
        past_participle = en.verb.past_participle(verb)

        if [word for word, pos in result_sent if pos == 'NNP' or pos =='NNI' or pos =='NNT' or pos =='NP']:

            print result_sent[-1][1]
            if result_sent[-1][1] == 'NNS':
                p1 = object + " were " + past_participle + " by " + subject + "."
                print 'p1: ' + p1
            else:
                p2 = object + " was " + past_participle + " by " + subject + "."
                print 'p2: ' + p2

        elif [word for word, pos in result_sent if pos == 'NNS']:

            print result_sent[-1][1]
            if result_sent[-1][1] == 'NNS':
                p3 = object + " were " + past_participle + " by " + subject + "."
                print 'p3: ' + p3
            else:
                p4 = object + " was " + past_participle + " by " + subject + "."
                print 'p4: ' + p4
        else:
            print'wrong'

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        verb = ''.join(tok)
        past_participle = en.verb.past_participle(verb)

        if [word for word, pos in result_sent if pos == 'NNP' or 'NNI' or 'NNT' or 'NP']:

            print result_sent[-1][1]
            if result_sent[-1][1] == 'NNS':
                p5 = object + " were " + past_participle + " by " + subject + "."
                print 'p5: ' + p5
            else:
                p6 = object + " was " + past_participle + " by " + subject + "."
                print 'p6 :' + p6


        elif [word for word, pos in result_sent if pos == 'NNS']:

            print result_sent[-1][1]
            if result_sent[-1][1] == 'NNS':
                p7 = object + " were " + past_participle + " by " + subject + "."
                print 'p7 :' + p7
            else:
                p8 = object + " was " + past_participle + " by " + subject + "."
                print 'p8 :' + p8
    else:
        print 'Wrongs'


    if answer1==p1:
        count=count+1
        print 'correct1'
    elif answer1==p2:
        count=count+1
        print 'correct2'
    elif answer1==p3:
        count=count+1
        print 'correct3'
    elif answer1==p4:
        count=count+1
        print 'correct4'
    elif answer1==p5:
        count=count+1
        print 'correct5'
    elif answer1==p6:
        count=count+1
        print 'correct6'
    elif answer1==p7:
        count=count+1
        print 'correct7'
    elif answer1==p8:
        count=count+1
        print 'correct8'

    print '--------------------------------------------2---------------------------'

    text = nltk.word_tokenize(sentence2)
    tagged_sent = nltk.pos_tag(text)
    print 'tagged_sent:',tagged_sent

    np_extractor = NPExtractor(sentence2)
    result3 = np_extractor.extract()

    print "result3:"
    print result3
    sub = result3[0]
    obj = result3[-1]
    object2 = obj.capitalize()

    if [word for word, pos in tagged_sent if pos == 'NNP']:
        subject2 = sub.capitalize()
    else:
        subject2 = sub.lower()

    print "subject:" + subject2
    print "object:" + object2
    result_sent2 = nltk.pos_tag(result3)
    print 'result_sent:',result_sent2

    if [word for word, pos in tagged_sent if pos == 'VBD']:
        tok = [word for word, pos in tagged_sent if pos == 'VBD']
        verb = ''.join(tok)
        past_participle = en.verb.past_participle(verb)

        if [word for word, pos in result_sent2 if pos == 'NNP' or 'NNI' or 'NNT' or 'NP']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                s1 = object2 + " were " + past_participle + " by " + subject2 + "."
                print 's1: ' + s1
            else:
                s2 = object2 + " was " + past_participle + " by " + subject2 + "."
                print 's2: ' + s2

        elif [word for word, pos in result_sent2 if pos == 'NNS']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                s3 = object2 + " were " + past_participle + " by " + subject2 + "."
                print 's3: ' + s3
            else:
                s4 = object2 + " was " + past_participle + " by " + subject2 + "."
                print 's4: ' + s4

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        verb = ''.join(tok)
        past_participle = en.verb.past_participle(verb)

        if [word for word, pos in result_sent2 if pos == 'NNP' or 'NNI' or 'NNT' or 'NP']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                s5 = object2 + " were " + past_participle + " by " + subject2 + "."
                print 's5: ' + s5
            else:
                s6 = object2 + " was " + past_participle + " by " + subject2 + "."
                print 's6 :' + s6


        elif [word for word, pos in result_sent2 if pos == 'NNS']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                s7 = object2 + " were " + past_participle + " by " + subject2 + "."
                print 's7 :' + s7
            else:
                s8 = object2 + " was " + past_participle + " by " + subject2 + "."
                print 's8 :' + s8
    else:
        print 'Wrongs'

    if answer2 == s1:
        count = count + 1
        print'correct1'
    elif answer2 == s2:
        count = count + 1
        print'correct2'
    elif answer2 == s3:
        count = count + 1
        print'correct3'
    elif answer2 == s4:
        count = count + 1
        print'correct4'
    if answer2 == s5:
        count = count + 1
        print'correct5'
    elif answer2 == s6:
        count = count + 1
        print'correct6'
    elif answer2 == s7:
        count = count + 1
        print'correct7'
    elif answer2 == s8:
        count = count + 1
        print'correct8'



    print '--------------------------------------------3---------------------------'

    text = nltk.word_tokenize(sentence3)
    tagged_sent = nltk.pos_tag(text)
    print 'tagged_sent:',tagged_sent

    np_extractor = NPExtractor(sentence3)
    result3 = np_extractor.extract()

    print "result3:"
    print result3
    sub = result3[0]
    obj = result3[-1]
    object3 = obj.capitalize()

    if [word for word, pos in tagged_sent if pos == 'NNP']:
        subject3 = sub.capitalize()
    else:
        subject3 = sub.lower()

    print "subject:" + subject3
    print "object:" + object3
    result_sent2 = nltk.pos_tag(result3)
    print 'result_sent:',result_sent2

    if [word for word, pos in tagged_sent if pos == 'VBD']:
        tok = [word for word, pos in tagged_sent if pos == 'VBD']
        verb = ''.join(tok)
        past_participle = en.verb.past_participle(verb)

        if [word for word, pos in result_sent2 if pos == 'NNP' or 'NNI' or 'NNT' or 'NP']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                t1 = object3 + " were " + past_participle + " by " + subject3 + "."
                print 't1: ' + t1
            else:
                t2 = object3 + " was " + past_participle + " by " + subject3 + "."
                print 't2: ' + t2

        elif [word for word, pos in result_sent2 if pos == 'NNS']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                t3 = object3 + " were " + past_participle + " by " + subject3 + "."
                print 't3: ' + t3
            else:
                t4 = object3 + " was " + past_participle + " by " + subject3 + "."
                print 't4: ' + t4

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tok = [word for word, pos in tagged_sent if pos == 'VBP']
        verb = ''.join(tok)
        past_participle = en.verb.past_participle(verb)

        if [word for word, pos in result_sent2 if pos == 'NNP' or 'NNI' or 'NNT' or 'NP']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                t5 = object3 + " were " + past_participle + " by " + subject3 + "."
                print 't5: ' + t5
            else:
                t6 = object3 + " was " + past_participle + " by " + subject3 + "."
                print 't6 :' + t6


        elif [word for word, pos in result_sent2 if pos == 'NNS']:

            print result_sent2[-1][1]
            if result_sent2[-1][1] == 'NNS':
                t7 = object3 + " were " + past_participle + " by " + subject3 + "."
                print 't7 :' + t7
            else:
                t8 = object3 + " was " + past_participle + " by " + subject3 + "."
                print 't8 :' + t8

    if answer3 == t1:
        count = count + 1
        print'correct1'
    elif answer3 == t2:
        count = count + 1
        print'correct2'
    elif answer3 == t3:
        count = count + 1
        print'correct3'
    elif answer3 == t4:
        count = count + 1
        print'correct4'
    elif answer3 == t5:
        count = count + 1
        print'correct5'
    elif answer3 == t6:
        count = count + 1
        print'correct6'
    elif answer3 == t7:
        count = count + 1
        print'correct7'
    elif answer3 == t8:
        count = count + 1
        print'correct8'


    else:
        print 'Wrongs'



    data_set={'s1':s1,'s2':s2,'s3':s3,'s4':s4,'s5':s5,'s6':s6,'s7':s7,'s8':s8,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t6':t6,'t7':t7,'t8':t8,
              'object':object,'p1':p1,'p2':p2,'p3':p3,'p4':p4,'p5':p5,'sentence1':sentence1,'sentence2':sentence2,'sentence3':sentence3,
              'p6':p6,'p7':p7,'p8':p8,'answer1':answer1,'answer2':answer2,'answer3':answer3,'subject':subject,'subject2':subject2,'object2':object2,
              'subject3':subject3,'object3':object3,'count':count}

    return render_template('level4_active_passive_evaluate.html', data_set=data_set)

#----------------level 4 Active Passive-CHAMIKA---------------

## ------------------------------------- Subscribe Teacher ----------------------------------------- ##

## Display All Teachers ##
@app.route('/display_teachers')
def display_teachers():
    cursor = db.cursor()
    sql = """SELECT * FROM users where role=%s """
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, ['Teacher'])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    cursor1 = db.cursor()
    sql1 = """SELECT u.fName,u.lName,s.teacher FROM users u, subscribe_teacher s where u.email=s.teacher AND s.status='pending' AND s.student=%s """
    try:
        # Execute the SQL command select all rows
        cursor1.execute(sql1, [session['username']])
        # fetch rows using fetchall() method.
        result1 = cursor1.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    cursor1 = db.cursor()
    sql1 = """SELECT u.fName,u.lName,s.teacher FROM users u, subscribe_teacher s where u.email=s.teacher AND s.status='accepted' AND s.student=%s """
    try:
        # Execute the SQL command select all rows
        cursor1.execute(sql1, [session['username']])
        # fetch rows using fetchall() method.
        subscribedResult = cursor1.fetchall()
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_teachers.html', data=result, student_data=result1, subscribedData=subscribedResult)


## Subscribe Teacher ##
@app.route('/subscribe_teacher/', methods=['GET'])
def subscribe_teacher():
    student = session['username']
    teacher = request.args.get('email')
    cursor = db.cursor()
    sql = """INSERT INTO subscribe_teacher (student,teacher) VALUES(%s,%s)"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [student, teacher])
        # Commit your changes in the database
        db.commit()
        alert(text='Your request under pending.', title='English Buddy', button='OK')
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('home'))


## Cancel Subscribe Teacher Request ##
@app.route('/cancel_teacher_subscribe_request/', methods=['GET'])
def cancel_teacher_subscribe_request():
    student = session['username']
    teacher = request.args.get('email')
    cursor = db.cursor()
    sql = """DELETE FROM subscribe_teacher WHERE teacher=%s AND student=%s"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [teacher, student])
        # Commit your changes in the database
        db.commit()
        # Get student subscribe request count
        student_subscribe_request_count()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_teachers'))


## Display All Subscribe Requests ##
@app.route('/display_student_subscribe_requests')
def display_student_subscribe_requests():
    cursor = db.cursor()
    sql = """SELECT u.fName,u.lName,u.school,u.image,u.placement_test,s.status,s.student FROM users u, subscribe_teacher s WHERE u.email=s.student AND s.status='pending' AND s.teacher=%s ORDER BY u.fName ASC"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()

        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_student_requests.html', data=result, query=query, count=count)


## Accept Subscribe Teacher Request ##
@app.route('/accept_teacher_subscribe_request/', methods=['GET'])
def accept_teacher_subscribe_request():
    teacher = session['username']
    student = request.args.get('email')
    cursor = db.cursor()
    sql = """UPDATE subscribe_teacher SET status='accepted' WHERE teacher=%s AND student=%s"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [teacher, student])
        # Commit your changes in the database
        db.commit()
        # Get student subscribe request count
        student_subscribe_request_count()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_student_subscribe_requests'))


## Decline Subscribe Teacher Request ##
@app.route('/decline_teacher_subscribe_request/', methods=['GET'])
def decline_teacher_subscribe_request():
    teacher = session['username']
    student = request.args.get('email')
    cursor = db.cursor()
    sql = """DELETE FROM subscribe_teacher WHERE teacher=%s AND student=%s"""

    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [teacher, student])
        # Commit your changes in the database
        db.commit()
        # Get student subscribe request count
        student_subscribe_request_count()
    except:
        # Rollback in case there is any error
        db.rollback()

    return redirect(url_for('display_student_subscribe_requests'))


## Display all students details who subscribes a teacher  ##
@app.route('/display_subscribe_student_details')
def display_subscribe_student_details():
    cursor = db.cursor()
    sql = """SELECT u.fName,u.lName,u.school,u.image,u.placement_test,s.status,s.student FROM users u, subscribe_teacher s WHERE u.email=s.student AND s.status='accepted' AND s.teacher=%s ORDER BY u.fName ASC"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username']])
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        db.commit()

        # Get student subscribe request count
        count=student_subscribe_request_count()
        # Get student subscribe request details
        query=display_student_subscribe_request_details()
    except:
        # Rollback in case there is any error
        db.rollback()

    return render_template('display_subscribe_student_details.html', data=result, query=query, count=count)


## ------------------------------------------------ Notifications --------------------------------------- ##

@app.route('/addChildren/', methods=['GET'])
def addChildren():
    Receiver = request.args.get('email')

    cursor = db.cursor()
    sql = """INSERT INTO notification (sender_email,receiver_email) VALUES(%s,%s)"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username'], Receiver])
        db.commit()
    except:
        db.rollback()

    return redirect(url_for('displayChildren'))


@app.route('/displayChildren')
def displayChildren():
    cursor = db.cursor()

    sql = """SELECT email,fname,lname,school,image FROM users WHERE role ='Student' AND email NOT IN (SELECT receiver_email FROM notification WHERE sender_email =%s) ORDER BY fname"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [session['username']])

        #fetch a single row using fetchone() method.
        query = cursor.fetchall()

    except:
        db.rollback()

    return render_template('addChild.html', data=query)



@app.route('/delete_request/', methods=['GET'])
def delete_request():
    id = request.args.get('id')

    cursor = db.cursor()
    sql = """delete from notification where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(escape_string(sql), [id])

        # fetch a single row using fetchone() method.
        db.commit()
    except:
        db.rollback()

    return redirect(url_for("home"))


@app.route('/accept_request/', methods=['GET'])
def accept_request():
    id = request.args.get('no')

    cursor = db.cursor()
    sql = """update notification set status='Accepted' where id=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [id])
        # fetch a single row using fetchone() method.
        db.commit()
        print('success')

    except:
        db.rollback()

    return redirect(url_for('home'))


def getSenderData(username):

    cursor = db.cursor()
    sql = """SELECT n.id,u.fName,u.lName,u.image FROM users u,notification n WHERE n.sender_email=u.email AND n.receiver_email=%s AND n.status='pending'"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [username])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return query

def getCount(username):

    cursor = db.cursor()
    sql = """SELECT count(*) from notification where receiver_email=%s and status='pending'"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [username])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return query


def getAcceptedData(username):
    cursor = db.cursor()

    sql = """SELECT n.receiver_email,u.fname,u.lname,u.image FROM users u, notification n WHERE n.receiver_email = u.email and status='Accepted'  and n.sender_email=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql, [username])
        #fetch a single row using fetchone() method.
        query = cursor.fetchall()
    except:
        db.rollback()

    return query



## ------------------------------------------level3_summary---------------------------------------------------------------------- ##


## ------------------------------------------level3_summary---------------------------------------------------------------------- ##


@app.route('/loadSummaryQues')
def loadSummaryQues():
    return render_template('Add_level3_summary.html')


@app.route('/addSummaryQues',methods=['POST'])
def addSummaryQues():


    Question1 = request.form['Question1']
    Question2 = request.form['Question2']
    Question3 = request.form['Question3']


    question1_exist=False
    question2_exist=False
    question3_exist=False

    cursor = db.cursor()
    sql ="""SELECT * FROM level3_summary WHERE question=%s OR question=%s OR question=%s"""
    try:    # Execute the SQL command
             cursor.execute(sql,[Question1,Question2,Question3])
             result = cursor.fetchall()

             print(cursor.fetchall())
             if result:
                for row in result:
                    if row[1]==Question1:
                        question1_exist=True
                    elif row[1]== Question2:
                        question2_exist=True
                    elif row[1]==Question3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'Question1':Question1, 'Question2':Question2, 'Question3':Question3,'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('Add_level3_summary.html', errors=errors)
                #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    rows = []
    if request.form.get('Question1') != '' :
        Question1 = request.form['Question1']
        rows.append(( Question1.strip(), session['username']))


    if request.form.get('Question2') != '' :
        Question2 = request.form['Question2']
        rows.append((Question2.strip(),session['username']))

    if request.form.get('Question3') != '':
        Question3 = request.form['Question3']
        rows.append((Question3.strip(),session['username']))

    cursor = db.cursor()
    sql = """INSERT INTO level3_summary (question,author) VALUES(%s,%s)"""

    try:
        # Execute the SQL command
        #cursor.execute(sql,[qusetion1,answer1])
        print 'add'
        cursor.executemany(sql, rows)
        db.commit()
    except:
        db.rollback()



    return render_template('Add_level3_summary.html')

@app.route('/level_3_summary')
def level_3_summary():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level3_summary order by rand() limit 1  """
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch rows using fetchall() method.
        query = cursor.fetchall()
        for row in query:
                data=row[1]

    except:
        db.rollback()


    return render_template('summary_level3.html', data=data)


@app.route('/evaluateSummary',methods=['POST'])
def evaluateSummary():
    value=request.form['Ques'].strip()
    answer=request.form['Answer'].strip()
    count_keywords=0
    status=""
    grammar=0
    content=0
    answer_sentences=sent_tokenize(answer)
    tokenizer = RegexpTokenizer(r'\w+')
    wordCount= len(tokenizer.tokenize(answer))
    print tokenizer.tokenize(answer)
    marks=0
    #check whether number of sentences equal to one


            # check sentence already existing in the question
    print answer_sentences
    print sent_tokenize(value)
    if any(sentence in sent_tokenize(value) for sentence in answer_sentences):
                status= 'Sentence already in the passage!'
                return render_template('summaryResult.html', answer=answer,status=status)

    else:
        top=keywords.top(value)
        print top
        print len(top)
        for count,word in top:
                    if word in answer:
                        count_keywords=count_keywords+1

        half=len(top)/2
        if count_keywords>0:
                conv =Ansi2HTMLConverter()
                array=[]

                array=ginger.main(answer)
                original_text=conv.convert(array[0])
                fixed_text=conv.convert(array[1])

                if array[1] =="Good English":

                        if wordCount >=5 and wordCount<=20:
                                       if(count_keywords>=half):
                                          marks=4.5
                                          content=3
                                          grammar=1.5
                                       else:
                                           marks=4
                                           content=2.5
                                           grammar=1.5
                        else:
                           marks=1.5
                           content=0

                else:
                    if wordCount >=5 and wordCount<=20:
                                       if(count_keywords>=half):
                                           if (array[2]>=2):
                                                   marks=3.5
                                                   grammar=0.5
                                                   content=3
                                           else:
                                               marks=3.5
                                               grammar=1
                                               content=2.5
                                       else:
                                          if (array[2]>=2):
                                                   marks=2
                                                   grammar=0.5
                                                   content=1.5
                                          else:
                                             marks=2.5
                                             grammar=1
                                             content=1.5
                    else:
                        marks=0.5
                        content=0
                        grammar=0.5
                print marks

                return render_template('summaryResult.html',original=original_text,fixed=fixed_text,answer=answer,status=status,wordCount=wordCount,grammar=grammar,content=content)
        else:
            status='Answer not complete!'
            return render_template('summaryResult.html', answer=answer,status=status)




    status='Your answer not relevant to the Question!'


    return render_template('summaryResult.html', answer=answer,status=status)



## ---------------------------------------------------------------------------------------------------------------- ##
###############level4 summary###############
###level4 summary##########

@app.route('/loadSummaryQues_level4')
def loadSummaryQues_level4():
    return render_template('Add_level4_summary.html')





@app.route('/addSummaryQues_Level4',methods=['POST'])
def addSummaryQues_Level4():


    Question1 = request.form['Question1']
    Question2 = request.form['Question2']
    Question3 = request.form['Question3']


    question1_exist=False
    question2_exist=False
    question3_exist=False

    cursor = db.cursor()
    sql ="""SELECT * FROM level4_summary WHERE question=%s OR question=%s OR question=%s"""
    try:    # Execute the SQL command
             cursor.execute(sql,[Question1,Question2,Question3])
             result = cursor.fetchall()

             print(cursor.fetchall())
             if result:
                for row in result:
                    if row[1]==Question1:
                        question1_exist=True
                    elif row[1]== Question2:
                        question2_exist=True
                    elif row[1]==Question3:
                        question3_exist=True


                alert(text='Questions Already exists !', title='English Buddy', button='OK')
                errors={'Question1':Question1, 'Question2':Question2, 'Question3':Question3,'question1Status':question1_exist, 'question2Status':question2_exist, 'question3Status':question3_exist}
                return render_template('Add_level4_summary.html', errors=errors)
                #flash('Question successfully added !')

    except:
        # Rollback in case there is any error
        db.rollback()

    rows = []
    if request.form.get('Question1') != '' :
        Question1 = request.form['Question1']
        rows.append(( Question1.strip(), session['username']))


    if request.form.get('Question2') != '' :
        Question2 = request.form['Question2']
        rows.append((Question2.strip(),session['username']))

    if request.form.get('Question3') != '':
        Question3 = request.form['Question3']
        rows.append((Question3.strip(),session['username']))

    cursor = db.cursor()
    sql = """INSERT INTO level4_summary (question,author) VALUES(%s,%s)"""

    try:
        # Execute the SQL command
        #cursor.execute(sql,[qusetion1,answer1])
        print 'add'
        cursor.executemany(sql, rows)
        db.commit()
    except:
        db.rollback()



    return render_template('Add_level4_summary.html')


@app.route('/level_4_summary')
def level_4_summary():
    cursor = db.cursor()

    sql = """SELECT * FROM english_buddy.level4_summary order by rand() limit 1  """
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # fetch rows using fetchall() method.
        query = cursor.fetchall()
        for row in query:
                data=row[1]

    except:
        db.rollback()


    return render_template('summary_level4.html', data=data)


@app.route('/evaluateSummary_level4',methods=['POST'])
def evaluateSummary_level4():
    value=request.form['Ques'].strip()
    answer=request.form['Answer'].strip()
    count_keywords=0
    status=""
    answer_sentences=sent_tokenize(answer)
    wordCount= len(word_tokenize(answer))
    print word_tokenize(answer)
    marks=0
    #check whether number of sentences equal to one


            # check sentence already existing in the question

    print sent_tokenize(value)
    if any(sentence in sent_tokenize(value) for sentence in answer_sentences):
                status= 'Sentence already in the passage!'
                return render_template('summaryResult.html', answer=answer,status=status)

    else:
        top=keywords.top(value)

        print top
        for count,word in top:
                    if word in answer:
                        count_keywords=count_keywords+1
        print(count_keywords)
        half=len(top)/2
        if count_keywords>0:
                conv =Ansi2HTMLConverter()
                array=[]

                array=ginger.main(answer)
                original_text=conv.convert(array[0])
                fixed_text=conv.convert(array[1])

                if array[1] =="Good English":

                        if len(word_tokenize(answer))>=5 and len(word_tokenize(answer))<=35:
                                       if(count_keywords>=half):
                                           marks=4.5
                                       else:
                                           marks=4
                        else:
                           marks=1.5

                else:
                    if len(word_tokenize(answer))>=5 and len(word_tokenize(answer))<=35:
                                       if(count_keywords>=half):
                                           if (array[2]>=2):
                                                   marks=3
                                           else:
                                               marks=3.5
                                       else:
                                          if (array[2]>=2):
                                                   marks=2
                                          else:
                                             marks=2.5
                    else:
                        marks=0.5
                print marks
                return render_template('summaryResult.html',original=original_text,fixed=fixed_text,answer=answer,status=status,wordCount=wordCount)
        else:
            status='Answer not complete!'
            return render_template('summaryResult.html', answer=answer,status=status)




    status='Your answer not relevant to the Question!'


    return render_template('summaryResult.html', answer=answer,status=status)

############level4 sumary#######################
##level 1 ranking ##



@app.route('/level1_ranking')
def level1_ranking():

    marks=0

    cursor=db.cursor()
    sql="""select marks from marks where user=%s"""
    try:
      cursor.execute(sql,[session['username']])
      result=cursor.fetchall()

      if result:
          for row in result:
              marks=row[0]
      db.commit()
    except:
        db.rollback()


    cursor = db.cursor()


    sql = """Insert into temp (question,answer) (select question,answer from level1_articles order by rand() limit 5) union (select question,answer from level_1_adjectives order by rand() limit 5) union (select question,correct from prepositions order by rand() limit 5) union (select question,answer from conjunctions order by rand() limit 5)"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)

        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()


    cursor = db.cursor()
    array=[]
    sql = """SELECT question,answer FROM temp order by rand() limit 10"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        result = cursor.fetchall()
        # Commit your changes in the database
        for row in result:
            answer =row[1]
            array.append(answer)
        shuffle(array)
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()


    return render_template('level1_rating.html',result=result,answer=array,marks=marks)

@app.route('/evaluate_ranking', methods=['POST'])
def evaluate_ranking():

       count=0
       provided_answer1=request.form['provideAnswer1']
       provided_answer2=request.form['provideAnswer2']
       provided_answer3=request.form['provideAnswer3']
       provided_answer4=request.form['provideAnswer4']
       provided_answer5=request.form['provideAnswer5']
       provided_answer6=request.form['provideAnswer6']
       provided_answer7=request.form['provideAnswer7']
       provided_answer8=request.form['provideAnswer8']
       provided_answer9=request.form['provideAnswer9']
       provided_answer10=request.form['provideAnswer10']

       correct_answer1=request.form['correct_answer1']
       correct_answer2=request.form['correct_answer2']
       correct_answer3=request.form['correct_answer3']
       correct_answer4=request.form['correct_answer4']
       correct_answer5=request.form['correct_answer5']
       correct_answer6=request.form['correct_answer6']
       correct_answer7=request.form['correct_answer7']
       correct_answer8=request.form['correct_answer8']
       correct_answer9=request.form['correct_answer9']
       correct_answer10=request.form['correct_answer10']

       if provided_answer1.strip()==correct_answer1:
           count=count+1

       if provided_answer2.strip()==correct_answer2:
           count=count+1
       if provided_answer3.strip()==correct_answer3:
           count=count+1


       if provided_answer4.strip()==correct_answer4:
            count=count+1

       if provided_answer5.strip()==correct_answer5:
           count=count+1

       if provided_answer6.strip()==correct_answer6:
           count=count+1
       if provided_answer7.strip()==correct_answer7:
           count=count+1
       if provided_answer8.strip()==correct_answer8:
           count=count+1

       if provided_answer9.strip()==correct_answer9:
           count=count+1

       if provided_answer10.strip()==correct_answer10:
           count=count+1
       print(count)

       sql = """SELECT user,marks FROM marks where user=%s"""
       try:
         cursor = db.cursor()
            # Execute the SQL command
         cursor.execute(sql,[session['username']])

            # fetch a single row using fetchone() method.
         data = cursor.fetchall()

         if data:

            for row in data:
                marks=row[1]


            last_mark=marks+count

            cursor = db.cursor()
            sql = """update marks set marks=%s where user=%s"""
            try:
                    # Execute the SQL command
              cursor.execute(sql, [last_mark,session['username']])
                    # Commit your changes in the database
              db.commit()
                    #flash('Successfully Updated !')
            except:
                    # Rollback in case there is any error
               db.rollback()
         else:
            cursor = db.cursor()
            sql = """INSERT INTO marks(marks,user) VALUES(%s,%s)"""

            try:
                  # Execute the SQL command
              cursor.execute(sql, [count, session['username']])
                  # Commit your changes in the database
              db.commit()
                  #flash('Question successfully added !')
            except:
                    # Rollback in case there is any error
               db.rollback()

         cursor = db.cursor()
         sql = """Truncate table temp"""

         try:
                  # Execute the SQL command
           cursor.execute(sql)
                  # Commit your changes in the database
           db.commit()
                  #flash('Question successfully added !')
         except:
                    # Rollback in case there is any error
            db.rollback()

       except:
           db.rollback()
       return redirect(url_for('view_level1_ratings'))

@app.route('/view_level1_ratings')
def view_level1_ratings():
    #display first five rankings
    cursor = db.cursor()

    sql = """SELECT u.fName,u.lName,u.image,m.marks,u.email FROM users u ,marks m where u.placement_test='Elementary' and u.email=m.user order by marks DESC limit 5"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        firstFive = cursor.fetchall()

        includeFirstFive='false'

        for row in firstFive:
            if row[4]==session['username']:
                includeFirstFive='true'

    except:
        db.rollback()

    sql = """select u.image,u.fName,u.lName,m.marks,u.email from marks m, users u where u.email=m.user AND m.marks IN (SELECT MIN(m1.marks) FROM marks m1, users u1 WHERE u1.placement_test='Elementary' AND u1.email=m1.user AND m1.marks>(select m3.marks from marks m3 where m3.user=%s)) UNION
select u.image,u.fName,u.lName,m.marks,u.email from marks m, users u where u.email=m.user AND m.user=%s AND u.placement_test='Elementary'
UNION
select u.image,u.fName,u.lName,m.marks,u.email from marks m, users u where u.email=m.user AND m.marks IN (SELECT MAX(m1.marks) FROM marks m1, users u1 WHERE u1.placement_test='Elementary' AND u1.email=m1.user AND m1.marks<(select m3.marks from marks m3 where m3.user=%s))
"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql,[session['username'], session['username'], session['username']])
        # fetch rows using fetchall() method.
        data = cursor.fetchall()
    except:
        db.rollback()


    return render_template("viewRatings.html", firstFive=firstFive,data=data,includeFirstFive=includeFirstFive)



@app.route('/view_level2_ratings')
def view_level2_ratings():

    # display first five rankings
    cursor = db.cursor()

    sql = """SELECT u.fName,u.lName,u.image,m.marks,u.email FROM users u ,marks m where u.placement_test='Preliminary' and u.email=m.user order by marks DESC limit 5"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql)
        # fetch rows using fetchall() method.
        firstFive = cursor.fetchall()

        includeFirstFive = 'false'

        for row in firstFive:
            if row[4] == session['username']:
                includeFirstFive = 'true'

    except:
        db.rollback()

    sql = """select u.image,u.fName,u.lName,m.marks,u.email from marks m, users u where u.email=m.user AND m.marks IN (SELECT MIN(m1.marks) FROM marks m1, users u1 WHERE u1.placement_test='Preliminary' AND u1.email=m1.user AND m1.marks>(select m3.marks from marks m3 where m3.user=%s)) UNION
select u.image,u.fName,u.lName,m.marks,u.email from marks m, users u where u.email=m.user AND m.user=%s AND u.placement_test='Preliminary'
UNION
select u.image,u.fName,u.lName,m.marks,u.email from marks m, users u where u.email=m.user AND m.marks IN (SELECT MAX(m1.marks) FROM marks m1, users u1 WHERE u1.placement_test='Preliminary' AND u1.email=m1.user AND m1.marks<(select m3.marks from marks m3 where m3.user=%s))
"""
    try:
        # Execute the SQL command select all rows
        cursor.execute(sql, [session['username'], session['username'], session['username']])
        # fetch rows using fetchall() method.
        data = cursor.fetchall()
    except:
        db.rollback()


    return render_template("viewLevel2Ratings.html", firstFive=firstFive,data=data, includeFirstFive=includeFirstFive)


@app.route('/level2_Ranking_Test')
def level2_Ranking_Test():


    marks=0

    cursor=db.cursor()
    sql="""select marks from marks where user=%s"""
    try:
      cursor.execute(sql,[session['username']])
      result=cursor.fetchall()

      if result:
          for row in result:
              marks=row[0]
      db.commit()
    except:
        db.rollback()


    array=[]
    value= random.choice([1,2,3])
    print value
    if value==1:
        category='jumble_sentences'
        cursor = db.cursor()
        sql = """SELECT * FROM jumblesentences order by rand()limit 10"""
        try:
           # Execute the SQL command
          cursor.execute(sql)
          # fetch a single row using fetchone() method.
          result = cursor.fetchall()
        except:
          db.rollback()

    if value==2:
        category='dialogs'
        cursor = db.cursor()
        sql = """SELECT * FROM dialogs where level='level2' order by rand() limit 1 """
        try:
        # Execute the SQL command select all rows
         cursor.execute(sql)
        # fetch rows using fetchall() method.
         result = cursor.fetchall()
        # Commit your changes in the database
         db.commit()
        except:
        # Rollback in case there is any error
          db.rollback()

    if value==3:

         category='match_pronoun'
         cursor=db.cursor();
         sql="""Insert into temp2 (question,answer) (select question,answer from level2_match order by rand() limit 6) union (select question,answer from level_2_pronoun order by rand() limit 6)"""
         try:
        # Execute the SQL command select all rows
          cursor.execute(sql)
        # fetch rows using fetchall() method.
         except:
        # Rollback in case there is any error
          db.rollback()

         cursor = db.cursor()
         array=[]
         sql = """SELECT question,answer FROM temp2 order by rand() limit 10"""
         try:
        # Execute the SQL command select all rows
           cursor.execute(sql)
        # fetch rows using fetchall() method.
           result = cursor.fetchall()
           print(result)
        # Commit your changes in the database
           for row in result:
               answer =row[1]
               array.append(answer)
           shuffle(array)


         except:
           # Rollback in case there is any error
            db.rollback()


    return render_template("level2_rating.html",category=category,result=result,answer=array,marks=marks)

@app.route('/evaluate_level2_ranking',methods=['POST'])
def evaluate_level2_ranking():
    category=request.form['category']
    count=0

    if category=='jumble_sentences':
        provided_answer1=request.form['jumbleSentence_provided_answer1']
        provided_answer2=request.form['jumbleSentence_provided_answer2']
        provided_answer3=request.form['jumbleSentence_provided_answer3']
        provided_answer4=request.form['jumbleSentence_provided_answer4']
        provided_answer5=request.form['jumbleSentence_provided_answer5']
        provided_answer6=request.form['jumbleSentence_provided_answer6']
        provided_answer7=request.form['jumbleSentence_provided_answer7']
        provided_answer8=request.form['jumbleSentence_provided_answer8']
        provided_answer9=request.form['jumbleSentence_provided_answer9']
        provided_answer10=request.form['jumbleSentence_provided_answer10']

        correct_answer1=request.form['jumbleSentence_correct_answer1']
        correct_answer2=request.form['jumbleSentence_correct_answer2']
        correct_answer3=request.form['jumbleSentence_correct_answer3']
        correct_answer4=request.form['jumbleSentence_correct_answer4']
        correct_answer5=request.form['jumbleSentence_correct_answer5']
        correct_answer6=request.form['jumbleSentence_correct_answer6']
        correct_answer7=request.form['jumbleSentence_correct_answer7']
        correct_answer8=request.form['jumbleSentence_correct_answer8']
        correct_answer9=request.form['jumbleSentence_correct_answer9']
        correct_answer10=request.form['jumbleSentence_correct_answer10']

        if provided_answer1.strip()==correct_answer1:
            count=count+1

        if provided_answer2.strip()==correct_answer2:
            count=count+1

        if provided_answer3.strip()==correct_answer3:
            count=count+1
        if provided_answer4.strip()==correct_answer4:
            count=count+1

        if provided_answer5.strip()==correct_answer5:
            count=count+1
        if provided_answer6.strip()==correct_answer6:
            count=count+1

        if provided_answer7.strip()==correct_answer7:
            count=count+1

        if provided_answer8.strip()==correct_answer8:
            count=count+1
        if provided_answer9.strip()==correct_answer9:
            count=count+1

        if provided_answer10.strip()==correct_answer10:
            count=count+1


    if category=='match_pronoun':
        provided_answer1=request.form['match_pronoun_provideAnswer1']
        provided_answer2=request.form['match_pronoun_provideAnswer2']
        provided_answer3=request.form['match_pronoun_provideAnswer3']
        provided_answer4=request.form['match_pronoun_provideAnswer4']
        provided_answer5=request.form['match_pronoun_provideAnswer5']
        provided_answer6=request.form['match_pronoun_provideAnswer6']
        provided_answer7=request.form['match_pronoun_provideAnswer7']
        provided_answer8=request.form['match_pronoun_provideAnswer8']
        provided_answer9=request.form['match_pronoun_provideAnswer9']
        provided_answer10=request.form['match_pronoun_provideAnswer10']

        correct_answer1=request.form['match_pronounAnswer1']
        correct_answer2=request.form['match_pronounAnswer2']
        correct_answer3=request.form['match_pronounAnswer3']
        correct_answer4=request.form['match_pronounAnswer4']
        correct_answer5=request.form['match_pronounAnswer5']
        correct_answer6=request.form['match_pronounAnswer6']
        correct_answer7=request.form['match_pronounAnswer7']
        correct_answer8=request.form['match_pronounAnswer8']
        correct_answer9=request.form['match_pronounAnswer9']
        correct_answer10=request.form['match_pronounAnswer10']

        if provided_answer1.strip()==correct_answer1:
            count=count+1

        if provided_answer2.strip()==correct_answer2:
            count=count+1

        if provided_answer3.strip()==correct_answer3:
            count=count+1
        if provided_answer4.strip()==correct_answer4:
            count=count+1

        if provided_answer5.strip()==correct_answer5:
            count=count+1
        if provided_answer6.strip()==correct_answer6:
            count=count+1

        if provided_answer7.strip()==correct_answer7:
            count=count+1

        if provided_answer8.strip()==correct_answer8:
            count=count+1
        if provided_answer9.strip()==correct_answer9:
            count=count+1

        if provided_answer10.strip()==correct_answer10:
            count=count+1

    if category=='dialogs'  :
        qNo = request.form['qNo']
        pa1 = request.form['dialog_answer1']
        pa2 = request.form['dialog_answer2']
        pa3 = request.form['dialog_answer3']
        pa4 = request.form['dialog_answer4']
        pa5 = request.form['dialog_answer5']

        cursor = db.cursor()
        sql = """SELECT * FROM dialogs where qNo=%s"""
        try:
            # Execute the SQL command
            cursor.execute(sql, [qNo])

            # fetch a single row using fetchone() method.
            data = cursor.fetchall()
            for row in data:
                a1 = row[4]
                a2 = row[5]
                a3 = row[6]
                a4 = row[7]
                a5 = row[8]


            if a1 == pa1:

               count=count+2


            if a2 == pa2:
                 count=count+2

            if a3 == pa3:
                count=count+2
            if a4 == pa4:
                 count=count+2

            if a5 == pa5:
                 count=count+2
        except:
            db.rollback()

    sql = """SELECT user,marks FROM marks where user=%s"""
    try:
         cursor = db.cursor()
            # Execute the SQL command
         cursor.execute(sql,[session['username']])

            # fetch a single row using fetchone() method.
         data = cursor.fetchall()

         if data:

            for row in data:
                marks=row[1]


            last_mark=marks+count

            cursor = db.cursor()
            sql = """update marks set marks=%s where user=%s"""
            try:
                    # Execute the SQL command
              cursor.execute(sql, [last_mark,session['username']])
                    # Commit your changes in the database
              db.commit()
                    #flash('Successfully Updated !')
            except:
                    # Rollback in case there is any error
               db.rollback()
         else:
            cursor = db.cursor()
            sql = """INSERT INTO marks(marks,user) VALUES(%s,%s)"""

            try:
                  # Execute the SQL command
              cursor.execute(sql, [count, session['username']])
                  # Commit your changes in the database
              db.commit()
                  #flash('Question successfully added !')
            except:
                    # Rollback in case there is any error
               db.rollback()

         cursor = db.cursor()
         sql = """Truncate table temp2"""

         try:
                  # Execute the SQL command
           cursor.execute(sql)
                  # Commit your changes in the database
           db.commit()
                  #flash('Question successfully added !')
         except:
                    # Rollback in case there is any error
            db.rollback()

    except:
        db.rollback()

    return redirect(url_for('view_level2_ratings'))


### ----------------------------------- Contact Teacher -------------------------------------------- ###

## Display Contact Teacher Page ##
@app.route('/view_contact_teacher')
def view_contact_teacher():

    cursor = db.cursor()
    sql = """SELECT u.fName,u.lName,u.image,u.email FROM users u, subscribe_teacher s WHERE u.email=s.teacher AND s.status='accepted' AND s.student=%s"""
    try:
        # Execute the SQL command
        cursor.execute(sql,[session['username']])
        # fetch a single row using fetchone() method.
        result = cursor.fetchall()

        if result:
            return render_template('contact_teacher.html',data=result)
        else:
            #alert(text='You are not subscribe a teacher yet. Please Subscribe a teacher to send messages.', title='English Buddy', button='OK')
            return render_template('contact_teacher.html')
    except:
        db.rollback()

    #return render_template('contact_teacher.html')


## Contact Teacher - Send email ##
@app.route('/contact_teacher',methods=['POST'])
def contact_teacher():

    teacher = request.form['teacher']
    student = request.form['student']
    message = request.form['question']

    ## Send email ##
    msg = Message('English Buddy - Student Questions', sender="englishbuddy.edu@gmail.com")
    msg.recipients = [teacher]
    msg.html = "<body bgcolor='#DCEEFC'><b>Dear Sir/Mis,</b><br><br><p>" + message + " </p><br><br><br><br>Student email : "+ student +"<br><br><a href='http://127.0.0.1:5000/'>Sign in Now</a><br></body>"
    mail.send(msg)

    alert(text='Message sent successfully ! Please check your e-mail for a reply.', title='English Buddy', button='OK')
    return redirect(url_for('view_contact_teacher'))



## ---------------------------------------------------------------------------------------------------------------- ##

def check_internet_connection():
    REMOTE_SERVER = "www.google.com"
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

# -------------------------------------------------------------


# Listen to the level4 dialog question
@app.route('/speak_dialog', methods=['GET'])
def speak_dialog():

    question1 = request.args.get('question1').split(":")[1]
    question2 = request.args.get('question2').split(":")[1]
    question3 = request.args.get('question3').split(":")[1]
    question4 = request.args.get('question4').split(":")[1]
    question5 = request.args.get('question5').split(":")[1]
    if request.args.get('question6') != "":
        question6 = request.args.get('question6').split(":")[1]
    else:
        question6 = ""

    answer1 = request.args.get('answer1')
    answer2 = request.args.get('answer2')
    answer3 = request.args.get('answer3')
    answer4 = request.args.get('answer4')
    answer5 = request.args.get('answer5')

    engine = pyttsx.init()
    engine.setProperty('rate', 120)

    engine.say(question1)
    engine.say(answer1)
    engine.say(question2)
    engine.say(answer2)
    engine.say(question3)
    engine.say(answer3)
    engine.say(question4)
    engine.say(answer4)
    engine.say(question5)
    engine.say(answer5)
    engine.say(question6)

    engine.runAndWait()

    return 'True'


# Stop level4 dialog reading
@app.route('/stop_dialog_reading', methods=['GET'])
def stop_dialog_reading():

    return 'True'



# Listen to level1 and level3 conjunction activity questions
@app.route('/speak_conjunction', methods=['GET'])
def speak_conjunction():

    statement = request.args.get('question').split("#")[0]+request.args.get('answer')+request.args.get('question').split("#")[1]

    engine = pyttsx.init()
    engine.setProperty('rate', 120)
    engine.say(statement)
    engine.runAndWait()

    return 'True'

# --------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)

