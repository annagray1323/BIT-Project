from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from . import auth 


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You have now been logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.map'))
            else:
                flash('This password is incorrect, please try again.', category='error')
        else:
            flash('This email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('The email address is already in use.', category='error')
        elif len(email) < 5:
            flash('The email should consist of more than 4 characters.', category='error')
        elif len(first_name) < 3:
            flash('The first name must be greater than 2 character.', category='error')
        elif password1 != password2:
            flash('The passwords provided do not match.', category='error')
        elif len(password1) < 6:
            flash('Your password should be minimum of 5 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has now been created!', category='success')
            return redirect(url_for('views.map'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/map')
@login_required
def map():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('map.html', user=user)






