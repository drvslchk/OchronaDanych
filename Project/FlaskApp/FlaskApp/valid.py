# funkcje odpowiadające za walidacje danych
import re

# sprawdzanie czy hasło spełnia wymogi
# 1 mała litera
# 1 duża
# 1 cyfra
# co najmniej 8 znaków


def passwordValidation(password):
    if not textVallidation(password):
        return False
    pat = re.compile(
        r"(?=(.*[0-9]))((?=.*[A-Za-z0-9])(?=.*[A-Z])(?=.*[a-z]))^.{8,}$")
    if re.fullmatch(pat, password):
        return True
    else:
        return False

# sprawdzanie czy nie ma znaków zagrażających programowi


def textVallidation(text):
    pat = re.compile(r"^[a-zA-Z0-9 ]*$")
    if re.fullmatch(pat, text):
        return True
    else:
        return False

# sprawdzenie czy login spełnia wymogi


def loginVallidation(login):
    pat = re.compile(r"^[a-zA-Z0-9]*$")
    if re.fullmatch(pat, login):
        return True
    else:
        return False

# sprawdzenie czy email spełnia wymogi


def emailVallidation(email):
    pat = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    if re.fullmatch(pat, email):
        return True
    else:
        return False
