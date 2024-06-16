# Mart Projects

This repository contains a series of projects designed to demonstrate different aspects of building a mart application using various technologies. Each project builds on the previous one, adding new features and integrations. Below is an overview of each project along with instructions for setup and running the applications.

## Projects Overview

### 1. Basic Mart

A simple FastAPI application providing basic endpoints to manage products and orders.

**Key Features:**
- FastAPI for building the API
- PostgreSQL for data persistence

**Setup:**
```sh
cd 1-basic-mart
docker-compose up --build
```

### 2. Mart with PostgreSQL

Extends the basic mart application by integrating PostgreSQL for persistent data storage.

**Key Features:**
- FastAPI
- PostgreSQL for data persistence
- Add some additional route

**Setup:**
```sh
cd 2-mart-fastapi-postgresql
docker-compose up --build
```

### 3. Mart with UUID

Enhances the mart application by using UUIDs for product and order IDs.

**Key Features:**
- FastAPI
- PostgreSQL
- UUIDs for primary keys

**Setup:**
```sh
cd 3-mart-db-uuid
docker-compose up --build
```

### 4. Mart with Kafka

Integrates Apache Kafka for real-time data streaming and event-driven architecture.

**Key Features:**
- FastAPI
- PostgreSQL
- Apache Kafka for messaging

**Setup:**
```sh
cd 4-mart-kafka
docker-compose up --build
```

### 5. Postgres Inside Kafka (JSON)

Demonstrates the use of JSON for message serialization in a Kafka-integrated mart application.

**Key Features:**
- FastAPI
- PostgreSQL
- Apache Kafka
- JSON for message serialization

**Setup:**
```sh
cd 5-postgres-inside-kafka-json
docker-compose up --build
```

### 6. Postgres Inside Kafka (Protobuf)

Adds Protobuf for efficient message serialization and communication between services.

**Key Features:**
- FastAPI
- PostgreSQL
- Apache Kafka
- Protobuf for message serialization

**Setup:**
```sh
cd 6-postgres-inside-kafka-protobuf
docker-compose up --build
```

## Global Setup Instructions

1. Clone the repository:
    ```sh
    git clone https://github.com/iamshoaibxyz/mart-projects.git
    cd mart-projects
    ```

2. Navigate to the desired project directory and follow the setup instructions provided above.

3. Each project has its own `docker-compose` configuration and can be run independently. Make sure Docker is installed and running on your machine.

## Additional Information

Each project directory contains a `README.md` file with more detailed instructions and information about the specific project.

For any issues or questions, please refer to the respective project's README or open an issue on the repository.
