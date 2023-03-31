from flask import Blueprint

api = Blueprint('api', __name__)

import json

from flask import Flask, render_template, request, redirect, jsonify
from . import db

# pull data methods and urls



#print(response_API.status_code)
