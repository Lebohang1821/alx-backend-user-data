#!/usr/bin/env python3
"""
Authentication module for the API.
"""

import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Handles generic authentication tasks.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path.endswith('*'):
                    pattern = '{}.*'.format(exclusion_path[:-1])
                elif exclusion_path.endswith('/'):
                    pattern = '{}/*'.format(exclusion_path[:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the authorization header, or None if not found.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            User: The current user, or None if not found.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Retrieves the value of the session cookie.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
