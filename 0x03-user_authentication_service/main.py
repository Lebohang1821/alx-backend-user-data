#!/usr/bin/env python3
"""End-to-end integration tests for `app.py`."""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration."""
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect password."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test profile retrieval when logged out."""
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile retrieval when logged in."""
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test session logout."""
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """It test password reset token request."""
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """It test password update."""
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
