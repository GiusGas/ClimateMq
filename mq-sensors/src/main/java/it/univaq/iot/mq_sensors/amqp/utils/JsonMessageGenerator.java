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

import it.univaq.iot.mq_sensors.amqp.Sender;
import it.univaq.iot.mq_sensors.amqp.dto.JsonMessage;
import it.univaq.iot.mq_sensors.amqp.dto.Location;
import it.univaq.iot.mq_sensors.amqp.dto.Station;

@Component
public class JsonMessageGenerator {
	
	private static final Logger log = LogManager.getLogger(JsonMessageGenerator.class);
	
//	private final Double LATITUDE_1 = 42.2309157544403;
//	private final Double LONGITUDE_1 = 14.390457587640933;
//	private final Double LATITUDE_2 = 42.34832633009445;
//	private final Double LONGITUDE_2 = 13.398957331640249;
//	private final Double LATITUDE_3 = 42.36805086696008;
//	private final Double LONGITUDE_3 = 13.365232454087643;
	
//	private final Double LATITUDE_MIN = -90.0;
//	private final Double LONGITUDE_MIN = 0.0;
//	private final Double LATITUDE_MAX = 90.0;
//	private final Double LONGITUDE_MAX = 180.0;
	
	private final Double LATITUDE_MIN = 41.77;
	private final Double LATITUDE_MAX = 42.78;
	private final Double LONGITUDE_MIN = 13.0;
	private final Double LONGITUDE_MAX = 14.8;
	
	private List<Station> stations = new ArrayList<>();
	
	public List<JSONObject> generateJsonTemperature() {
		
		List<JSONObject> jsonTemperatures = new ArrayList<>();
		
		for (Station station : stations) {
			double temp = ThreadLocalRandom.current().nextDouble(-15.0, 40.0);
			BigDecimal decimal = BigDecimal.valueOf(temp).setScale(1, RoundingMode.FLOOR);
			
			JsonMessage jsonMessage = new JsonMessage(station, decimal, "°C");
			
			jsonTemperatures.add(new JSONObject(jsonMessage));
		}
		
		return jsonTemperatures;
		
	}
	
	public List<JSONObject> generateJsonPrecipitation() {
		
		List<JSONObject> jsonPrecipitations = new ArrayList<>();
		
		for (Station station : stations) {
			double prec = ThreadLocalRandom.current().nextDouble(0.0, 100.0);
			BigDecimal decimal = BigDecimal.valueOf(prec).setScale(1, RoundingMode.FLOOR);
			
			JsonMessage jsonMessage = new JsonMessage(station, decimal, "mm");
			
			jsonPrecipitations.add(new JSONObject(jsonMessage));
		}
		
		return jsonPrecipitations;
		
	}
	
	public List<JSONObject> generateJsonStation() {
		
		List<JSONObject> jsonStations = new ArrayList<>();
		
		for (int i = 0; i < 10; i++) {
			double latitude = ThreadLocalRandom.current().nextDouble(LATITUDE_MIN, LATITUDE_MAX);
			double longitude = ThreadLocalRandom.current().nextDouble(LONGITUDE_MIN, LONGITUDE_MAX);
			
			Location location = new Location(latitude, longitude);
			String name = "Station " + (i+1);
			String username = "station" + (i+1);
			String key = "station" + (i+1);
			
			Station jsonStation = new Station(name, username, key, location);
			stations.add(jsonStation);
			
			jsonStations.add(new JSONObject(jsonStation));
		}
		
		return jsonStations;
	}

}
