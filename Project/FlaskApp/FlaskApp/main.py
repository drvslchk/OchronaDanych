from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from database import User, Note, ConnectorNote
from database import db
from valid import passwordValidation, textVallidation, loginVallidation, emailVallidation
import cryptocode
from auth import ip_ban_list
main = Blueprint('main', __name__)


@main.route('/')
def index():
    ip = request.remote_addr
    if ip in ip_ban_list:
        abort(403)
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    usersData = User.query.all()
    return render_template('profile.html', name=current_user.login, UsersData=usersData)


@main.route('/notes')
@login_required
def notes():
    # Dodanie pobierania notatek użytkownika
    userNotes = Note.query.filter(Note.userID == current_user.login)

    return render_template('noteList.html', userNotes=userNotes)


@main.route('/sharedNotes')
@login_required
def sharedNotes():
    # Dodanie pobierania notatek udostępnionych

    connectedNotes = Note.query.filter(
        (ConnectorNote.userID == current_user.id) & (ConnectorNote.noteID == Note.id))

    return render_template('sharedNotes.html',  connectedNotes=connectedNotes)


@main.route('/publicNotes')
@login_required
def publicNotes():
    # Dodanie pobierania publicznych notatek
    publicNotes = Note.query.filter(
        Note.isPublic & (Note.userID != current_user.login))

    return render_template('publicNotes.html', publicNotes=publicNotes)


@main.route('/notes/new')
@login_required
def addNote():
    return render_template('noteForm.html', name=current_user.login, UserID=current_user.id)


@main.route('/notes/new', methods=['POST'])
@login_required
def addNote_post():
    # Dane Notatki
    userId = current_user.login
    title = request.form.get('title')
    note = request.form.get('note')
    public = True if request.form.get('isPublic') else False
    users = request.form.get('users')
    encrypt = True if request.form.get('isEncrypted') else False
    key = request.form.get('key')

    # walidacja danych formularza

    if not textVallidation(title):
        flash('Bad title format.')
        return redirect(url_for('main.addNote'))
    if not textVallidation(note):
        flash('Bad note format.')
        return redirect(url_for('main.addNote'))
    if public:
        if not textVallidation(users):
            flash('Bad users format.')
            return redirect(url_for('main.addNote'))
    if encrypt:
        if not textVallidation(key):
            flash('Bad key format.')
            return redirect(url_for('main.addNote'))

    allowedUsers = users.split(" ")

    # szyfrowanie notatki
    if encrypt:
        note = cryptocode.encrypt(note, key)

    # Utworzenie nowej notatki
    newNote = Note(
        title=title,
        text=note,
        isPublic=public,
        userID=userId,
        isEncrypted=encrypt,
        key=key
    )

    db.session.add(newNote)
    db.session.commit()

    noteID = Note.query.order_by(Note.id.desc()).first()

    for user in allowedUsers:
        _user = user.replace(' ', '')
        userData = User.query.filter(User.login == _user).first()
        if userData:
            connect = ConnectorNote(
                noteID=noteID.id,
                userID=userData.id
            )
            db.session.add(connect)
    db.session.commit()
    return redirect(url_for('main.profile'))
