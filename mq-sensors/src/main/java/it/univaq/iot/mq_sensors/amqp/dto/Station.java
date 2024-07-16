package it.univaq.iot.mq_sensors.amqp.dto;

public class Station {
	
	private String name;
	
	private String password;
	
	private Location location;
	
	public Station(String name, String password, Location location) {
		this.name = name;
		this.password = password;
		this.location = location;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

}
