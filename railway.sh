#!/bin/bash
# Railway build script
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate