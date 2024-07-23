package it.univaq.iot.mq_sensors.amqp;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Profile;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class MessagingRabbitmqApplication {
	
	private static final Logger log = LogManager.getLogger(MessagingRabbitmqApplication.class);

    @Profile("usage_message")
    @Bean
    public CommandLineRunner usage() {
        return args -> {
        	log.info("This app uses Spring Profiles to control its behavior.\n");
        	log.info("Sample usage: java -jar rabbit-tutorials.jar "
            		+ "--spring.profiles.active=hello-world,sender");
        };
    }

    @Profile("!usage_message")
    @Bean
    public CommandLineRunner tutorial() {
        return new Runner();
    }

  public static void main(String[] args) {
    SpringApplication.run(MessagingRabbitmqApplication.class, args);
  }

}
