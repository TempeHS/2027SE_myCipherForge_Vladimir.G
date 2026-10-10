"""CipherForge Flask web application.

Provides registration, login, logout, and the encryption workshop.
"""

import os
from functools import wraps

from flask import Flask, render_template, request, session, redirect, url_for

from database import init_db, register_user, verify_user
from engine import encrypt, decrypt

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

init_db()


def login_required(view_func):
    """Require a logged-in session for protected routes."""

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    """Display the home page."""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if len(username) < 3:
            return render_template(
                "register.html", error="Username must be at least 3 characters"
            )

        if len(password) < 8:
            return render_template(
                "register.html", error="Password must be at least 8 characters"
            )

        if password != confirm:
            return render_template("register.html", error="Passwords do not match")

        if register_user(username, password):
            return redirect(url_for("login"))

        return render_template("register.html", error="Username already exists")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if verify_user(username, password):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("workshop"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out the current user."""
    session.clear()
    return redirect(url_for("index"))


@app.route("/workshop", methods=["GET", "POST"])
@login_required
def workshop():
    """Handle encrypt/decrypt workshop form."""
    result = ""
    original = ""

    default_key = {
        "shift": 5,
        "block_size": 4,
        "password": "SECRET",
        "noise_interval": 3,
        "noise_char": "~",
    }
    key = default_key.copy()

    if request.method == "POST":
        action = request.form.get("action", "").strip().lower()
        message = request.form.get("message", "")
        result_input = request.form.get("result_input", "")
        use_result = request.form.get("use_result", "0") == "1"

        # If decrypt is clicked with use_result=1, decrypt the previous result.
        original = (
            result_input
            if action == "decrypt" and use_result and result_input
            else message
        )

        try:
            noise_char_raw = (
                request.form.get("noise_char", default_key["noise_char"])
                or default_key["noise_char"]
            )
            key = {
                "shift": int(request.form.get("shift", default_key["shift"])),
                "block_size": int(
                    request.form.get("block_size", default_key["block_size"])
                ),
                "password": request.form.get("password", default_key["password"])
                or default_key["password"],
                "noise_interval": int(
                    request.form.get("noise_interval", default_key["noise_interval"])
                ),
                "noise_char": noise_char_raw[0],
            }
        except (ValueError, TypeError, IndexError):
            result = "Invalid key values. Please check your inputs."

        if not result:
            if action == "encrypt":
                result = encrypt(original, key)
            elif action == "decrypt":
                result = decrypt(original, key)
            else:
                result = "Please click Encrypt or Decrypt."

    return render_template(
        "workshop.html",
        result=result,
        original=original,
        key_values=key,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
