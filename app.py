"""
Time tracking – Flask app.

Start:  flask --app app init-db      (creates the database, deletes old data)
        flask --app app run --debug
"""

import sqlite3
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, g

from db import DB_HANDLER

app = Flask(__name__)
app.config["DATABASE"] = "zeiterfassung.sqlite"
app.config["SECRET_KEY"] = "nur-fuer-den-unterricht"  # needed for flash() messages


# ------------------------------------------------------------
# Database: one DB_HANDLER per request
# ------------------------------------------------------------

def get_db() -> DB_HANDLER:
    """Return the DB_HANDLER for the current request (created on first use)."""
    if "db" not in g:
        g.db = DB_HANDLER(app.config["DATABASE"])
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    """Close the database connection automatically at the end of every request."""
    handler = g.pop("db", None)
    if handler is not None:
        handler.close_db_conn()


# ------------------------------------------------------------
# Pages
# ------------------------------------------------------------

@app.route("/")
def startseite():
    return render_template("start.html", sqlite_version=sqlite3.sqlite_version)


# UC1: create a project (boss)
# GET  = show the page
# POST = the form was submitted
@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        # The keys must match name="..." in the HTML form
        number = request.form["project_number"].strip()
        name = request.form["project_name"].strip()

        if not number or not name:
            flash("Bitte Projektnummer und Name ausfüllen.", "fehler")
        else:
            try:
                get_db().add_project(number, name)
                flash(f"Projekt {number} wurde gespeichert.", "ok")
            except sqlite3.IntegrityError:
                # UNIQUE on project_number was violated -> number already exists
                flash(f"Die Projektnummer {number} gibt es schon. Nichts gespeichert.", "fehler")

        # Redirect after POST, so pressing F5 does not submit the form again
        return redirect(url_for("projects"))

    # GET: load all projects and pass them to the template as "projects"
    return render_template("projects.html", projects=get_db().get_all_projects())


# ------------------------------------------------------------
# Command line
# ------------------------------------------------------------

STARTING_PROJECTS = [
    ("1", "Hourly"),
    ("2", "Testing"),
    ("3", "Documentation"),
]


@app.cli.command("init-db")
def init_db():
    """Delete the database and create it again with the starting projects."""
    path = Path(app.config["DATABASE"])
    path.unlink(missing_ok=True)        # delete the old database file, if there is one
    handler = DB_HANDLER(str(path))     # creates the empty tables
    for number, name in STARTING_PROJECTS:
        handler.add_project(number, name)
    handler.close_db_conn()
    print("Datenbank angelegt.")