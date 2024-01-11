#!/bin/bash
cd django_simple_third_party_jwt_example
python manage.py makemigrations && python manage.py migrate
python manage.py runserver 0.0.0.0:8000