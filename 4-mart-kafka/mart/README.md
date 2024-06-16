# Basic Mart with Kafka Integration

This project, **Basic Mart with Kafka Integration**, demonstrates a FastAPI application integrated with Kafka for asynchronous messaging and PostgreSQL for database management. The application allows for product and order management with real-time data processing through Kafka.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Docker Setup](#docker-setup)
- [Kafka Setup](#kafka-setup)

## Features

- **Product Management**: Add, update, and retrieve products.
- **Order Management**: Place orders and retrieve order details.
- **Kafka Integration**: Asynchronous message processing for products and orders.
- **PostgreSQL Integration**: Persistent data storage.
- **Dockerized Environment**: Easy setup and deployment using Docker and Docker Compose.

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/iamshoaibxyz/mart-projects.git
   cd 4-mart-kafka
   ```

## Usage

### Running the Application

1. **Start Docker Containers**
   ```sh
   docker-compose up --build
   ```

2. **Access the API:**
   Open your browser and navigate to `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

3. **Kafka UI**
   Kafka UI can be accessed at `http://127.0.0.1:8080` for monitoring Kafka topics and messages.

## API Endpoints

### Root Endpoint

- `GET /`: Returns a welcome message.

### Product Endpoints

- `GET /get-all-products`: Retrieve all products.
- `GET /get-products-by-category/{product_category}`: Retrieve products by category.
- `GET /get-product/{product_id}`: Retrieve a specific product by ID.
- `POST /add-product`: Add a new product.
- `PATCH /increment_product_item/{product_id}`: Increment product quantity.
- `PATCH /update_product/{product_id}`: Update product details.

### Order Endpoints

- `POST /order`: Place a new order.
- `GET /get_orders`: Retrieve all orders.

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string.

### Kafka Configuration

Kafka settings are configured in the `docker-compose.yml` file. Key configurations include:

- `KAFKA_ADVERTISED_LISTENERS`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS`

## Docker Setup

### Dockerfile

The Dockerfile sets up the application environment, installs dependencies using Poetry, and exposes port 8000.

### Docker Compose

The `docker-compose.yml` file configures the following services:

- **API Service**: Runs the FastAPI application.
- **PostgreSQL Service**: Database service for storing products and orders.
- **Kafka Broker Service**: Kafka message broker.
- **Kafka UI Service**: Web UI for monitoring Kafka.

## Kafka Setup

The application uses `AIOKafkaProducer` and `AIOKafkaConsumer` for Kafka integration:

- **Producer**: Sends messages to Kafka topics (`mart-product-topic`, `mart-order-topic`).
- **Consumer**: Listens to Kafka topics and processes messages asynchronously.

### Kafka Topics

- `mart-product-topic`: Handles messages related to product management.
- `mart-order-topic`: Handles messages related to order management.

### Starting Kafka Consumers

Kafka consumers are started as asynchronous tasks in the `lifespan` context manager of the FastAPI application:

```python
asyncio.create_task(kafka_consumer("mart-order-topic", "broker:19092"))
asyncio.create_task(kafka_consumer("mart-product-topic", "broker:19092"))
```

## Conclusion

This project showcases a complete setup of a FastAPI application integrated with Kafka and PostgreSQL, running in a Dockerized environment. The architecture is designed for scalability and real-time data processing, making it suitable for a wide range of applications. Feel free to explore the code and adapt it to your needs.