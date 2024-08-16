import schedule
import time
from google.cloud import bigquery
from google.oauth2 import service_account
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up BigQuery client
credentials_path = os.path.join(os.path.dirname(__file__),  'credentials.json')
credentials = service_account.Credentials.from_service_account_file(
    credentials_path
)
bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Set up SQLAlchemy engine for your database
db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise ValueError("DATABASE_URL environment variable is not set")

bq_table_name = os.getenv('BIG_QUERY_TABLE_NAME')
engine = create_engine(db_url)

def update_patients_data():
    print(f"Updating patient data from BigQuery table {bq_table_name}...")
    # Query BigQuery
    query = f"""
    SELECT vaccine_type, vaccine_count, no_ktp
    FROM `{bq_table_name}`
    """
    query_job = bq_client.query(query)
    results = query_job.result()

    # Update database
    with engine.connect() as connection:
        for row in results:
            update_query = text("""
            UPDATE patient
            SET 
                vaccine_type = :vaccine_type,
                vaccine_count = :vaccine_count
            WHERE no_ktp = :no_ktp
            """)
            connection.execute(update_query, {
                'vaccine_type': row['vaccine_type'],
                'vaccine_count': row['vaccine_count'],
                'no_ktp': row['no_ktp']
            })
        connection.commit()

    print("Patient data updated successfully.")

# Schedule the job to run every 6 hours
schedule.every(1).hours.do(update_patients_data)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
