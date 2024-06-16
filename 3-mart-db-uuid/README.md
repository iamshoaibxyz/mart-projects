
---

# Mart FastAPI with UUIDs and PostgreSQL

Welcome to the Mart FastAPI project! This project is a RESTful API built using FastAPI, SQLModel, and PostgreSQL, featuring UUIDs as primary keys for better scalability and uniqueness. It manages products in a mart and includes features such as creating orders and retrieving order details.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [GET /get-all-products](#get-get-all-products)
  - [GET /get-products-by-category/{product_category}](#get-get-products-by-categoryproduct_category)
  - [GET /get-product/{product_id}](#get-get-productproduct_id)
  - [POST /add-product](#post-add-product)
  - [PATCH /increment-product-item/{product_id}](#patch-increment-product-itemproduct_id)
  - [PATCH /update-product/{product_id}](#patch-update-productproduct_id)
  - [POST /order/](#post-order)
  - [GET /get-orders](#get-get-orders)
- [Project Structure](#project-structure)
- [Docker](#docker)
- [Contributing](#contributing)

## Overview

Mart FastAPI with UUIDs and PostgreSQL is a web service for managing a product catalog and creating orders. It includes features for retrieving, adding, and updating products as well as placing and viewing orders, with UUIDs used for unique identifiers.

## Features

- Retrieve all products
- Filter products by category
- Get details of a single product
- Add new products
- Update existing products
- Increment product quantity
- Place an order
- Retrieve all orders

## Setup

### Requirements

- Docker
- Docker Compose

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/iamshoaibxyz/mart-projects.git
    cd 3-mart-db-uuid
    ```

### Running the Project

1. **Build and start the containers:**

    ```sh
    docker-compose up --build
    ```

2. **Access the API:**
   Open your browser and navigate to `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### GET /

Returns a welcome message.

- **URL:** `/`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "Message": "Mart API Sourcecode"
  }
  ```

### GET /get-all-products

Retrieves all products in the mart.

- **URL:** `/get-all-products`
- **Method:** `GET`
- **Response:** `200 OK` with a JSON array of products.

### GET /get-products-by-category/{product_category}

Retrieves products filtered by category.

- **URL:** `/get-products-by-category/{product_category}`
- **Method:** `GET`
- **Path Parameters:**
  - `product_category` (string): The category of the products.
- **Response:** `200 OK` with a JSON array of products.

### GET /get-product/{product_id}

Retrieves a single product by its ID.

- **URL:** `/get-product/{product_id}`
- **Method:** `GET`
- **Path Parameters:**
  - `product_id` (UUID): The ID of the product.
- **Response:** `200 OK` with a JSON object of the product.

### POST /add-product

Adds a new product to the mart.

- **URL:** `/add-product`
- **Method:** `POST`
- **Request Body:**
  - `name` (string): The name of the product.
  - `category` (string): The category of the product.
  - `price` (int): The price of the product.
  - `quantity` (int): The quantity of the product.
- **Response:** `201 Created` with a JSON object of the newly created product.

### PATCH /increment-product-item/{product_id}

Increments the quantity of a product.

- **URL:** `/increment-product-item/{product_id}`
- **Method:** `PATCH`
- **Path Parameters:**
  - `product_id` (UUID): The ID of the product.
- **Request Body:**
  - `add_item` (int): The number of items to add to the product's quantity.
- **Response:** `200 OK` with a JSON object of the updated product.

### PATCH /update-product/{product_id}

Updates the details of a product.

- **URL:** `/update-product/{product_id}`
- **Method:** `PATCH`
- **Path Parameters:**
  - `product_id` (UUID): The ID of the product.
- **Request Body:**
  - `name` (string, optional): The name of the product.
  - `category` (string, optional): The category of the product.
  - `price` (int, optional): The price of the product.
  - `quantity` (int, optional): The quantity of the product.
- **Response:** `200 OK` with a JSON object of the updated product.

### POST /order/

Places an order for a product.

- **URL:** `/order/`
- **Method:** `POST`
- **Request Body:**
  - `product_id` (UUID): The ID of the product.
  - `quantity` (int): The quantity to order.
- **Response:** `201 Created` with a JSON object of the newly created order.

### GET /get-orders

Retrieves all orders.

- **URL:** `/get-orders`
- **Method:** `GET`
- **Response:** `200 OK` with a JSON array of orders.

## Project Structure

```
mart-fastapi-uuid-postgresql/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schema.py
│   ├── setting.py
│
├── Dockerfile
├── pyproject.toml
├── README.md
└── .env
```

## Docker

This project uses Docker for containerization and Docker Compose for orchestration. The `docker-compose.yml` file sets up the API, PostgreSQL database, and network configuration.

### Building and Running the Containers

To build and run the containers, use the following command:

```sh
docker-compose up --build
```

This will start the API service on `http://127.0.0.1:8000` and the PostgreSQL database on port `5432`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

---

Feel free to further customize the `README.md` to fit your project and any additional details you want to include.