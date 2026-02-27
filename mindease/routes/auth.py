from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from mindease import db
from mindease.models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not full_name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/signup.html")

        if len(password) < 6:
            flash("Password must have at least 6 characters.", "danger")
            return render_template("auth/signup.html")

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return render_template("auth/signup.html")

        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account created successfully.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("auth/login.html")

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user or not existing_user.check_password(password):
            flash("Invalid credentials.", "danger")
            return render_template("auth/login.html")

        login_user(existing_user)
        flash("Welcome back.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
