from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required, Length
from wtforms import ValidationError

class AddBook(Form):
    title = StringField('Book title', validators=[Required(), Length(min=1, max=120)])
    author = StringField("Author's name(s)", validators=[Required()], description="Use ',' as delimiter")
    submit = SubmitField('Add book!')

class EditBook(Form):
    title = StringField('Book title', validators=[Required(), Length(min=1, max=120)])
    author = StringField("Author's name(s)", validators=[Required()], description="Use ',' as delimiter")
    submit = SubmitField('Edit book!')

class RemoveBook(Form):
    title = StringField('Book title', validators=[Required()], description="Please do not delete data in the field")
    author = StringField("Author's name(s)", validators=[Required()], description="Please do not delete data in the field")
    submit = SubmitField('Remove book!')

class AddAuthor(Form):
    name = StringField("Author's name", validators=[Required(), Length(min=1, max=50)], description="Enter only one name!")
    submit = SubmitField('Add author!')

class EditAuthor(Form):
    name = StringField("Author's name", validators=[Required(), Length(min=1, max=50)])
    submit = SubmitField('Edit author!')

class RemoveAuthor(Form):
    name = StringField("Author's name", validators=[Required()], description="Please do not delete data in the field")
    submit = SubmitField('Remove author!')

class Search(Form):
    pattern = StringField('Search', validators=[Required()])
    submit = SubmitField('Go')
