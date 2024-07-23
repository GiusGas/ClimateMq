package it.univaq.iot.mq_sensors.amqp;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.ConfigurableApplicationContext;

public class Runner implements CommandLineRunner {

	private static final Logger log = LogManager.getLogger(Runner.class);
	
    @Value("${tutorial.client.duration:0}")
    private int duration;

    @Autowired
    private ConfigurableApplicationContext ctx;

    @Override
    public void run(String... arg0) throws Exception {
        log.info("Ready ... running for " + duration + "ms");
        Thread.sleep(duration);
        ctx.close();
    }

}
