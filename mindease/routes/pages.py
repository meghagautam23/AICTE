from flask import Blueprint, render_template


pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/about")
def about():
    return render_template("about.html")


@pages_bp.route("/resources")
def resources():
    return render_template("resources.html")


@pages_bp.route("/faq")
def faq():
    return render_template("faq.html")
