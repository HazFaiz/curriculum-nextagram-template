from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template, request, flash
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/', methods=["GET"])
def new():
    return render_template("sessions/new.html")


@sessions_blueprint.route('/new', methods=['POST'])
def sign_in():
    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")
    # passw = User.get_or_none(User.password == login_password)

    user = User.get_or_none(User.email == login_email)
    # check in db if there is a user with the email we typed in in signin form

    checked = check_password_hash(user.password, login_password)

    if not user:  # CHANGE TO == USERID
        flash(f"Email does not exist")
        return redirect(url_for('sessions.new'))
    else:

        if not checked:
            flash(f"Password does not match our records")
            return redirect(url_for('sessions.new'))
        else:
            # session cannot store a whole python object, just the attritbute, so choose between id, name, email, etc
            # SESSION METHOD
            # session["user"] = user.id
            # session["name"] = user.name
            # FLASK METHOD
            login_user(user)
            flash(f"Login sucessful")
            # return redirect(url_for('sessions.new'))
            return redirect(url_for('home'))


@sessions_blueprint.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    flash(f"Logout sucessful")
    return redirect(url_for('sessions.new'))


# -------------------- GOOGLE SIGN IN ROUTES ---------------

@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/google_authorize')
def google_authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)

    if user:
        login_user(user)
        return redirect(url_for('users.index'))
    else:
        return redirect(url_for('sessions.new'))
