from main import create_app
from models.contact_model import ContactModel

VALID = {
    "nom": "Durand",
    "prenom": "Alice",
    "telephone": "0555123456",
    "email": "alice@example.com",
    "adresse": "1 rue des Lilas",
}


def page(client, url="/"):
    return client.get(url).get_data(as_text=True)


def test_index_vide(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Aucun contact trouvé" in response.get_data(as_text=True)


def test_ajout_contact(client):
    response = client.post("/add", data=VALID)
    assert response.status_code == 302
    html = page(client)
    assert "Durand" in html
    assert "Contact ajouté avec succès" in html


def test_ajout_invalide_conserve_la_saisie(client):
    response = client.post("/add", data={**VALID, "nom": "A", "telephone": "123"})
    html = response.get_data(as_text=True)
    assert response.status_code == 400
    assert "Le nom doit contenir au moins 2 caractères" in html
    assert "10 chiffres" in html
    assert 'value="Alice"' in html  # le prénom saisi n'est pas perdu


def test_modification_contact(client):
    client.post("/add", data=VALID)
    response = client.post("/edit/1", data={**VALID, "nom": "Dupuis"})
    assert response.status_code == 302
    html = page(client)
    assert "Dupuis" in html
    assert "Durand" not in html


def test_edition_contact_inexistant(client):
    response = client.get("/edit/999", follow_redirects=True)
    assert "Contact introuvable" in response.get_data(as_text=True)


def test_suppression_contact(client):
    client.post("/add", data=VALID)
    response = client.post("/delete/1")
    assert response.status_code == 302
    assert "Aucun contact trouvé" in page(client)


def test_page_404_personnalisee(client):
    response = client.get("/page-inconnue")
    assert response.status_code == 404
    assert "Page non trouvée" in response.get_data(as_text=True)


def test_csrf_actif_hors_tests(tmp_path):
    app = create_app(
        "testing", {"DATABASE": str(tmp_path / "csrf.db"), "WTF_CSRF_ENABLED": True}
    )
    response = app.test_client().post("/add", data=VALID)
    assert response.status_code == 400


def test_validation_modele(app):
    with app.app_context():
        assert ContactModel.validate_contact_data("Durand", "Alice", "", "") == (True, [])
        ok, erreurs = ContactModel.validate_contact_data("", "A", "12", "pas-un-email")
        assert not ok and len(erreurs) == 4


def test_donnees_exemple_inserees_une_seule_fois(app):
    with app.app_context():
        assert ContactModel.init_db(seed=True) == 3
        assert ContactModel.init_db(seed=True) == 0
        assert len(ContactModel.get_all_contacts()) == 3
