#!/bin/bash
python manage.py makemigrations --settings=smartcrm_backend.settings.staging
python manage.py migrate --settings=smartcrm_backend.settings.staging
