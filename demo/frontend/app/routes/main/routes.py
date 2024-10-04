from flask import (
    current_app,
    render_template,
    url_for,
    redirect,
    session,
    request,
    flash,
    send_file,
)
from app.routes.main import bp
from .forms import RegisterIssuerForm
import requests

@bp.route("/", methods=["GET"])
def index():
    form = RegisterIssuerForm()
    if form.submit.data and form.validate():
        url = form.url.data
        name = form.name.data
        scope = form.scope.data
        description = form.description.data
        
        namespace = scope.replace(" ", "-").lower()
        identifier = name.replace(" ", "-").lower()
        r = requests.get(f'{current_app.config["TDW_SERVER_URL"]}?namespace={namespace}&identifier={identifier}')
        
        
        
    return render_template("pages/index.jinja", title='Dashboard')
