class Config(object):
    # klucz do szyfrowania sesji użytkownika
    SECRET_KEY = 'as345kj34h5kljj34sy'
    # adress do bazy danych
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite'

 # pieprz do haseł
    PEPPER = b'{Qxa-\@j'
