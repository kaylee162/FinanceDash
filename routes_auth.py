from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from extensions import db
from models import User
from forms import RegisterForm, LoginForm

# ✅ Only one blueprint definition
auth_bp = Blueprint("auth", __name__)

# -------------------------
# Register Route
# -------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("auth.login"))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


# -------------------------
# Login Route
# -------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = LoginForm()

    # 👇 Add these debug prints
    print("POST request:", form.is_submitted())
    print("Form valid?", form.validate_on_submit())
    print("Form errors:", form.errors)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print("User found:", user is not None)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


# -------------------------
# Logout Route
# -------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
