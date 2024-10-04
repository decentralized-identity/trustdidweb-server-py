from flask import (
    render_template,
)
from app.routes.main import bp
from app.plugins.tdw import TDWService
from .forms import RegisterIssuerForm

@bp.route("/", methods=["GET", "POST"])
def index():
    form = RegisterIssuerForm()
    if form.submit.data and form.validate():
        TDWService().register_did(form.name.data, form.scope.data)
        return render_template("pages/response.jinja", title='TDW Server Demo')
        

    return render_template("pages/index.jinja", title='TDW Server Demo', form=form)
