from flask import render_template, flash, request, redirect, url_for, session, jsonify, abort
from app import app, db, models, admin
from .forms import LogInUser, TypeMessage, ReviewGame
from flask_sqlalchemy import SQLAlchemy
# Admin
from flask_admin.contrib.sqla import ModelView
from .models import UserInfo, Messages, Groups, Games, Review
# Logging
import logging
# Json
import json
# External Python Files
# from app.recommendation import recom

app.app_context().push()

# Register model with flask admin
admin.add_view(ModelView(UserInfo, db.session))
admin.add_view(ModelView(Games, db.session))
admin.add_view(ModelView(Groups, db.session))
admin.add_view(ModelView(Messages, db.session))
admin.add_view(ModelView(Review, db.session))

# Login to Website - store username into session

@app.route('/', methods=['GET', 'POST'])
def login():
    heading = {'head': 'Welcome to Hub!'}
    form = LogInUser()
    if request.method == "POST":
        if form.validate_on_submit():
            # Check if username in database, Check if password matches username
            existing_name = models.UserInfo.query.filter_by(username=form.username.data).first()
            existing_pass = models.UserInfo.query.filter_by(username=form.username.data, password=form.password.data).first()
            if existing_name == None:
                app.logger.warning("---Failed login---")
                flash("Username doesn't exist")
                return redirect(url_for('login'))
            if existing_pass == None:
                app.logger.warning("---%s Failed login---", form.username.data)
                flash("Password doesn't match Username")
                return redirect(url_for('login'))
            # Load home page, Save username via Session
            else:
                session.pop('username', None)
                session['username'] = form.username.data
                curr_user = session.get('username')
                if (existing_name.id == 1):
                    # Log the Admin Access
                    return redirect(url_for('admin'))
                app.logger.warning("---Successful login---")
                return redirect(url_for('home'))
    
    return render_template("login.html", title="Login", heading=heading, form=form)

# Signup to Website

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    heading = { 'head': 'Sign Up Here!' }
    form = LogInUser()
    userinfo = models.UserInfo.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            # Check Email is typed in - As made Optional for Login
            if form.email.data == '':
                flash("No Email Entered, Try Again")
                return redirect(url_for('signup'))
            # Check email isn't in Database - Return None if true
            existing_email = models.UserInfo.query.filter(models.UserInfo.email == form.email.data).first()
            if existing_email != None:
                flash("Email already in use for another account, Try Again")
                return redirect(url_for('signup'))
            # Check username isn't in Database - Return None if true
            existing_user = models.UserInfo.query.filter(models.UserInfo.username == form.username.data).first()
            if existing_user != None:
                flash("Username already in use for another account, Try Again")
                return redirect(url_for('signup'))
            # Add new user to database and take them to home page
            else:
                record = models.UserInfo(email=form.email.data, username=form.username.data, password=form.password.data)
                db.session.add(record)
                db.session.commit()
                session.pop('username', None)
                session['username'] = form.username.data
                return redirect(url_for('home'))
                
    return render_template("signup.html", title="Sign Up", heading=heading, form=form, userinfo=userinfo)

# Stop Admin Access

@app.route('/admin')
def admin():
    curr_user = session.get('username')
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    if user.id != 1:
        abort(403)
    return "This is the Admin Page. Logged in as "+curr_user

# Display Home Page for User

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Get Record of Current User
    curr_user = session.get('username')
    heading = { 'head': 'Welcome, '+curr_user}
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    # Get User's Games and Groups
    groups = []
    for i in user.group:
        groups.append(i)
    games = []
    for i in user.games:
        for j in i.review:
            if j.user_id == user.id:
                games.append(j)
    return render_template('home.html', title='Home', heading=heading, groups=groups, games=games)

# Delete Account

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    curr_user = session.get('username')
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('login'))


# View Groups to Join

@app.route('/view_group', methods=['GET', 'POST'])
def view_group():
    curr_user = session.get('username')
    groups = models.Groups.query.all()
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    for i in user.group:
        temp_g = models.Groups.query.filter_by(id=i.id).first()
        groups.remove(temp_g)
    return render_template('viewgroup.html', title='Groups', groups=groups)

# Join Group

@ app.route('/join_group', methods=['GET', 'POST'])
def join_group():
    # Get User Record and Group to-join Record
    curr_user = session.get('username')    
    record = request.form.get("add_button")
    g = models.Groups.query.get(record)
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    user.group.append(g)
    db.session.commit()
    groups = models.Groups.query.all()
    return redirect(url_for('view_group'))

# Leave Group

@app.route('/leave_group', methods=['GET', 'POST'])
def leave_group():
    curr_user = session.get('username')
    record = request.form.get("leave_but")
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    group = models.Groups.query.filter_by(id=record).first()
    user.group.remove(group)
    db.session.commit()
    return redirect(url_for('home'))

# Load and Send Messages to Group 

@app.route('/chat_group', methods=['GET', 'POST'])
def chat_group():
    # Saves the group ID as session - Check if already saved Group
    record = request.form.get("chat_button")
    if record == None:
        record = session.get("current_group")
    else:
        session['current_group'] = record
    # Get Username 
    curr_user = session.get('username')
    this_group = models.Groups.query.filter_by(id=record).first()
    heading = { 'head': this_group.group_name}
    # Type Message and Save it with username of who sent it
    form = TypeMessage()
    chats = []
    if form.validate_on_submit():
        new_chat = models.Messages(text=curr_user + ": " + form.text.data, group_id=record)
        db.session.add(new_chat)
        this_group.messages.append(new_chat)
        db.session.commit()
    # Display Messages
    for i in this_group.messages:
        chats.append(i)
    return render_template('chatgroup.html', title=this_group.group_name, heading=heading, form=form, groups=this_group)

# Update Likes and Dislikes

@app.route('/update_likes', methods=['GET', 'POST'])
def update_likes():
    data = json.loads(request.data)
    # Get the Message
    current_msg = models.Messages.query.filter_by(id=data['id']).first()
    # Get the current user for ID
    curr_user = session.get('username')
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    action = data['action']
    # Check if User has interacted with this message
    for i in current_msg.users:
        # User has interacted
        if i.id == user.id:
            # User Presses Like
            if action == "like" :
                # Previous Action Was Like -> Decrease Like            
                if session.get("pre_action") == "like":
                    print("Pressed Like, Already Liked")
                    current_msg.like -= 1
                    current_msg.users.remove(user)

                elif session.get("pre_action") == "dislike":
                    print("Pressed Like, Already Disliked")
                    current_msg.dislike = max(current_msg.dislike-1, 0)
                    current_msg.like += 1
                    session["pre_action"] = action
                    print(session.get("pre_action"))
            # User Presses Dislike
            else:
                if session.get("pre_action") == "like":
                    print("Pressed Dislike, Already Liked")
                    current_msg.like = max(current_msg.like-1, 0)
                    current_msg.dislike += 1
                    session['pre_action'] = action

                elif session.get("pre_action") == "dislike":
                    print("Pressed Disliked, Already Disliked")
                    current_msg.dislike -= 1
                    current_msg.users.remove(user)
                
            db.session.commit()
            return json.dumps({"status": "OK", "likes": current_msg.like, "dislikes": current_msg.dislike})
    # User hasn't Interacted - Save Action as Session
    if action == "like":
        current_msg.like += 1
        session['pre_action'] = action 
    else:
        current_msg.dislike += 1
        session['pre_action'] = action 
    current_msg.users.append(user)
    db.session.commit()
    return json.dumps({"status": "OK", "likes": current_msg.like, "dislikes": current_msg.dislike})

# Find Games to rate - Display Average

@app.route('/search_game', methods=['GET','POST'])
def search_game():
    heading = { 'head': "Search for Games"}
    games = models.Games.query.all()
    # Get Average Rating of specific game and save to list
    average_list = []
    for i in games:
        average = 0
        total = 0
        no_of_reviews = 0
        for j in i.review:
            total += j.rating
            no_of_reviews += 1
        # Account for no reviews - cause zero division error
        try:
            average = round(total/no_of_reviews, 1)
            if average > 0:
                average_list.append(average)
        except ZeroDivisionError:
            average_list.append(0)
    return render_template("searchgames.html", title="Find Games", heading=heading, games=games, average_list=average_list)

# Review Game

@app.route('/review_game', methods=['GET', 'POST'])
def review_game():
    # Get and store Game ID
    record = request.form.get("review_btn")
    if record == None:
        record = session.get("current_game")
    else:
        session['current_game'] = record
    this_game = models.Games.query.filter_by(id=record).first()
    # Get User ID
    curr_user = session.get('username')
    user = models.UserInfo.query.filter_by(username=curr_user).first()
    heading = { 'head': this_game.name}
    form = ReviewGame()
    temp_reviews = []
    # User Makes Review
    if form.validate_on_submit():
        # Loop through and find review - Update Old Review
        for i in this_game.review:
            if i.user_id == user.id:
                i.rating = form.rating.data
                i.text = form.text.data
                db.session.commit()
                return redirect(url_for('review_game'))
        # If Not found - New Review Made and added to u
        new_review = models.Review(user_id=user.id, username=curr_user,name=this_game.name, rating=form.rating.data, text=form.text.data, game_id=this_game.id)
        db.session.add(new_review)
        db.session.commit()
        this_game.review.append(new_review)
        if this_game not in user.games:
            user.games.append(this_game)
        db.session.commit()
    # Display Reviews
    for i in this_game.review:
        temp_reviews.append(i)
    return render_template("reviewgame.html", title="Game Name", heading=heading, form=form, games=this_game)