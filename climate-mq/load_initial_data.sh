#!/bin/bash

python manage.py migrate
python manage.py loaddata ./climatemq/fixtures/dump.json