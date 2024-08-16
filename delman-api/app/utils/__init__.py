from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.employee import Employee
from flask import jsonify
from flask.json.provider import DefaultJSONProvider
import json
from datetime import date, time, datetime
from pydantic import ValidationError

class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=self.default, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def construct_error_msg(e: ValidationError):
    msg =  str(e.errors()[0]["msg"])
    loc = str(e.errors()[0]["loc"][0])

    return f"{loc}: {msg}"

def get_current_user():
    user_id = get_jwt_identity()
    return Employee.query.get(user_id)

def jwt_and_current_user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                return jsonify({
                    "error": {
                        "code": "auth/user-not-found",
                        "message": "Current user not found"
                    }
                }), 401
            return fn(current_user, *args, **kwargs)
        return decorator
    return wrapper

def success_response(data=None, status_code=200):
    res = {"ok": True}
    if data:
        res["result"] = data
    return jsonify(res), status_code

def error_response(message, code, status_code):
    return jsonify({
        "error": {
            "code": code,
            "message": message
        },
        "ok": False
    }), status_code
