from flask import Blueprint

api = Blueprint('api', __name__)

import json

from flask import Flask, render_template, request, redirect, jsonify
from . import db, response_API

# pull data methods and urls

def Parse():
    data = response_API.text
#print(response_API.status_code)
