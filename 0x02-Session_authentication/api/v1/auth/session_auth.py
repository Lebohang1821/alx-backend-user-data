#!/usr/bin/env python3
"""Session authentication module for API.
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """It manages session authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """It creates session ID for a user.
        """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """It etrieves user ID associated with session ID.
        """
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """It retrieves user based on session ID in request.
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Destroys authenticated session.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
