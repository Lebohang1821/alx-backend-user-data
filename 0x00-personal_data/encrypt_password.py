#!/usr/bin/env python3
"""Module for encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """It generates hashed password using bcrypt with random salt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """It verifies if given password matches the hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
