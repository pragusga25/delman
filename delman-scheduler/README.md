# BigQuery Scheduler for Patient Data

This project contains a scheduler that pulls data from Google BigQuery every 1 hour and updates the `patient` table in a specified database.

## Prerequisite

- Docker and Docker Compose installed on your system
- Google Cloud Platform account with BigQuery access
- BigQuery service account key (JSON file)

## Setup

1. Clone this repository to your local machine.

2. Create a `credentials.json` file:

   - Go to your Google Cloud Console
   - Navigate to "IAM & Admin" > "Service Accounts"
   - Create a new service account or select an existing one
   - Generate a new JSON key for this service account
   - Save the downloaded JSON file as `credentials.json` in the project root directory

3. Adjust the `.env` file in the project root:

   - Open the existing `.env` file
   - Update the values for `DATABASE_URL` and `BIG_QUERY_TABLE_NAME`:

   ```
   DATABASE_URL=your_database_url_here
   BIG_QUERY_TABLE_NAME=your_bigquery_table_name_here
   ```

   Replace the placeholders with your actual values:

   - `your_database_url_here`: The URL of your database (e.g., "postgresql://username:password@localhost/dbname")
   - `your_bigquery_table_name_here`: The full name of your BigQuery table (e.g., "project.dataset.table")

## File Structure

- `main.py`: The main Python script that handles the scheduling and data update.
- `Dockerfile`: Defines the Docker image for the scheduler.
- `docker-compose.yml`: Defines the services needed to run the scheduler.
- `requirements.txt`: Lists the Python dependencies.
- `credentials.json`: Your BigQuery service account key (you need to create this).
- `.env`: Contains environment variables (already exists, just update the values).

## Running the Scheduler

Before running the scheduler, ensure you have set up the `credentials.json` file and adjusted the `.env` file as described in the Setup section.

To run the scheduler using Docker Compose:

1. Build and start the containers:

   ```
   docker-compose up -d
   ```

2. To view logs:

   ```
   docker-compose logs -f scheduler
   ```

3. To stop the scheduler:

   ```
   docker-compose down
   ```

## Customization

If you need to modify the schedule or the data processing logic, edit the `main.py` file and rebuild the Docker image.

## Environment Variables

The following environment variables are set in your `.env` file:

- `DATABASE_URL`: The URL of your database
- `BIG_QUERY_TABLE_NAME`: The full name of your BigQuery table

Make sure to update these values in the `.env` file before running the scheduler.

## Troubleshooting

If you encounter any issues:

1. Verify that your `credentials.json` file is correct and has the necessary permissions to access the BigQuery table.
2. Check that the values in your `.env` file are correct and updated.
3. Ensure that your database is accessible from the Docker container.
4. Review the logs for any error messages.

## Security Note

The `credentials.json` file contains sensitive information. Ensure it's properly secured and never commit it to version control. Consider using secret management solutions for production deployments.
