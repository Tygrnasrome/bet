from flask import Blueprint

api = Blueprint('api', __name__)

import json
from flask import Flask, render_template, request, redirect, jsonify
from . import db
