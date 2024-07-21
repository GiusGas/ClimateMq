#!/bin/bash

wait-for-it postgres:5432 -- python manage.py runserver 0.0.0.0:8000 --settings=geodjango.settings
#wait-for-it app:8000 -- python manage.py start_consumer --settings=geodjango.settings
