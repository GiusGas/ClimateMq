package it.univaq.iot.mq_sensors.amqp.dto;

public class Station {
	
	private String name;
	
	private String username;
	
	private String key;
	
	private Location location;
	
	public Station(String name, String username, String key, Location location) {
		this.setName(name);
		this.setUsername(username);
		this.setKey(key);
		this.setLocation(location);
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getKey() {
		return key;
	}

	public void setKey(String key) {
		this.key = key;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

}
