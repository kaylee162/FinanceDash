from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FloatField,
    SelectField,
    DateField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired
from datetime import date


# -------------------------------
#  Register / Login Forms
# -------------------------------

class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=3, max=100)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[InputRequired(), EqualTo("password")],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    submit = SubmitField("Log In")


# -------------------------------
#  Transaction Form
# -------------------------------

class TransactionForm(FlaskForm):
    type = SelectField(
        "Type",
        choices=[
            ("income", "Income"),
            ("expense", "Expense"),
        ],
        validators=[DataRequired()],
    )

    category = SelectField(
        "Category",
        choices=[
            ("income", "💰 Income"),
            ("food", "☕ Food"),
            ("rent", "🏠 Rent"),
            ("entertainment", "🎉 Entertainment"),
            ("transport", "🚗 Transport"),
            ("shopping", "🛍️ Shopping"),
            ("utilities", "💡 Utilities"),
            ("other", "💵 Other"),
        ],
        validators=[DataRequired()],
    )

    amount = FloatField("Amount ($)", validators=[InputRequired()])
    date = DateField("Date", format="%Y-%m-%d", default=date.today)
    description = TextAreaField("Description")
    submit = SubmitField("Save Transaction")

# -------------------------------
#  Budget Form
# -------------------------------
class BudgetForm(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            ("food", "Food"),
            ("rent", "Rent"),
            ("entertainment", "Entertainment"),
            ("transport", "Transport"),
            ("shopping", "Shopping"),
            ("utilities", "Utilities"),
            ("other", "Other"),
        ],
        validators=[InputRequired()],
    )
    limit = FloatField("Monthly Limit ($)", validators=[InputRequired()])
    submit = SubmitField("Save Budget")
