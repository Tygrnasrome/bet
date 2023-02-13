#!/bin/sh

python3 -m flask --app app/__init__.py run --host=0.0.0.0 --port=80
