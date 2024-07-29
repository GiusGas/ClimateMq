package it.univaq.iot.mq_sensors.amqp;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;

import it.univaq.iot.mq_sensors.amqp.utils.JsonMessageGenerator;

public class FixedSender {

	private static final Logger log = LogManager.getLogger(FixedSender.class);

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
			log.info(" [x] Sent new station '" + message + "'");
		}
	}

	@Scheduled(fixedRate = 5000, initialDelay = 100)
	public void sendLum1() {
		for (JSONObject lum : generator.generateJsonLum()) {
			StringBuilder builder = new StringBuilder(lum.toString());
			String message = builder.toString();
			template.convertAndSend(topic.getName(), "sensor.detected", message);
			log.info(" [x] Sent lum '" + message + "'");
		}
	}
}
