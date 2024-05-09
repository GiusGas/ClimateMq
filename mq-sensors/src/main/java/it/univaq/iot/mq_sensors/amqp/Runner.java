package it.univaq.iot.mq_sensors.amqp;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.ConfigurableApplicationContext;

//@Component
public class Runner implements CommandLineRunner {

//  private final RabbitTemplate rabbitTemplate;
//  private final Receiver receiver;
//
//  public Runner(Receiver receiver, RabbitTemplate rabbitTemplate) {
//    this.receiver = receiver;
//    this.rabbitTemplate = rabbitTemplate;
//  }

    @Value("${tutorial.client.duration:0}")
    private int duration;

    @Autowired
    private ConfigurableApplicationContext ctx;

    @Override
    public void run(String... arg0) throws Exception {
        System.out.println("Ready ... running for " + duration + "ms");
        Thread.sleep(duration);
        ctx.close();
    }
    
//  @Override
//  public void run(String... args) throws Exception {
//    System.out.println("Sending message...");
//    rabbitTemplate.convertAndSend(MessagingRabbitmqApplication.topicExchangeName, "foo.bar.baz", "Hello from RabbitMQ!");
//    receiver.getLatch().await(10000, TimeUnit.MILLISECONDS);
//  }

}
