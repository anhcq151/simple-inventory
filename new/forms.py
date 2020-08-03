from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from new.models import ItemName, Item, Location, itemLocation






def get_item_name():
    return ItemName.query

def get_item_loc():
    return Location.query


class NewItemForm(FlaskForm):
    item_name = QuerySelectField('Name', validators=[DataRequired('Select name')], query_factory=get_item_name)
    # serial_number = StringField('Serial Number')
    status = SelectField('Status', validators=[DataRequired()], choices=[('new', 'New'), ('in_used', 'In-Used'), ('out_dated', 'Out-dated')])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    location = QuerySelectField('Location', validators=[DataRequired('Select location')], query_factory=get_item_loc)
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(1, 100)])
    submit = SubmitField('Submit')


class NewNameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewLocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    description = StringField('Location Detail')
    submit = SubmitField('Submit')


class TransferItem(FlaskForm):
    item_name = QuerySelectField('Item Name', validators=[DataRequired('Select name')], query_factory=get_item_name)
    # item_serial = StringField('Item Serial')
    transfer_to = QuerySelectField('Transfer to', validators=[DataRequired('Transfer To')], query_factory=get_item_loc)
    note = TextAreaField('Transfer Note', validators=[Length(min=0, max=400)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(1, 100)])
    submit = SubmitField('Submit')