from flask import Flask, render_template, request, redirect, url_for
from db import DB_HANDLER

app = Flask(__name__)
db = DB_HANDLER()



@app.route("/", methods=["GET", "POST"])
def startseite():
    # 1. Wenn das Formular abgeschickt wird (Mitarbeiter klickt "Start")
    if request.method == "POST":
        worker_id = request.form.get("worker_id")
        project_id = request.form.get("project_id")
        
        if worker_id and project_id:
            # Hier rufst du deine Stempel-Funktion auf, 
            # die in deiner db.py definiert sein muss (inkl. Projektwechsel-Logik)
            db.stamp(int(worker_id), int(project_id))
            
        # Nach dem Absenden Seite neu laden, damit die Änderung sichtbar wird
        return redirect(url_for("startseite"))

    # 2. Daten für die HTML-Seite laden (Mitarbeiter & Projekte)
    # Wichtig: Dafür brauchst du entsprechende Methoden in deiner db.py!
    workers = db.get_all_workers()     # Gibt alle Mitarbeiter zurück
    projects = db.get_all_projects()   # Gibt alle Projekte zurück
    
    # Optional: Aktuellen Status ermitteln (wer ist worauf eingestempelt?)
    # timestamps = db.get_all_timestamps()

    return render_template(
        "start.html", 
        sqlite_version=db.sqlite_version(),
        workers=workers,
        projects=projects
    )

@app.route("/test", methods=["GET", "POST"])
def testseite():
    workers = db.get_all_workers()
    print("test")
    for worker in workers:
        print (worker)
    return render_template("test.html", workers=workers)

@app.cli.command("init-db")
def init_db():
    """Fügt Testdaten hinzu."""
    print("Initialisiere Testdaten...")
    try:
        db.add_project("0", "Work")  
        db.add_worker("Anna", "Test", False)
        print("Testdaten erfolgreich eingefügt.")
    except Exception as e:
        print(f"Hinweis: Daten existieren möglicherweise bereits ({e})")

if __name__ == "__main__":
    app.run(debug=True)