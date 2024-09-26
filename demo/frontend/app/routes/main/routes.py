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
from .forms import RegisterIssuerForm, RegisterCredentialForm, IssueCredentialForm, ViewCredentialForm





@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/index.jinja", title='Dashboard')


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    register_issuer_form = RegisterIssuerForm()
    issuers = [
        {
            'id': 'did:web:',
            'name': 'Director of Petroleum Lands',
        }
    ]
    register_credential_form = RegisterCredentialForm()
    register_credential_form.issuer.choices = [("", "")] + [
        (issuer['id'], issuer['name']) for issuer in issuers
    ]
    register_credential_form.extra_type.choices = [("", "")] + [
        ("DigitalConformityCredential", "DigitalConformityCredential")
    ]
    issue_credential_form = IssueCredentialForm()
    issue_credential_form.type.choices =  [("", "")] + [
        ("BCPetroleumAndNaturalGasTitle", "BCPetroleumAndNaturalGasTitle")
    ]
    view_credential_form = ViewCredentialForm()
    if register_issuer_form.submit.data and register_issuer_form.validate():
        issuer = {
            'name': register_issuer_form.name.data,
            'description': register_issuer_form.description.data,
            'namespace': register_issuer_form.namespace.data,
            'identifier': register_issuer_form.identifier.data,
            'url': register_issuer_form.url.data,
        }
    if register_credential_form.submit.data and register_credential_form.validate():
        credential_registration = {
            'type': register_credential_form.type.data,
            'extra_type': register_credential_form.extra_type.data,
            'name': register_credential_form.name.data,
            'version': register_credential_form.version.data,
            'description': register_credential_form.description.data,
            'issuer': register_credential_form.issuer.data,
            'oca': register_credential_form.oca.data,
            'governance': register_credential_form.governance.data,
            'vocabulary': register_credential_form.vocabulary.data,
            'act': register_credential_form.act.data,
            'context': register_credential_form.context.data,
            'schema': register_credential_form.schema.data,
        }
    if issue_credential_form.submit.data and issue_credential_form.validate():
        credential_data = {
            'name': issue_credential_form.type.data,
            'description': issue_credential_form.entity_id.data,
            'namespace': issue_credential_form.title_no.data,
        }
    if view_credential_form.submit.data and view_credential_form.validate():
        credential_id = view_credential_form.credential_id.data
    return render_template(
        "pages/main/index.jinja",
        title='Dashboard',
        register_issuer_form=register_issuer_form,
        register_credential_form=register_credential_form,
        issue_credential_form=issue_credential_form,
        view_credential_form=view_credential_form
    )