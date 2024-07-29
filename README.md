# IoTMq

## To start-up the system:

- Go to climate-mq folder;
- run on terminal "docker-compose build";
- run on terminal "docker-compose up";
- run "docker-compose exec app python manage.py start_consumer" if you want to start consuming data from rabbitMQ;
- go on browser to http://localhost:8080/climatemq/map/

If you want to access to the admin panel the credentials are:
- username: admin 
- password: admin

## To run the simulated Station and send data to rabbitMQ:

- Run on terminal "docker-compose build spring-app" (Always in the climate-mq folder);
- Run on terminal "docker-compose up spring-app".

If you want to see data stored, remember to accept stations from the Admin Panel (go to the [Administration site](http://localhost:8080/admin/climatemq/station/) 
and modify the new stations checking the "accepted" field).

---

To see other details on the project or how to add a custom station, you can refer to the full [Documentation](ClimateMQ.docx)
