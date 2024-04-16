from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_restx import abort
from typing_extensions import Union, List


def validate_site(value: Union[str, None], parametres: Union[List[str], None],):
    """Decorator to validate if a parameter starts with a specified value."""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            for n in parametres:
                param_value = request.json.get(n)
                if not param_value:
                    return f(*args, **kwargs)
                if not param_value.startswith(value):
                    abort(400, f"Invalid {n}. It must start with '{value}'.")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def allowed_roles(roles: List[str], optional: bool = False):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional=optional)
            if optional:
                return func(*args, **kwargs)
            claims = get_jwt()
            role = claims.get("role")
            if roles and role and (role in roles):
                return func(*args, **kwargs)
            else:
                abort(
                    403,
                    f"Forbidden. Your role is {role}. Allowed roles are: {', '.join(roles)}."
                )

        return decorator

    return wrapper
