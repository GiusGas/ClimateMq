package it.univaq.iot.mq_sensors.amqp;

import org.springframework.amqp.core.TopicExchange;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Profile({"topics"})
@Configuration
public class Config {

	@Bean
	TopicExchange topic() {
		return new TopicExchange("data");
	}

	@Profile("sender")
	@Bean
	Sender sender() {
		return new Sender();
	}

}
