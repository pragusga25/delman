from app.models.employee import Employee

class EmployeeRepository:
    def __init__(self, db):
        self.db = db

    def create(self, employee_data):
        employee = Employee(**employee_data)
        self.db.session.add(employee)
        self.db.session.commit()
        return employee

    def get_all(self):
        return Employee.query.all()

    def get_by_id(self, id):
        return Employee.query.get(id)

    def update(self, id, employee_data):
        employee = self.get_by_id(id)
        if employee:
            for key, value in employee_data.items():
                setattr(employee, key, value)
            self.db.session.commit()
        return employee

    def delete(self, id):
        employee = self.get_by_id(id)
        if employee:
            self.db.session.delete(employee)
            self.db.session.commit()
            return True
        return False
    
    
    def get_by_username(self, username):
        return Employee.query.filter_by(username=username).first()
