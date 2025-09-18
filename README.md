# E-commerce API

A **FastAPI-based E-commerce API** built with PostgreSQL and async SQLAlchemy. This API supports user authentication, product management, cart, and orders. Fully deployed on Render.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [API Endpoints](#api-endpoints)
4. [Project Structure](#project-structure)
5. [Technologies Used](#technologies-used)
6. [Live Deployment](#live-deployment)

---

## Project Overview
This is a backend API for an E-commerce application, developed as a job-ready project to demonstrate professional FastAPI skills. It includes:

- User registration & JWT-based authentication
- Role-based access control
- CRUD operations for products
- Cart management and order placement
- Async database queries for better performance
- Deployed to Render with a live PostgreSQL database

---

## Features
- **Users**
  - Register & login
  - JWT authentication
  - Role-based access: Admin/User

- **Products**
  - Create, read, update, delete (Admin only for some)
  - Pagination & search

- **Cart & Orders**
  - Add items to cart
  - Place orders
  - View order history

- **Middleware & Error Handling**
  - Global exception handling

---

## API Endpoints

### Users
- `POST /users/` → Register a new user
- `POST /login/` → Login to get JWT token
- `GET /users/me/` → Get current logged-in user

### Products
- `GET /products/` → List all products
- `GET /products/{id}/` → Get product by ID
- `POST /products/` → Add a new product (Admin only)
- `PUT /products/{id}/` → Update product (Admin only)
- `DELETE /products/{id}/` → Delete product (Admin only)

### Cart & Orders
- `POST /cart/` → Add item to cart
- `GET /cart/` → View cart
- `POST /orders/` → Place order
- `GET /orders/` → View order history

---



---

## Technologies Used
- Python 3.12
- FastAPI
- PostgreSQL
- async SQLAlchemy
- JWT (python-jose)
- passlib[bcrypt]
- Uvicorn
- Render (deployment)

---

## Live Deployment
- **URL:** [https://ecommerce-api-65vh.onrender.com](https://ecommerce-api-65vh.onrender.com)

