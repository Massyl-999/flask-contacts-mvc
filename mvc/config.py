"""
Configuration centralisée de l'application de gestion de contacts.

Les valeurs sensibles (clé secrète, chemin de la base, hôte, port) peuvent être
surchargées par des variables d'environnement, ce qui évite de les écrire en
dur dans le code source :

    APP_ENV        development (défaut) | testing | production
    SECRET_KEY     clé secrète Flask (obligatoire en production)
    DATABASE_PATH  chemin du fichier SQLite
    HOST / PORT    adresse et port d'écoute (défaut : 127.0.0.1:5000)
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuration de base, partagée par tous les environnements."""

    BASE_DIR = BASE_DIR

    # Base de données
    DATABASE = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "instance", "database.db")
    )

    # Clé secrète (sessions, messages flash, jetons CSRF)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-a-changer")

    # Serveur : local uniquement par défaut (mettre HOST=0.0.0.0 pour exposer)
    DEBUG = False
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", 5000))

    # Dossiers des vues
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "views", "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "views", "static")

    # Règles de validation
    MIN_NAME_LENGTH = 2
    PHONE_REGEX = r"^[0-9]{10}$"
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "testing-secret-key"
    DATABASE = os.path.join(BASE_DIR, "instance", "test_database.db")
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    # Pas de valeur par défaut : l'application refuse de démarrer sans SECRET_KEY
    SECRET_KEY = os.environ.get("SECRET_KEY")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name=None):
    """Retourne la classe de configuration demandée (ou celle de APP_ENV)."""
    name = (name or os.environ.get("APP_ENV", "development")).lower()
    try:
        return config[name]
    except KeyError:
        choix = ", ".join(config)
        raise ValueError(f"Configuration inconnue : {name!r} (choix : {choix})") from None
