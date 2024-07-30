#!/bin/bash

wait-for-it postgres:5432 -- python manage.py migrate
python manage.py loaddata ./climatemq/fixtures/dump.json
python manage.py runserver 0.0.0.0:8000 --settings=geodjango.settings
