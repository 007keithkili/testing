from flask import Blueprint

api = Blueprint('api', __name__)

from . import views  # noqa: E402,F401
