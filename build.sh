#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Seed the database (if applicable)
python manage.py loaddata seed.py

# Collect static files (if needed)
python manage.py collectstatic --noinput