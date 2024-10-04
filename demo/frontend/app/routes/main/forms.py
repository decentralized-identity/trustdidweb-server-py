from flask_wtf import FlaskForm
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectMultipleField,
)


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class RegisterIssuerForm(FlaskForm):
    name = StringField("Name", render_kw={"value": "Director of Petroleum Lands"})
    scope = TextAreaField("Scope", render_kw={"value": "Petroleum and Natural Gas Act"})
    description = TextAreaField("Description", render_kw={"value": "An officer or employee of the ministry who is designated as the Director of Petroleum Lands by the minister."})
    url = StringField("Url", render_kw={"value": "https://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure"})
    submit = SubmitField("Register")