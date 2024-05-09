FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE geodjango.settings

RUN apt-get update --fix-missing
RUN apt-get install -y gcc libgeos-dev libcgal-dev libgdal-dev libproj-dev libpq-dev wait-for-it
RUN apt-get install -y postgresql-client

RUN mkdir /climatemq
WORKDIR /climatemq

COPY load_initial_data.sh .
RUN chmod +x load_initial_data.sh

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]