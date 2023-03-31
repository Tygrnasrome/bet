import sqlite3
from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from . import db

main = Blueprint('main', __name__)
