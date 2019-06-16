from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators



#Form for all API Search Forms
class ApiCallForm(FlaskForm):
	stateAbbreviation = StringField('State', [validators.Length(min=2,max=2)])
	parkCode = StringField("Park Code")
	keyword = StringField("Keyword to Search")
	submit = SubmitField("Enter")
