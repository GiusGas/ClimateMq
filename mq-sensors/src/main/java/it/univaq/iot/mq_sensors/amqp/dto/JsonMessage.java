package it.univaq.iot.mq_sensors.amqp.dto;

import java.math.BigDecimal;

public class JsonMessage {

	private Station station;
	
	private BigDecimal detectedData;
	
	private String unit;
	
	public JsonMessage(Station station, BigDecimal detectedData, String unit) {
		this.station = station;
		this.detectedData = detectedData;
		this.unit = unit;
	}

	public Station getStation() {
		return station;
	}

	public void setStation(Station station) {
		this.station = station;
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
