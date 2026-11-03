"""
Point d'entrée de l'application MVC de gestion de contacts.

Usage :
    python main.py                       # serveur de développement
    gunicorn "main:create_app()"         # exemple de déploiement
"""

import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import get_config
from controllers.contact_controller import contact_bp
from models.contact_model import ContactModel

csrf = CSRFProtect()


def create_app(config_name=None, overrides=None):
    """
    Crée et configure l'application Flask (pattern « application factory »).

    Args:
        config_name (str): development, testing ou production (défaut : APP_ENV).
        overrides (dict): valeurs de configuration à forcer (utile pour les tests).

    Returns:
        Flask: l'application configurée.
    """
    cfg = get_config(config_name)
    app = Flask(
        __name__,
        template_folder=cfg.TEMPLATE_FOLDER,
        static_folder=cfg.STATIC_FOLDER,
    )
    app.config.from_object(cfg)
    if overrides:
        app.config.update(overrides)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY n'est pas définie : exportez cette variable d'environnement."
        )

    # Protection CSRF pour tous les formulaires POST
    csrf.init_app(app)

    # Le dossier de la base de données doit exister avant la première connexion
    db_dir = os.path.dirname(app.config["DATABASE"])
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    app.register_blueprint(contact_bp)

    # Crée la table si nécessaire (sans données d'exemple)
    with app.app_context():
        ContactModel.init_db()

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(
        debug=application.config["DEBUG"],
        host=application.config["HOST"],
        port=application.config["PORT"],
    )
