import os

import pathlib

import requests

from .providers.google import flow
from .providers.azure import azure_auth

import google.auth.transport.requests
from google.oauth2 import id_token


from flask import session, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user, login_user, logout_user

from ..src.base import db
from ..src.user import User, oAuthProviders

from . import auth_bp


def gen_avatar(name):
    name = ''.join(name.split()[:2]).replace(' ', '+')
    return f"https://ui-avatars.com/api/?name={name}&bold=true&background=fcead6&color=885724"


@auth_bp.route("/login/google")
def google_login():
    flow.redirect_uri = url_for("auth.google_callback", _external=True, _scheme='https')

    if current_user is not None and current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for("index"))

    authorization_url, state = flow.authorization_url(
        hd="stu.kau.edu.sa",
        include_granted_scopes='true',
    )

    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/google/callback")
def google_callback():
    if request.args.get("state") != session["state"]:
        abort(401)

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=google.auth.transport.requests.Request(),
        audience=os.environ["GOOGLE_CLIENT_ID"],
    )

    if id_info["email_verified"] == False:
        flash("Email not verified", "danger")
        return redirect(url_for("index"))

    user = User.query.filter(
        (User.google_email == id_info["email"].lower()) |
        (User.id == id_info["sub"])
    ).first()

    if not user:
        user = User(id_=id_info["sub"], name=id_info["name"],
                    google_email=id_info["email"].lower(), profile_pic=id_info["picture"])
        user.main_oauth_provider = oAuthProviders.GOOGLE
        db.session.add(user)
        db.session.commit()

    # if the user exists and has a third-party generated avatar, change it to google's
    if "ui-avatars" in user.profile_pic:
        user.profile_pic = id_info["picture"]
        db.session.commit()

    login_user(user)

    if "next" in request.args:
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for("index"))


@auth_bp.route("/login/azure")
def azure_login():
    if current_user is not None and current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for("index"))

    auth_data = azure_auth.log_in(
        redirect_uri=url_for(
            "auth.azure_callback", _external=True, _scheme='https'),
    )
    return redirect(auth_data['auth_uri'])


@auth_bp.route("/azure/callback")
def azure_callback():
    login_res = azure_auth.complete_log_in(request.args)
    if 'error' in login_res:
        flash(login_res['error_description'], "danger")
        return redirect(url_for("login"))

    # get user data and signup the user to the db
    # User.Read is the least required privilaged premission
    token = azure_auth.get_token_for_user(["User.Read"])
    if "error" in token:
        flash(token['error_description'], "danger")
        return redirect(url_for("login"))

    api_result = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()

    user_openid = azure_auth.get_user()
    google_email = api_result['mail'].lower()
    azure_email = user_openid['preferred_username'].lower()

    user = User.query.filter(
        (User.azure_email == azure_email) |
        (User.google_email == google_email)
    ).first()

    if not user:
        user = User(
            id_=user_openid['sub'],
            name=user_openid['name'],
            google_email=google_email,
            azure_email=azure_email,
            profile_pic=gen_avatar(user_openid['name'])
        )
        user.main_oauth_provider = oAuthProviders.AZURE
        db.session.add(user)
        db.session.commit()

    if not user.azure_email:
        user.azure_email = azure_email
        db.session.commit()

    if not user.profile_pic:
        user.profile_pic = gen_avatar(user_openid['name'])
        db.session.commit()

    login_user(user)

    if "next" in request.args:
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for("index"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("index"))
