package it.univaq.iot.mq_sensors.amqp;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.concurrent.ThreadLocalRandom;

import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;

public class Sender {

	private final String LATITUDE_1 = "42.23";
	private final String LONGITUDE_1 = "14.39";
	@Autowired
	private RabbitTemplate template;

	@Autowired
	private TopicExchange topic;

//	private final String[] keys = {"quick.orange.rabbit", "lazy.orange.elephant", "quick.orange.fox",
//			"lazy.brown.fox", "lazy.pink.rabbit", "quick.brown.fox"};

	@Scheduled(fixedRate = 5000, initialDelay = 500)
	public void sendTemperature1() {
		double temp = ThreadLocalRandom.current().nextDouble(-15.0, 40.0);
		BigDecimal decimal = new BigDecimal(temp).setScale(1, RoundingMode.FLOOR);
		StringBuilder builder = new StringBuilder(decimal.toString());
		String message = builder.toString();
		template.convertAndSend(topic.getName(), "sensor.temperature."+LONGITUDE_1+"."+LATITUDE_1, message);
		System.out.println(" [x] Sent temperature '" + message + "'");
	}

	@Scheduled(fixedRate = 5000, initialDelay = 1500)
	public void sendPrecipitation1() {
		double prec = ThreadLocalRandom.current().nextDouble(0.0, 200.0);
		BigDecimal decimal = new BigDecimal(prec).setScale(1, RoundingMode.FLOOR);
		StringBuilder builder = new StringBuilder(decimal.toString());
		String message = builder.toString();
		template.convertAndSend(topic.getName(), "sensor.precipitation"+LONGITUDE_1+"."+LATITUDE_1, message);
		System.out.println(" [x] Sent precipitation '" + message + "'");
	}
}
