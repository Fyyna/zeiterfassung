def test_startseite_wird_angezeigt(client):
    antwort = client.get("/")
    assert antwort.status_code == 200
    assert "Die App läuft." in antwort.get_data(as_text=True)
