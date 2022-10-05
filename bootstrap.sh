#!/bin/sh
export FLASK_APP=./main.py
pipenv run flask run -h 0.0.0.0 
