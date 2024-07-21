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

//	@Profile("receiver")
//	private static class ReceiverConfig {
//
//		@Bean
//		public Tut5Receiver receiver() {
//	 	 	return new Tut5Receiver();
//		}
//
//		@Bean
//		public Queue autoDeleteQueue1() {
//			return new AnonymousQueue();
//		}
//
//		@Bean
//		public Queue autoDeleteQueue2() {
//			return new AnonymousQueue();
//		}
//
//		@Bean
//		public Binding binding1a(TopicExchange topic,
//		    Queue autoDeleteQueue1) {
//			return BindingBuilder.bind(autoDeleteQueue1)
//			    .to(topic)
//			    .with("*.orange.*");
//		}
//
//		@Bean
//		public Binding binding1b(TopicExchange topic,
//		    Queue autoDeleteQueue1) {
//			return BindingBuilder.bind(autoDeleteQueue1)
//			    .to(topic)
//			    .with("*.*.rabbit");
//		}
//
//		@Bean
//		public Binding binding2a(TopicExchange topic,
//		    Queue autoDeleteQueue2) {
//			return BindingBuilder.bind(autoDeleteQueue2)
//			    .to(topic)
//			    .with("lazy.#");
//		}
//
//	}

	@Profile("sender")
	@Bean
	Sender sender() {
		return new Sender();
	}

}
