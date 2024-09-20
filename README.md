# Scalable Tracking Number Generator API

## Overview

This project implements a RESTful API for generating unique tracking numbers for parcels. The API is built using Django and Django REST Framework and follows best practices for scalability and efficiency.

## Setup
Prerequisites
Ensure you have the following installed:

Python 3.x
pip
Virtual environment (optional, but recommended)

## Clone the repository

<!-- git clone https://github.com/kemburuchandramouli/tracking-number-generator.git -->
https://github.com/kemburuchandramouli/Valuelab_parcel_tracking.git
cd tracking-number-generator

## Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install dependencies
pip install -r requirements.txt

## Apply migrations
python manage.py migrate

## Run the development server
python manage.py runserver

## Access the API
http://127.0.0.1:8000/api/next-tracking-number/


## 1. Generate Next Tracking Number

- **Endpoint**: `GET /api/next-tracking-number/`
- **Query Parameters**:
  - `origin_country_id`: (string) Origin country code in ISO 3166-1 alpha-2 format (e.g., "MY").
  - `destination_country_id`: (string) Destination country code in ISO 3166-1 alpha-2 format (e.g., "ID").
  - `weight`: (decimal) Order weight in kilograms, up to three decimal places (e.g., "1.234").
  - `created_at`: (string) Order creation timestamp in RFC 3339 format (e.g., "2018-11-20T19:29:32+08:00").
  - `customer_id`: (UUID) Customer's UUID (e.g., "de619854-b59b-425e-9db4-943979e1bd49").
  - `customer_name`: (string) Customer's name (e.g., "RedBox Logistics").
  - `customer_slug`: (string) Customer's name in slug-case/kebab-case (e.g., "redbox-logistics").

- **Response Structure**:
  ```json
  {
    "tracking_number": "ABCD1234EFGH5678",
    "created_at": "2023-09-20T19:29:32+08:00",
  }

- **Running Tests Section**: Added instructions for running tests with the `python manage.py test tracking` command.

## Features

- Generate unique tracking numbers comparing in db
- Validate input parameters
- Secure endpoint using JWT authentication # yet to implement
- Support for high concurrency # need to finetune


