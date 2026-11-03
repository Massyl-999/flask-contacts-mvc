"""
Contrôleur : routes de l'application et coordination modèle / vue.

Le contrôleur lit les requêtes, appelle le modèle (validation + base de données)
et choisit le template à afficher. Il ne contient aucun SQL ni aucun HTML.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.contact_model import ContactModel, DatabaseError

contact_bp = Blueprint("contact", __name__)

FIELDS = ("nom", "prenom", "telephone", "email", "adresse")


def _read_form():
    """Récupère et nettoie les champs du formulaire."""
    return {field: request.form.get(field, "").strip() for field in FIELDS}


def _validate(data):
    """Valide les données ; flashe les erreurs et retourne True si tout est OK."""
    is_valid, errors = ContactModel.validate_contact_data(
        data["nom"], data["prenom"], data["telephone"], data["email"]
    )
    for error in errors:
        flash(error, "error")
    return is_valid


def _render_index(form=None, status=200):
    """Affiche la liste des contacts (et le formulaire pré-rempli si besoin)."""
    try:
        contacts = ContactModel.get_all_contacts()
    except DatabaseError as exc:
        flash(str(exc), "error")
        contacts = []
    return render_template("index.html", contacts=contacts, form=form or {}), status


@contact_bp.route("/")
def index():
    """Page d'accueil : formulaire d'ajout et liste des contacts."""
    return _render_index()


@contact_bp.route("/add", methods=["POST"])
def add_contact():
    """Traite l'ajout d'un contact."""
    data = _read_form()
    if not _validate(data):
        return _render_index(form=data, status=400)

    try:
        ContactModel.add_contact(**data)
    except DatabaseError as exc:
        flash(str(exc), "error")
        return _render_index(form=data, status=500)

    flash("Contact ajouté avec succès !", "success")
    return redirect(url_for("contact.index"))


@contact_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    """Affiche le formulaire d'édition (GET) ou enregistre les changements (POST)."""
    if request.method == "POST":
        data = _read_form()
        if not _validate(data):
            return render_template("edit.html", contact={"id": id, **data}), 400
        try:
            updated = ContactModel.update_contact(id, **data)
        except DatabaseError as exc:
            flash(str(exc), "error")
            return render_template("edit.html", contact={"id": id, **data}), 500
        if updated:
            flash("Contact modifié avec succès !", "success")
        else:
            flash("Contact introuvable.", "error")
        return redirect(url_for("contact.index"))

    try:
        contact = ContactModel.get_contact_by_id(id)
    except DatabaseError as exc:
        flash(str(exc), "error")
        return redirect(url_for("contact.index"))
    if contact is None:
        flash("Contact introuvable.", "error")
        return redirect(url_for("contact.index"))
    return render_template("edit.html", contact=contact)


@contact_bp.route("/delete/<int:id>", methods=["POST"])
def delete_contact(id):
    """Traite la suppression d'un contact."""
    try:
        deleted = ContactModel.delete_contact(id)
    except DatabaseError as exc:
        flash(str(exc), "error")
    else:
        if deleted:
            flash("Contact supprimé avec succès !", "success")
        else:
            flash("Contact introuvable.", "error")
    return redirect(url_for("contact.index"))


# --- Gestion des erreurs (app_errorhandler : valable pour toute l'application,
# --- y compris les URL inconnues qui n'appartiennent à aucun blueprint) ---

@contact_bp.app_errorhandler(400)
def bad_request(error):
    message = "Requête invalide ou formulaire expiré. Rechargez la page et réessayez."
    return render_template("error.html", error=message), 400


@contact_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Page non trouvée"), 404


@contact_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", error="Erreur interne du serveur"), 500
