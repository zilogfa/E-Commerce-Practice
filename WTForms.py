from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField

class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    body = CKEditorField('Body', validators=[DataRequired()])
    pic = FileField('Post Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])], render_kw={'class': ''})
    submit = SubmitField('Add Product')