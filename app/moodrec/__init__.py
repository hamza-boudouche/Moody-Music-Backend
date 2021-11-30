from flask import Blueprint

bp = Blueprint('moodrec', __name__)

from app.moodrec import routes