# Hospital Management API

This project is a Flask-based API for a hospital management system. It provides endpoints for managing employees, doctors, patients, and appointments in a hospital or clinic setting.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- pip

## Project Structure

```
project_structure/
├── .env
├── .gitignore
├── requirements.txt
├── docker-compose.yml
├── gunicorn.conf.py
├── run.py
├── seed.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── employee.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── employee.py
│   │   ├── health.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── employee.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── security.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_employee.py
```

## Setup

1. Clone the repository:

   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

   Note: If you encounter any issues with bcrypt, you may need to install additional system dependencies. On Ubuntu/Debian, you can do this with:

   ```
   sudo apt-get install build-essential libffi-dev python-dev
   ```

   On macOS with Homebrew:

   ```
   brew install openssl
   ```

4. Create a `.env` file in the root directory with the following content:

   ```
   FLASK_APP=run.py
   DATABASE_URL=postgresql://user:password@localhost/hospital_db
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Start the PostgreSQL database using Docker Compose:

   ```
   docker-compose up -d
   ```

6. Initialize the database and run migrations:

   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. Seed the database with an initial admin employee:

   ```
   python seed.py
   ```

   This will create an admin employee with the following credentials:

   - Username: admin
   - Password: admin123

   **Important:** Make sure to change this password after your first login.

## Running the Application

1. For development, you can use the Flask development server:

   ```
   flask run
   ```

   The API will be available at `http://localhost:5000`.

2. For a more production-like environment, use Gunicorn:

   ```
   gunicorn -c gunicorn.conf.py run:app
   ```

   The API will be available at `http://localhost:8000`.

## API Endpoints

- GET /health - Health check endpoint
- POST /auth/login - Login and get access token
- POST /employees - Create a new employee
- GET /employees - Get all employees
- GET /employees/:id - Get an employee by ID
- PUT /employees/:id - Update an employee
- DELETE /employees/:id - Delete an employee

## Running Tests

To run the unit tests:

```
pytest
```

## Stopping the Application

1. Stop the Flask development server or Gunicorn by pressing `Ctrl+C`.

2. Stop and remove the Docker containers:

   ```
   docker-compose down
   ```

   Add `-v` if you want to remove the associated volumes as well:

   ```
   docker-compose down -v
   ```

## Development

- The application uses Flask-Migrate for handling database migrations. After making changes to the models, create a new migration:

  ```
  flask db migrate -m "Description of changes"
  ```

  Then apply the migration:

  ```
  flask db upgrade
  ```

- The `seed.py` script can be modified to add more initial data as needed.

- Environment variables are loaded from the `.env` file. Make sure to update this file with the correct values for your environment.

## Deployment

For production deployment:

1. Use a production-grade database setup instead of the Docker Compose PostgreSQL instance.
2. Set `debug=False` in the Flask application configuration.
3. Use a production WSGI server like Gunicorn behind a reverse proxy like Nginx.
4. Set up proper logging and monitoring.
5. Use environment variables for all sensitive information instead of the `.env` file.

## Security Notes

- The initial admin user created by `seed.py` has a default password. This should be changed immediately after the first login.
- All passwords are hashed before being stored in the database.
- JWT is used for authentication. Make sure to keep your `SECRET_KEY` secure and consider using short-lived tokens in production.
