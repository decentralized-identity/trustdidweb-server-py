from flask_wtf import FlaskForm
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms import (
    StringField,
    SubmitField,
    SelectMultipleField,
)


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class RegisterIssuerForm(FlaskForm):
    name = StringField("Name", render_kw={"value": "Issuer"})
    scope = StringField("Scope", render_kw={"value": "Example"})
    submit = SubmitField("Register")