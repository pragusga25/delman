# Delman Projects

This repository contains two related projects: Delman API and Delman Scheduler.

## Project Overview

1. **Delman API**

   - A REST API for CRUD operations on employee, patient, doctor, and appointment data.
   - Includes login functionality.
   - Located in the `delman-api` directory.

2. **Delman Scheduler**
   - A scheduler that updates vaccine_type and vaccine_count for patient data based on no_ktp every 3 hours.
   - Located in the `delman-scheduler` directory.

## Prerequisites

- Docker and Docker Compose installed on your system

## Important: Before You Begin

Before running the applications, please follow these crucial steps:

1. Read the README files in both project folders:

   - [Delman API README](./delman-api/README.md)
   - [Delman Scheduler README](./delman-scheduler/README.md)

   These README files contain important project-specific information and setup instructions.

2. Create a `credentials.json` file:
   - In the `delman-scheduler` folder, create a file named `credentials.json`.
   - This file should contain the service account credentials for querying BigQuery.
   - If you don't have the credentials, please contact your system administrator or refer to the Google Cloud Console to create a service account with appropriate permissions.

## Quick Start

1. Clone this repository:

   ```
   git clone https://github.com/your-username/delman-projects.git
   cd delman-projects
   ```

2. Adjust the environment variables:

   - Open the existing `.env` file in both `delman-api` and `delman-scheduler` directories.
   - Review and update the values if necessary to match your specific configurations.

3. Ensure you've created the `credentials.json` file in the `delman-scheduler` directory as mentioned in the "Before You Begin" section.

4. Run both projects using Docker Compose:

   ```
   docker-compose up -d
   ```

   This command will start both the API and the scheduler, along with a PostgreSQL database.

5. Access the API at `http://localhost:3000`

## Project-Specific Details

For more detailed information about each project, including how to run unit tests, check coverage, or make modifications, please refer to the README files in their respective directories as mentioned above.

## Stopping the Projects

To stop both projects:

```
docker-compose down
```

To stop the projects and remove all data (including the database volume):

```
docker-compose down -v
```

## Troubleshooting

If you encounter any issues:

1. Ensure you've read and followed the instructions in both project-specific README files.
2. Verify that the `credentials.json` file is correctly set up in the `delman-scheduler` directory.
3. Ensure all environment variables in the `.env` files are correctly set and appropriate for your setup.
4. Check the logs of the services:

   ```
   docker-compose logs api
   docker-compose logs scheduler
   ```

5. Verify that the database is running and accessible to both services.
