# python
import logging
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

def success_response(message="Success", data=None, status=200):
    return JSONResponse(
        status_code=status,
        content={
            "ok": True,
            "code": status,
            "message": message,
            "data": data or {}
        }
    )

def error_response(message="Something went wrong", status=500, data=None):
    logger.error(f"[{status}] {message}")
    return JSONResponse(
        status_code=status,
        content={
            "ok": False,
            "code": status,
            "message": message,
            "data": data or {}
        }
    )

def not_found_response(message="Resource not found"):
    return error_response(message, 404)

def bad_request_response(message="Bad request"):
    return error_response(message, 400)

def unauthorized_response(message="Unauthorized"):
    return error_response(message, 401)

def conflict_response(message="Conflict"):
    return error_response(message, 409)