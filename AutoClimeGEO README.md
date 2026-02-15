# AutoClime GEO: Autonomic Weather Monitoring System

This project implements a self-adaptive monitoring system using the **MAPE-K framework**. It features a **Transformer-based ML model** for data validation and an automated control loop managed via **Django** and **RabbitMQ**.

## To Start-up the System

The system is fully containerized. The **Consumer Thread** and **ML Model** load automatically upon the web container's initialization.

1. Navigate to the project root folder.
2. Build the containers:
```bash
docker-compose build

```

3. Launch the environment:
```bash
docker-compose up

```

4. **Automatic Services:** 
* The **RabbitMQ Consumer** starts automatically in a background daemon thread once the Django app is ready.
* The **ML Inference Engine** is triggered automatically every hour via Celery to update sensor goals based on new predictions.

5. Access the **Geographic Dashboard**: [http://localhost:8080/climatemq/map/](http://localhost:8080/climatemq/map/)

### Administrative Access

To manage stations or manually override thresholds:

* **Admin Panel:** [http://localhost:8080/admin/](http://localhost:8080/admin/)
* **Credentials:** `username: admin` | `password: admin`

## To Run the Simulated Stations (Python Managed Resources)

The station simulation is now handled by a Python-based multiprocessing script that mimics the behavior of the **Managed Resources**.

1. **Open a new terminal** (ensure you have the requirements installed locally or run via a dedicated container).
2. Run the simulation script:
```bash
python stations.py [number_of_stations]

```
*(Default is 3 stations if no argument is provided)*.

3. **Accepting New Stations:** For security and data integrity, new stations must be authorized.
* Go to the [Station Administration](http://localhost:8080/admin/climatemq/station/).
* Select the newly appeared stations and check the **"accepted"** field.
* Once accepted, the Autonomic Manager will begin monitoring, analyzing, and sending control signals (e.g. `SCALE_RATE`) to these stations.

## System Features

* **Self-Healing:** 3-Strike policy based on AI variance detection.
* **Self-Optimization:** Dynamic battery-aware sampling rates (`SCALE_RATE`).
* **Self-Configuration:** Automatic neighbor activation during primary sensor failure.

## Project Structure and Component Responsibilities

The implementation follows a modular Django-based architecture, where the logic is decoupled into specific files that handle different phases of the autonomic loop.

### Core Autonomic Logic

* **`analyzer.py`**: Serves as the primary engine for the **Analyze** and **Plan** phases. It implements the **Rule-Based** logic and **Goal** strategies—such as the 3-strike policy and battery-aware scaling—based on variance data received from the AI model.
* **`ml_engine.py`**: Manages the **Knowledge** component of the loop by handling the loading and inference of the **Transformer Machine Learning Model**. It provides the "models" used as **Adaptation Decision Criteria**.
* **`consumer.py`**: Implements the **Monitor** phase. It runs as a background daemon thread to ingest raw telemetry from the RabbitMQ exchange, allowing the system to respond to **Changes in Technical Resources** in real-time.
* **`tasks.py`**: Coordinates **Proactive** adaptation by scheduling periodic Celery tasks. This includes the hourly inference cycle used to refresh the **SensorGoal** knowledge base.

### Data Modeling and Orchestration

* **`models.py`**: Defines the **Technical Resources** (Stations, Sensors) and the **Goals** (SensorGoal) that govern the managed environment.
* **`apps.py`**: Orchestrates the system startup, ensuring the **External** adaptation control thread is launched automatically once the Django application is initialized.
* **`admin.py`**: Facilitates **Changes Caused by the User**, enabling administrators to manually approve stations or set static threshold overrides.

### Management and Interface

* **`management/commands/`**: Contains administrative orchestration scripts:
* **`force_predict.py`**: Allows manual triggering of the **Proactive** inference cycle.
* **`start_consumer.py`**: A utility script for the manual initialization of the monitoring process. In the current version of the system, this is no longer strictly required as the consumer is automatically instantiated by `apps.py` upon server startup, but it remains available for manual debugging of the Monitor phase.


* **`api.py` & `viewsets.py`**: Provide the data interfaces for the external dashboard, reflecting the current state of the application **Level** within the taxonomy.


### MAPE-K Functional Mapping

| Phase | Component | Taxonomy Category |
| --- | --- | --- |
| **Monitor** | `consumer.py` | Reactive Time / Technical Resource Level |
| **Analyze** | `analyzer.py` / `ml_engine.py` | Models & Goals Decision Criteria |
| **Plan** | `analyzer.py` | Rules & Policies Decision Criteria |
| **Execute** | `RabbitMQ Publisher` | Parameter & Structure Technique |
| **Knowledge** | `models.py` / `ml_engine.py` | Centralized Control Approach |


---

For theoretical details on the **MAPE-K implementation** or the **Transformer Model architecture**, please refer to the internal [documentation](AutoClimeGEO.docx).
