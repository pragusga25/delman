import sys
from app import create_app, db
from app.models.employee import Employee
from app.models.doctor import Doctor
from app.models.gender import Gender
from werkzeug.security import generate_password_hash
from datetime import date, time

def seed_data():
    app = create_app()
    with app.app_context():
        # Check if we already have employees
        if Employee.query.first() is None:
            print("Seeding employees...")
            employees = [
                Employee(
                    name="John Doe",
                    username="johndoe",
                    password=generate_password_hash("password123"),
                    gender=Gender.MALE,
                    birthdate=date(1990, 1, 1)
                ),
                Employee(
                    name="Jane Smith",
                    username="janesmith",
                    password=generate_password_hash("password456"),
                    gender=Gender.FEMALE,
                    birthdate=date(1985, 5, 15)
                )
            ]
            db.session.add_all(employees)
        else:
            print("Employees data already exists, skipping...")

        # Check if we already have doctors
        if Doctor.query.first() is None:
            print("Seeding doctors...")
            doctors = [
                Doctor(
                    name="Dr. Alice Johnson",
                    username="dralice",
                    password=generate_password_hash("doctorpass123"),
                    gender=Gender.FEMALE,
                    birthdate=date(1980, 3, 20),
                    work_start_time=time(9, 0),
                    work_end_time=time(17, 0)
                ),
                Doctor(
                    name="Dr. Bob Williams",
                    username="drbob",
                    password=generate_password_hash("doctorpass456"),
                    gender=Gender.MALE,
                    birthdate=date(1975, 7, 10),
                    work_start_time=time(10, 0),
                    work_end_time=time(18, 0)
                )
            ]
            db.session.add_all(doctors)
        else:
            print("Doctors data already exists, skipping...")

        db.session.commit()
        print("Database seeding completed.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        seed_data()
    else:
        print("Run with --check to perform database seeding.")
