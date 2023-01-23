# autoryzacja
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from threading import Event

# blacklist
# bazadanych
from database import db, User, Client
# walidacja
from valid import passwordValidation, loginVallidation, emailVallidation


auth = Blueprint('auth', __name__)

# lista zablokowanych ip
ip_ban_list = list()


@auth.route('/login')
def login():
    ip = request.remote_addr
    if ip in ip_ban_list:
        abort(403)
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    ip = request.remote_addr
    if ip in ip_ban_list:
        abort(403)
    # pobranie danych formularza
    login = request.form.get('login')
    password = request.form.get('password')
    Event().wait(2)
    if login == "admin" and password == "Admin123":
        ip_ban_list.append(ip)
    # sprawdzenie ilosci prob logowania
    ip_addr = request.remote_addr
    client = Client.query.filter(Client.ip == ip_addr).first()

    if client:
        client.prob = client.prob + 1
        db.session.commit()
        if client.prob > 20:
            ip_ban_list.append(ip_addr)
    if not client:
        new_ip = Client(ip=ip_addr, prob=1)
        db.session.add(new_ip)
        db.session.commit()

    # walidacja
    if not passwordValidation(password) or not loginVallidation(login):
        flash('Invalid login or password.')
        return redirect(url_for('auth.login'))

    # sprawdzenie poprawności logowania
    user = User.query.filter(User.login == login).first()
    if not user or not user.checkPassword(password):
        flash('Invalid login or password.')
        return redirect(url_for('auth.login'))

    # zalogowanie
    login_user(user)
    client.prob = 1
    db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    ip = request.remote_addr
    if ip in ip_ban_list:
        abort(403)
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    ip = request.remote_addr
    if ip in ip_ban_list:
        abort(403)
    # pobranie danych formularza

    email = request.form.get('email')
    login = request.form.get('name')
    password = request.form.get('password')

    # walidacja
    if not passwordValidation(password):
        flash(
            'Bad password format. 1 lowercase, 1 uppercase, 1 number, at least 8 character')
        return redirect(url_for('auth.login'))
    if not loginVallidation(login):
        flash('Bad login format. Only numbers and letters avaible.')
        return redirect(url_for('auth.login'))
    if not emailVallidation(email):
        flash('Bad email format.')
        return redirect(url_for('auth.login'))

    # sprawdzenie czy użytkownik o podanym emailu lub loginie już istnieje
    user = User.query.filter((User.email == email) |
                             (User.login == login)).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # dodanie użytkownika do bazy danych
    new_user = User(email=email, login=login)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
