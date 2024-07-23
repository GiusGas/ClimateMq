# IoTMq

## To start-up the system:

- Go to climate-mq folder;
- run on terminal "docker-compose build";
- run on terminal "docker-compose up";
- run "docker-compose exec app ./load_initial_data.sh";
- run "docker-compose exec app python manage.py start_consumer" if you want to start consuming data from rabbitMQ;
- go on browser to http://localhost:8080/climatemq/map/

If you want to access to the admin panel the credentials are:
- username: admin 
- password: admin
