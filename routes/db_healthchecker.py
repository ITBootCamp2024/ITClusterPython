from flask import Blueprint


db_health = Blueprint('app_file1', __name__)


@db_health.route("/healthchecker")
def healthchecker():
    """
    This is the function for checking connection to the database
    :return: str: database connection status
    """
    return "<h1>DB works normally</h1>"
