#!/usr/bin/env python3
"""User session module for managing user sessions.
"""
from models.base import Base


class UserSession(Base):
    """User session class to represent user's session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
