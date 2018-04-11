from flask import Blueprint

bapp = Blueprint('main', __name__)

from . import views, errors
