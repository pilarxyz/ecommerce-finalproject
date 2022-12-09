"""Default configuration

Use env var to override
"""
import os
from os.path import join, dirname, realpath

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# BACKEND_HOST = os.getenv("BACKEND_HOST", "localhost:5000")
UPLOAD_FOLDER = join(dirname(realpath(__file__)), "static/images")

MODEL_FOLDER = join(dirname(realpath(__file__)), "machine/Model/")
 