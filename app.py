"""
Zeiterfassung – Flask-App.

Starten:   flask --app app init-db      (Datenbank anlegen, löscht alte Daten)
           flask --app app run --debug
"""

from flask import Flask, render_template, request

import db

app = Flask(__name__)
app.config["DATABASE"] = "zeiterfassung.sqlite"
app.config["SECRET_KEY"] = "nur-fuer-den-unterricht"  # für Login-Sessions und flash()-Meldungen
app.teardown_appcontext(db.schliessen)


@app.route("/")
def startseite():
    return render_template("start.html", sqlite_version=db.sqlite_version())

@app.route("/test", methods=["GET", "POST"])
def testseite():
    ergebnis = None
    
    # Prüfen, ob der Nutzer ein Formular abgeschickt hat (POST)
    if request.method == "POST":
        # Den Wert aus dem HTML-Eingabefeld abfangen
        eingabe = request.form.get("benutzer_text")
        
        if eingabe: # Sicherstellen, dass nicht leer abgesendet wurde
            ergebnis = f"Hallo {eingabe.upper()}! Dein Name hat {len(eingabe)} Buchstaben."

    # Egal ob GET (Seite aufgerufen) oder POST (Formular gesendet): Seite rendern
    return render_template("test.html", sqlite_version=db.sqlite_version(), ergebnis=ergebnis)

    


@app.cli.command("init-db")
def init_db():
    """Legt die Datenbank aus schema.sql neu an."""
    db.tabellen_anlegen()
    print("Datenbank angelegt.")
