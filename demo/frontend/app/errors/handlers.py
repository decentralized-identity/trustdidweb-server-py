from flask import render_template, current_app, url_for
from werkzeug.exceptions import HTTPException
from app.errors import bp
import traceback
import uuid


@bp.app_errorhandler(HTTPException)
def handle_http_exception(error):
    print(str(error))
    error = {
        # "code": error.code,
        # "name": error.name,
        # "description": error.description,
    }
    return render_template(
        "pages/error/index.jinja",
        title='Error',
        error=error
    )


@bp.app_errorhandler(Exception)
def handle_exception(error):
    print(str(error))
    error = {
        # "code": error.code,
        # "name": error.name,
        # "description": error.description,
    }
    return render_template(
        "pages/error/index.jinja",
        title='Error',
        error=error
    )