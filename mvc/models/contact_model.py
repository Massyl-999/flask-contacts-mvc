"""
Modèle : accès aux données et validation des contacts.

ContactModel suit le pattern DAO (Data Access Object) : il encapsule toutes les
opérations de persistance (SQLite) et de validation. Les contrôleurs n'écrivent
jamais de SQL.
"""

import re
import sqlite3
from contextlib import contextmanager

from flask import current_app

SCHEMA = """
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    telephone TEXT,
    email TEXT,
    adresse TEXT
)
"""

SAMPLE_CONTACTS = [
    ("Dupont", "Jean", "0123456789", "jean.dupont@example.com", "123 Rue de Paris"),
    ("Martin", "Sophie", "0987654321", "sophie.martin@example.com", "456 Avenue des Fleurs"),
    ("Dubois", "Pierre", "0654321987", "pierre.dubois@example.com", "789 Boulevard du Lac"),
]


class DatabaseError(Exception):
    """Erreur d'accès à la base (le message peut être affiché à l'utilisateur)."""


@contextmanager
def get_connection():
    """
    Ouvre une connexion SQLite, valide la transaction à la sortie et ferme
    toujours la connexion, même en cas d'erreur.
    """
    conn = None
    try:
        conn = sqlite3.connect(current_app.config["DATABASE"])
        conn.row_factory = sqlite3.Row  # accès aux colonnes par nom
        yield conn
        conn.commit()
    except sqlite3.Error as exc:
        if conn is not None:
            conn.rollback()
        current_app.logger.error("Erreur SQLite : %s", exc)
        raise DatabaseError("Erreur d'accès à la base de données.") from exc
    finally:
        if conn is not None:
            conn.close()


class ContactModel:
    """Opérations CRUD et validation pour les contacts."""

    @staticmethod
    def init_db(seed=False):
        """
        Crée la table des contacts si elle n'existe pas.

        Args:
            seed (bool): insère des contacts d'exemple si la table est vide.

        Returns:
            int: nombre de contacts d'exemple insérés.
        """
        with get_connection() as conn:
            conn.execute(SCHEMA)
            if seed and conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0] == 0:
                conn.executemany(
                    "INSERT INTO contacts (nom, prenom, telephone, email, adresse) "
                    "VALUES (?, ?, ?, ?, ?)",
                    SAMPLE_CONTACTS,
                )
                return len(SAMPLE_CONTACTS)
        return 0

    @staticmethod
    def validate_contact_data(nom, prenom, telephone, email):
        """
        Valide les données d'un contact.

        Returns:
            tuple: (est_valide, liste_des_messages_d_erreur)
        """
        cfg = current_app.config
        min_len = cfg["MIN_NAME_LENGTH"]
        errors = []

        if len((nom or "").strip()) < min_len:
            errors.append(f"Le nom doit contenir au moins {min_len} caractères")
        if len((prenom or "").strip()) < min_len:
            errors.append(f"Le prénom doit contenir au moins {min_len} caractères")
        if telephone and not re.fullmatch(cfg["PHONE_REGEX"], telephone.strip()):
            errors.append("Le numéro de téléphone doit contenir 10 chiffres")
        if email and not re.fullmatch(cfg["EMAIL_REGEX"], email.strip()):
            errors.append("Format d'email invalide")

        return (not errors, errors)

    @staticmethod
    def get_all_contacts():
        """Retourne tous les contacts, triés par nom puis prénom."""
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM contacts "
                "ORDER BY nom COLLATE NOCASE, prenom COLLATE NOCASE"
            ).fetchall()

    @staticmethod
    def get_contact_by_id(id):
        """Retourne un contact (sqlite3.Row) ou None s'il n'existe pas."""
        with get_connection() as conn:
            return conn.execute("SELECT * FROM contacts WHERE id = ?", (id,)).fetchone()

    @staticmethod
    def add_contact(nom, prenom, telephone, email, adresse):
        """Ajoute un contact et retourne son identifiant."""
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO contacts (nom, prenom, telephone, email, adresse) "
                "VALUES (?, ?, ?, ?, ?)",
                (nom, prenom, telephone, email, adresse),
            )
            return cursor.lastrowid

    @staticmethod
    def update_contact(id, nom, prenom, telephone, email, adresse):
        """Met à jour un contact. Retourne False si l'identifiant n'existe pas."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, "
                "email = ?, adresse = ? WHERE id = ?",
                (nom, prenom, telephone, email, adresse, id),
            )
            return cursor.rowcount > 0

    @staticmethod
    def delete_contact(id):
        """Supprime un contact. Retourne False si l'identifiant n'existe pas."""
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
            return cursor.rowcount > 0
