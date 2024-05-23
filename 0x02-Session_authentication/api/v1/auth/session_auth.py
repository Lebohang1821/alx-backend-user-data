#!/usr/bin/env python3
"""
Session authentication module for the API
"""

from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Handles session-based authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates session ID for a given user ID
        
        Args:
            user_id (str): The ID of user to create session for.
        
        Returns:
            str: new session ID
        """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.
        
        Args:
            session_id (str): The session ID to look up.
        
        Returns:
            str: user ID associated with session ID, or None if not found
        """
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Retrieves current user based on the session cookie in request
        
        Args:
            request: Flask request object containing the session cookie
        
        Returns:
            User: User associated with the session, or None if not found
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Invalidates session associated with given request
        
        Args:
            request: Flask request object containing session cookie
        
        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
