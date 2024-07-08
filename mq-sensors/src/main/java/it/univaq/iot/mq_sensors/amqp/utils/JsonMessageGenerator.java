package it.univaq.iot.mq_sensors.amqp.utils;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.concurrent.ThreadLocalRandom;

import org.json.JSONObject;
import org.springframework.stereotype.Component;

import it.univaq.iot.mq_sensors.amqp.dto.JsonMessage;
import it.univaq.iot.mq_sensors.amqp.dto.Location;

@Component
public class JsonMessageGenerator {
	
	private final Double LATITUDE_1 = 42.2309157544403;
	private final Double LONGITUDE_1 = 14.390457587640933;
	
	public JSONObject generateJsonTemperature() {
		
		Location location = new Location(LATITUDE_1, LONGITUDE_1);	
		
		double temp = ThreadLocalRandom.current().nextDouble(-15.0, 40.0);
		BigDecimal decimal = new BigDecimal(temp).setScale(1, RoundingMode.FLOOR);
		
		JsonMessage jsonMessage = new JsonMessage(location, decimal, "°C");
		
		JSONObject json = new JSONObject(jsonMessage);
		
		return json;
		
	}

}
