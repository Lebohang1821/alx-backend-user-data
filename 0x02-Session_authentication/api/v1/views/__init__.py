#!/usr/bin/env python3
"""Blueprint for API routes.
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

# Load users from file when the blueprint is initialized.
User.load_from_file()

from api.v1.views.session_auth import *
