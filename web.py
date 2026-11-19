from secrets import token_hex
from flask import Flask, flash, redirect, render_template, request,session
from battle import play, start, starters
from history import read_history, save

def create_app():
    """Connect the game with browser"""
    app = Flask(__name__)
    app.secret_key = token_hex(16)
    @app.route("/", methods = ["GET", "POST"])
    def page():
        """Buttons and screen"""
        if request.method == "POST":
            action = request.form.get("action")
            value = request.form.get("value", "")
            if action in ("menu", "exit"):
                session.clear()
                return redirect("/?show=exit" if action == "exit" else "/")
            try:
                if action == "start":
                    battle = start(value)
                    player, rival = battle["fighters"]
                    message = f"{player['name']} faces {rival['name']}"
                elif action == "attack":
                    battle, message = play(session.get("battle"), value)
                else:
                    raise ValueError("Unknown menu action")
                save (value, message)
                session["battle"] = battle
                flash(message)
            except ValueError as error:
                flash(str(error))
            except (OSError, KeyError, TypeError):
                flash ("Could not load Pokemon data or save the log")
            return redirect("/")
        screen = request.args.get("show")
        log = read_history() if screen == "history" else ""
        return render_template("index.html", starters = starters(), battle = session.get("battle"), screen = screen, log = log)
    return app
