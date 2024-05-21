#!/usr/bin/env python3
"""Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """It GET /api/v1/status
    Returns:
      - Status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """It GET /api/v1/stats
    Returns:
    Number of each object type
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """It GET /api/v1/unauthorized
    Returns:
    401 Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """GET /api/v1/forbidden
    Returns:
    403 Forbidden error
    """
    abort(403)
