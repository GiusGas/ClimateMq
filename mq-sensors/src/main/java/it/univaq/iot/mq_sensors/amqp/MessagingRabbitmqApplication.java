package it.univaq.iot.mq_sensors.amqp;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Profile;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class MessagingRabbitmqApplication {
	

    @Profile("usage_message")
    @Bean
    public CommandLineRunner usage() {
        return args -> {
            System.out.println("This app uses Spring Profiles to control its behavior.\n");
            System.out.println("Sample usage: java -jar rabbit-tutorials.jar "
            		+ "--spring.profiles.active=hello-world,sender");
        };
    }

    @Profile("!usage_message")
    @Bean
    public CommandLineRunner tutorial() {
        return new Runner();
    }

//  static final String topicExchangeName = "spring-boot-exchange";
//
//  static final String queueName = "spring-boot";
//
//  @Bean
//  Queue queue() {
//    return new Queue(queueName, false);
//  }
//
//  @Bean
//  TopicExchange exchange() {
//    return new TopicExchange(topicExchangeName);
//  }
//
//  @Bean
//  Binding binding(Queue queue, TopicExchange exchange) {
//    return BindingBuilder.bind(queue).to(exchange).with("foo.bar.#");
//  }
//
//  @Bean
//  SimpleMessageListenerContainer container(ConnectionFactory connectionFactory,
//      MessageListenerAdapter listenerAdapter) {
//    SimpleMessageListenerContainer container = new SimpleMessageListenerContainer();
//    container.setConnectionFactory(connectionFactory);
//    container.setQueueNames(queueName);
//    container.setMessageListener(listenerAdapter);
//    return container;
//  }
//
//  @Bean
//  MessageListenerAdapter listenerAdapter(Receiver receiver) {
//    return new MessageListenerAdapter(receiver, "receiveMessage");
//  }

  public static void main(String[] args) throws InterruptedException {
    SpringApplication.run(MessagingRabbitmqApplication.class, args);
  }

}
