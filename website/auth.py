from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        twitter_tag = request.form.get('twitter_tag')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(twitter_tag) == 0:
            flash('Invalid Twitter name.', category='error')
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            flash('Account created!', category='success')

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<h1>logout</h1>"
