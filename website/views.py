from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required,  current_user, logout_user
from .models import Message
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/home', methods=['GET', 'POST', 'PUT'])
@login_required
def home_login():
    return render_template('home_login.html', user=current_user)


@views.route('/pricing')
def pricing():
    return render_template('pricing.html', user=current_user)


@views.route('/delete-message', methods=['POST'])
@login_required
def delete_message():
    message = json.loads(request.data)
    messageId = message['messageId']
    message = Message.query.get(messageId)
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

    return redirect('/home')


@views.route('/activate-message', methods=['POST'])
@login_required
def activate_message():
    message = json.loads(request.data)
    messageId = message['messageId']
    message = Message.query.get(messageId)
    if message:
        if message.user_id == current_user.id:
            message.activate()
            db.session.commit()
            flash("Message activated successfully.", category='success')
    return redirect('/home')


@views.route('/save-message', methods=['GET', 'POST', 'PUT'])
@login_required
def save_message():
    if request.method == 'POST':
        message = request.form.get('message')
        num_messages = Message.query.filter_by(user_id=current_user.id).count()
        if num_messages < 3:
            if len(message) < 1:
                flash('Message is to short', category='error')
            else:
                new_message = Message(message=message, user_id=current_user.id)
                db.session.add(new_message)
                db.session.commit()
                flash("Message has been saved.", category='success')
        else:
            flash("Limit of 3 Message templates reached", category='error')
    return redirect('/home')


@views.route('/unsubscribe', methods=['GET', 'POST'])
@login_required
def unsubscribe():
    if request.method == 'POST':
        return redirect('/delete-user')
    return render_template('unsubscribe.html', user=current_user)


@views.route('/delete-user', methods=['POST'])
@login_required
def delete_user():
    # Delete the user's data from the database
    user = current_user
    db.session.delete(user)
    db.session.commit()

    # Log the user out
    logout_user()

    # Redirect to the home page or a confirmation page
    flash("Your data has been deleted. Thank you for using our service.",
          category='success')
    print('user left service')
    return redirect('/')
