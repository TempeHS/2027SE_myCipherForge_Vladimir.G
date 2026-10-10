"""CipherForge Flask Web Application.

Provides a web interface for the 5-phase encryption algorithm.
"""

from flask import Flask, render_template, request
from engine import encrypt, decrypt

app = Flask(__name__)


@app.route("/")
def index():
    """Display the homepage."""
    return render_template("index.html")


@app.route("/workshop", methods=["GET", "POST"])
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

        # Optional workflow helper:
        # if decrypt button sets use_result=1, decrypt the shown result directly.
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

        # Debug prints
        print("POST form:", dict(request.form))
        print("Action:", action)
        print("Key:", key)
        print("Original repr:", repr(original))

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
