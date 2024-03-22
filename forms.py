from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_ckeditor import CKEditorField

## FormInfo Form
class testForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    content = CKEditorField("What are you trying to do")
    submit = SubmitField("Submit")