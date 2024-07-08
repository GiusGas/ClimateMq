package it.univaq.iot.mq_sensors.amqp.dto;

import java.math.BigDecimal;

public class JsonMessage {

	private Location location;
	
	private BigDecimal detectedData;
	
	private String unit;
	
	public JsonMessage(Location location, BigDecimal detectedData, String unit) {
		this.location = location;
		this.detectedData = detectedData;
		this.unit = unit;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

	public BigDecimal getDetectedData() {
		return detectedData;
	}

	public void setDetectedData(BigDecimal detectedData) {
		this.detectedData = detectedData;
	}

	public String getUnit() {
		return unit;
	}

	public void setUnit(String unit) {
		this.unit = unit;
	}

}
