from flask import render_template
from werkzeug.exceptions import HTTPException
from app.errors import bp


@bp.app_errorhandler(HTTPException)
def handle_http_exception(error):
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