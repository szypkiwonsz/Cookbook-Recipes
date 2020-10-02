from flask_wtf import FlaskForm
from wtforms import StringField, FileField, FieldList, FormField, IntegerField, SelectField, PasswordField
from wtforms.validators import Length, DataRequired


class MyForm(FlaskForm):
    """Class with disabled CSRF token. Used for subforms of FieldList."""

    class Meta:
        csrf = False


class NoLabelMixin(object):
    """Class setting labels in form fields as empty string."""

    def __init__(self, *args, **kwargs):
        super(NoLabelMixin, self).__init__(*args, **kwargs)
        for field_name in self._fields:
            field_property = getattr(self, field_name)
            field_property.label = ''


class FoodAddForm(NoLabelMixin, MyForm):
    # used NoLabelMixin class due to a field and label display error
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])


class IngredientAddForm(MyForm):
    food = FormField(FoodAddForm)
    unit = SelectField('Unit', validators=[DataRequired()], choices=['PIECE', 'GRAM'])
    amount = IntegerField('Amount', validators=[DataRequired()])


class StepAddForm(MyForm):
    instruction = StringField('Instruction', validators=[DataRequired(), Length(min=3, max=500)])


class RecipeAddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    image = FileField('Image', filters=[lambda x: x or "app/media/default.png"])
    description = StringField('Description', validators=[DataRequired(), Length(min=3, max=500)])
    ingredients = FieldList(FormField(IngredientAddForm), min_entries=1)
    steps = FieldList(FormField(StepAddForm), min_entries=1)
    portions = IntegerField('Portions', validators=[DataRequired()])
    preparation_time = IntegerField('Preparation time', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', validators=[DataRequired()], choices=['EASY', 'MEDIUM', 'HARD'])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
