# Mini Hospital Management System

## Overview

This is a mini hospital management system built with Flask. The application manages three main entities: Employee, Doctor, Patient, and Appointment. Employees can log in and perform CRUD operations on doctors, employees, patients, and appointments.

## Features

- Employee authentication
- Management of doctors, employees, patients, and appointments
- CRUD operations for all entities
- Docker support for easy deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.x (for running tests locally)

## Running the Application

The easiest way to run the application is using Docker Compose:

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Run the following command:

```
docker compose up -d
```

The application will start and be available at `http://localhost:3000`.

## API Documentation

You can view the detailed API documentation on Postman:

[Hospital Management System API Documentation](https://documenter.getpostman.com/view/16401831/2sA3s7iofV)

## Initial Login

The application comes with pre-seeded employee data for initial login. You can find these login credentials in the `seed.py` file. Use these credentials to log in for the first time without needing to manually create an employee account.

## Running Tests

To run the tests locally:

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. Run the tests using pytest:

```
pytest
```

## Code Coverage

To check the code coverage:

1. Run the coverage command:

```
coverage run --rcfile=.coveragerc -m unittest discover tests
```

2. Generate the coverage report:

```
coverage report --rcfile=.coveragerc -m --include="app/services/*,app/routes/*"
```

## Project Structure

```
.
├── app/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── __init__.py
├── tests/
├── config.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
├── seed.py
└── README.md
```
