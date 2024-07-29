package it.univaq.iot.mq_sensors.amqp;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;

import it.univaq.iot.mq_sensors.amqp.utils.JsonMessageRandomGenerator;

public class Sender {

	private static final Logger log = LogManager.getLogger(Sender.class);

	@Autowired
	private RabbitTemplate template;

	@Autowired
	private TopicExchange topic;

	@Autowired
	private JsonMessageRandomGenerator generator;

	@Scheduled(fixedRate = 170000, initialDelay = 10)
	public void sendNewStations() {
		for (JSONObject station : generator.generateRandomJsonStation()) {
			StringBuilder builder = new StringBuilder(station.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "station.new", message);
			log.info(" [x] Sent new station '" + message + "'");
		}
	}

	@Scheduled(fixedRate = 5000, initialDelay = 60000)
	public void sendTemperature1() {
		for (JSONObject temperature : generator.generateJsonTemperature()) {
			StringBuilder builder = new StringBuilder(temperature.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "sensor.detected", message);
			log.info(" [x] Sent temperature '" + message + "'");
		}
	}

	@Scheduled(fixedRate = 5000, initialDelay = 61500)
	public void sendPrecipitation1() {
		for (JSONObject precipitation : generator.generateJsonPrecipitation()) {
			StringBuilder builder = new StringBuilder(precipitation.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "sensor.detected", message);
			log.info(" [x] Sent precipitation '" + message + "'");
		}
	}
}
