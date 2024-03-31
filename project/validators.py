from flask import request
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
