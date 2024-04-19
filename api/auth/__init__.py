from flask import Blueprint

auth_bp: Blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')

from .login import *