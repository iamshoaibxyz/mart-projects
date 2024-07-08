
---

# Basic Mart API

Welcome to the Basic Mart API project! This project is a simple RESTful API for managing products in a mart, built using FastAPI, SQLModel, and PostgreSQL. The API allows you to perform basic CRUD (Create, Read, Update, Delete) operations on the products.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [GET /get-all-products](#get-get-all-products)
  - [GET /get-products-by-category/{product_category}](#get-get-products-by-categoryproduct_category)
  - [GET /get-product/{product_id}](#get-get-productproduct_id)
  - [POST /add-product](#post-add-product)
  - [PATCH /increment-product-item/{product_id}](#patch-increment-product-itemproduct_id)
  - [PATCH /update-product/{product_id}](#patch-update-productproduct_id)
- [Project Structure](#project-structure)
- [Docker](#docker)
- [Contributing](#contributing)

## Overview

Basic Mart API is a web service for managing a catalog of products. It includes features such as retrieving all products, filtering products by category, getting details of a single product, adding new products, and updating existing products.

## Features

- Retrieve all products
- Filter products by category
- Get details of a single product
- Add new products
- Update existing products
- Increment product quantity

## Setup

### Requirements

- Docker
- Docker Compose

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/iamshoaibxyz/mart-projects.git
    cd 1-basic-mart
    ```

### Running the Project

1. **Build and start the containers:**

    ```sh
    docker-compose up --build
    ```

2. **Access the API:**
   Open your browser and navigate to `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Configuration

The project uses environment variables to configure the database connection. These variables are stored in a `.env` file. Here’s an example of what your `.env` file should look like:

```env
DATABASE_URL="postgresql://shoaib:mypassword@basicMartPostgresCont:5432/mydatabase"
```

The `setting.py` file reads these environment variables and provides them to the application:

```python
from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except:
    config = Config("")

DATABASE_URL = config("DATABASE_URL", Secret)
```

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
  - `product_id` (int): The ID of the product.
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
  - `product_id` (int): The ID of the product.
- **Request Body:**
  - `add_item` (int): The number of items to add to the product's quantity.
- **Response:** `200 OK` with a JSON object of the updated product.

### PATCH /update-product/{product_id}

Updates the details of a product.

- **URL:** `/update-product/{product_id}`
- **Method:** `PATCH`
- **Path Parameters:**
  - `product_id` (int): The ID of the product.
- **Request Body:**
  - `name` (string, optional): The name of the product.
  - `category` (string, optional): The category of the product.
  - `price` (int, optional): The price of the product.
  - `quantity` (int, optional): The quantity of the product.
- **Response:** `200 OK` with a JSON object of the updated product.

## Project Structure

```
basic-mart/
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

Feel free to customize the `README.md` further based on your specific project needs and any additional details you want to include.