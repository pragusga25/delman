from app.routes.employee import create_employee_blueprint
from app.routes.auth import create_auth_blueprint
from app.routes.doctor import create_doctor_blueprint
from app.routes.patient import create_patient_blueprint
from app.routes.appointment import create_appointment_blueprint

def register_routes(app, services):
    app.register_blueprint(create_employee_blueprint(services['employee_service']))
    app.register_blueprint(create_auth_blueprint(services['auth_service']))
    app.register_blueprint(create_doctor_blueprint(services['doctor_service']))
    app.register_blueprint(create_patient_blueprint(services['patient_service']))
    app.register_blueprint(create_appointment_blueprint(services['appointment_service']))
