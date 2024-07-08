# Project 5: Postgres Inside Kafka JSON

## Overview

This project demonstrates the integration of PostgreSQL with Kafka for a basic mart application. The application is built using FastAPI and leverages SQLModel for ORM and asynchronous processing with Kafka to manage products and orders. 

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)

## Features

- **Product Management**: Add, update, and list products.
- **Order Management**: Place orders and list all orders.
- **Kafka Integration**: Asynchronous communication between services using Kafka.
- **PostgreSQL**: Persistent storage of products and orders.
- **Docker**: Containerized application setup using Docker and Docker Compose.

## Setup

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/iamshoaibxyz/mart-projects.git
   cd 5-postgres-inside-kafka-json
   ```

2. **Build and run the containers:**
   ```sh
   docker-compose up --build
   ```

3. **Access the API:**
   Open your browser and navigate to `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

3. **Kafka UI**
   Kafka UI can be accessed at `http://127.0.0.1:8080` for monitoring Kafka topics and messages.

## API Endpoints

### Product Endpoints

- **Add a Product**
  - **POST** `/add-product`
  - Request body: 
    ```json
    {
      "name": "Product Name",
      "category": "Category",
      "price": 100,
      "quantity": 10
    }
    ```

- **Get All Products**
  - **GET** `/get-all-products`

- **Get Products by Category**
  - **GET** `/get-products-by-category/{product_category}`

- **Get Product by ID**
  - **GET** `/get-product/{product_id}`

- **Update Product Quantity**
  - **PATCH** `/increment_product_item/{product_id}`
  - Request body:
    ```json
    {
      "add_item": 5
    }
    ```

- **Update Product**
  - **PATCH** `/update_product/{product_id}`
  - Request body:
    ```json
    {
      "name": "Updated Product Name",
      "category": "Updated Category",
      "price": 150,
      "quantity": 20
    }
    ```

### Order Endpoints

- **Place an Order**
  - **POST** `/order`
  - Request body:
    ```json
    {
      "product_id": "0123456789",
      "quantity": 2
    }
    ```

- **Get All Orders**
  - **GET** `/get_orders`

## Project Structure

```
project-5-postgres-inside-kafka-json/
├── mart/
│   ├── main.py
│   ├── schema.py
│   ├── setting.py
│   ├── Dockerfile
│   ├── .env
├── docker-compose.yaml
```

- **main.py**: The main FastAPI application with endpoints and Kafka consumers.
- **schema.py**: SQLModel schemas for products and orders.
- **setting.py**: Configuration settings for the application.
- **Dockerfile**: Dockerfile for the FastAPI application.
- **docker-compose.yaml**: Docker Compose configuration for setting up the entire application stack.

## Running the Project

To start the project, run:

```sh
docker-compose up --build
```

This command will build and start all the services defined in `docker-compose.yaml`, including the FastAPI application, PostgreSQL database, Kafka broker, and Kafka UI.

## Conclusion

This project demonstrates the integration of FastAPI, PostgreSQL, and Kafka to create a simple mart application. It showcases asynchronous processing, containerization, and the use of modern Python web frameworks and libraries.