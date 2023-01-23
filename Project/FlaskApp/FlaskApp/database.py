# Bazadanych
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from config import Config
# from notesCrypt import encryptNote

db = SQLAlchemy()

# UserMixin - flask wykorzystuje klase do logowania (niezbedne pola i funkcje)


class Client(db.Model):
    ip = db.Column(db.String(), primary_key=True)
    prob = db.Column(db.Integer)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), index=True, unique=True)
    password = db.Column(db.String())
    salt = db.Column(db.String())
    email = db.Column(db.String(), index=True, unique=True)

    def set_password(self, password):
        # zmiana na bajty
        _password = password.encode()
        _salt = bcrypt.gensalt()
        _hash = bcrypt.hashpw(_password + Config.PEPPER, _salt)
        # zapisanie w bazie
        self.salt = _salt.decode()
        self.password = _hash.decode()

    def checkPassword(self, password):
        _salt = self.salt.encode()
        _password = password.encode()
        _checkedHash = bcrypt.hashpw(_password + Config.PEPPER, _salt)
        return _checkedHash.decode() == self.password

    def __repr__(self):
        return f'{self.login}'


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    isPublic = db.Column(db.Boolean())
    isEncrypted = db.Column(db.Boolean())
    key = db.Column(db.String())
    userID = db.Column(db.String(), db.ForeignKey('user.login'))


class ConnectorNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    noteID = db.Column(db.Integer, db.ForeignKey('note.id'))


def fillDefault():

    user = User(
        login='Test1',
        email='email@test.pl')
    user.set_password('Test1awa')
    db.session.add(user)

    user = User(
        login='Test2',
        email='email2@test.pl')
    user.set_password('Test2kng')
    db.session.add(user)

    note = Note(
        title='Public',
        text='Ta notatka jest ustawiona jako publiczna',
        isPublic=True,
        userID='Test1')
    db.session.add(note)

    note = Note(
        title='Private',
        text='Ta notatka jest ustawiona jako prywanta',
        isPublic=False,
        userID='Test1')
    db.session.add(note)

    note = Note(
        title='Shared',
        text='Ta notatka została udostępniona użytkownika Test1',
        isPublic=False,
        userID='Test2')
    db.session.add(note)
    db.session.commit()

    noteID = Note.query.order_by(Note.id.desc()).first()
    connect = ConnectorNote(
        noteID=noteID.id,
        userID=1
    )
    db.session.add(connect)
    db.session.commit()
