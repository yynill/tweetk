from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required,  current_user
from .models import Message
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/home', methods=['GET', 'POST', 'PUT'])
@login_required
def logged_in_home():
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
                flash('Message has been saved.', category='success')
        else:
            flash('Limit of 3 Message templates reached', category='error')

    return render_template('logged_in_home.html', user=current_user)


@views.route('/pricing')
def pricing():
    return render_template('pricing.html', user=current_user)


@views.route('/delete-message', methods=['POST'])
def delete_message():
    message = json.loads(request.data)
    messageId = message['messageId']
    message = Message.query.get(messageId)
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

    return jsonify({})
