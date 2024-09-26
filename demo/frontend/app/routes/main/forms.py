from flask_wtf import FlaskForm
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField,
    SelectMultipleField,
)


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class RegisterIssuerForm(FlaskForm):
    name = StringField("Name", render_kw={"value": "Director of Petroleum Lands"})
    description = TextAreaField("Description", render_kw={"value": "An officer or employee of the ministry who is designated as the Director of Petroleum Lands by the minister."})
    url = StringField("Url", render_kw={"value": "https://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure"})
    namespace = StringField("Namespace", render_kw={"value": "petroleum-and-natural-gas-act"})
    identifier = StringField("Identifier", render_kw={"value": "director-of-petroleum-lands"})
    submit = SubmitField("Register")


class RegisterCredentialForm(FlaskForm):
    type = StringField("Type", render_kw={"value": "BCPetroleumAndNaturalGasTitle"})
    extra_type = SelectField("Extra Type")
    name = StringField("Name", render_kw={"value": "B.C. Petroleum & Natural Gas Title - DRAFT"})
    version = StringField("Version", render_kw={"value": "draft"})
    description = TextAreaField("Description", render_kw={"value": "The majority of subsurface petroleum and natural gas (PNG) resources in British Columbia (B.C.) are owned by the Province. By entering into a tenure agreement with the Province, private industry can develop these resources. Tenure agreements are the mechanism used by the Province to give rights to petroleum and natural gas resources through issuance of Petroleum and Natural Gas Titles."})
    issuer = SelectField("Issuer")
    oca = StringField("OCABundle", render_kw={"value": "https://"})
    governance = StringField("Governance", render_kw={"value": "https://bcgov.github.io/digital-trust-toolkit/docs/governance/pilots/bc-petroleum-and-natural-gas-title/governance"})
    vocabulary = StringField("Vocabulary", render_kw={"value": "https://bcgov.github.io/digital-trust-toolkit/docs/governance/pilots/bc-petroleum-and-natural-gas-title/vocabulary"})
    act = StringField("Legal Act", render_kw={"value": "https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/00_96361_01"})
    context = StringField("Context", render_kw={"value": "https://bcgov.github.io/digital-trust-toolkit/assets/files/context-d241f8fc331c518b484556afe9e6fb71.jsonld"})
    schema = StringField("Json Schema", render_kw={"value": "https://"})
    submit = SubmitField("Register")


class IssueCredentialForm(FlaskForm):
    type = SelectField("Type")
    entity_id = StringField("Registration Number", render_kw={"value": "A0131571"})
    title_no = StringField("Title Number", render_kw={"value": "745"})
    submit = SubmitField("Issue")


class ViewCredentialForm(FlaskForm):
    credential_id = StringField("Credential Id")
    submit = SubmitField("View")