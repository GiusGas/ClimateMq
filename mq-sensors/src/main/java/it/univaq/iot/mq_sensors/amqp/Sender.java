package it.univaq.iot.mq_sensors.amqp;

import org.json.JSONObject;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;

import it.univaq.iot.mq_sensors.amqp.utils.JsonMessageGenerator;

public class Sender {

	@Autowired
	private RabbitTemplate template;

	@Autowired
	private TopicExchange topic;
	
	@Autowired
	private JsonMessageGenerator generator;
	
	@Scheduled(fixedRate = 170000, initialDelay = 10)
	public void sendNewStation() {
		for (JSONObject station : generator.generateJsonStation()) {
			StringBuilder builder = new StringBuilder(station.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "station.new", message);
			System.out.println(" [x] Sent data '" + message + "'");
		}
	}

	@Scheduled(fixedRate = 5000, initialDelay = 60000)
	public void sendTemperature1() {
		for (JSONObject temperature : generator.generateJsonTemperature()) {
			StringBuilder builder = new StringBuilder(temperature.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "sensor.detected", message);
			System.out.println(" [x] Sent temperature '" + message + "'");
		}
	}

	@Scheduled(fixedRate = 5000, initialDelay = 61500)
	public void sendPrecipitation1() {
		for (JSONObject precipitation : generator.generateJsonPrecipitation()) {
			StringBuilder builder = new StringBuilder(precipitation.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "sensor.detected", message);
			System.out.println(" [x] Sent precipitation '" + message + "'");
		}
	}
}
