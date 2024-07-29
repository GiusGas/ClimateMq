package it.univaq.iot.mq_sensors.amqp.utils;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;
import org.springframework.stereotype.Component;

import it.univaq.iot.mq_sensors.amqp.dto.JsonMessage;
import it.univaq.iot.mq_sensors.amqp.dto.Location;
import it.univaq.iot.mq_sensors.amqp.dto.Station;

@Component
public class JsonMessageGenerator {

    private static final Logger log = LogManager.getLogger(JsonMessageRandomGenerator.class);

    private final Double LATITUDE = 42.36805086696008;
    private final Double LONGITUDE = 13.365232454087643;
    private final String STATION_NAME = "L'Aquila Pettino";
    private final String STATION_USERNAME = "aquilaPettino";
    private final String STATION_KEY = "aquilaPettino";
    private final String VARIABLE_UNIT = "lux";
    private final Double VALUE_MIN = 0.0;
    private final Double VALUE_MAX = 100.0;

    private List<Station> stations = new ArrayList<>();

    public List<JSONObject> generateJsonStation() {

        List<JSONObject> jsonStations = new ArrayList<>();

        Station jsonStation = new Station(STATION_NAME, STATION_USERNAME, STATION_KEY,
                new Location(LATITUDE, LONGITUDE));

        stations.add(jsonStation);

        jsonStations.add(new JSONObject(jsonStation));

        return jsonStations;
    }

    public List<JSONObject> generateJsonLum() {

        List<JSONObject> jsonTemperatures = new ArrayList<>();

        Station station = new Station(STATION_NAME, STATION_USERNAME, STATION_KEY,
                new Location(LATITUDE, LONGITUDE));

        double temp = ThreadLocalRandom.current().nextDouble(VALUE_MIN, VALUE_MAX);
        BigDecimal decimal = BigDecimal.valueOf(temp).setScale(1, RoundingMode.FLOOR);

        JsonMessage jsonMessage = new JsonMessage(station, decimal, VARIABLE_UNIT);

        jsonTemperatures.add(new JSONObject(jsonMessage));

        return jsonTemperatures;

    }

}
