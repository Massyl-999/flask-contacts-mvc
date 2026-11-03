"""
Initialise la base de données SQLite de l'application.

Usage :
    python init_database.py                   # crée la table + 3 contacts d'exemple
    python init_database.py --no-seed         # crée uniquement la table
    python init_database.py --db ma_base.db   # utilise un autre fichier
"""

import argparse

from main import create_app
from models.contact_model import ContactModel, DatabaseError


def main():
    parser = argparse.ArgumentParser(description="Initialise la base de données.")
    parser.add_argument("--db", help="chemin du fichier SQLite (défaut : instance/database.db)")
    parser.add_argument(
        "--no-seed", action="store_true", help="ne pas insérer de contacts d'exemple"
    )
    args = parser.parse_args()

    app = create_app(overrides={"DATABASE": args.db} if args.db else None)
    with app.app_context():
        print(f"Initialisation de la base de données : {app.config['DATABASE']}")
        try:
            inserted = ContactModel.init_db(seed=not args.no_seed)
        except DatabaseError as exc:
            print(f"Erreur : {exc}")
            return 1
        if inserted:
            print(f"{inserted} contacts d'exemple ajoutés.")
        print("Base de données prête. Lancez l'application avec : python main.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
