# Flask Contacts MVC

![CI](https://github.com/Massyl-999/flask-contacts-mvc/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Application web de gestion de contacts (CRUD) développée avec **Python, Flask et SQLite**.
Le dépôt contient **deux implémentations de la même application** pour comparer l'impact
des choix d'architecture sur la qualité du code :

| Version | Dossier | Description |
|---|---|---|
| Non structurée | [`non_mvc/`](non_mvc) | Un seul fichier : HTML, SQL et routes mélangés (volontairement « maladroit ») |
| Structurée (MVC) | [`mvc/`](mvc) | Séparation modèle / vue / contrôleur, configuration centralisée, validation, tests |

Projet réalisé dans le cadre du module **Génie Logiciel** (3ᵉ année Informatique, cycle ingénieur IA,
Université Mouloud Mammeri de Tizi-Ouzou, 2024/2025). Le rapport complet est dans [`docs/`](docs).

## Fonctionnalités

- Ajouter, lister, modifier et supprimer des contacts
- Validation des données côté serveur **et** côté client
- Messages de confirmation / d'erreur et pages d'erreur dédiées (400, 404, 500)
- Protection CSRF sur tous les formulaires (Flask-WTF)
- Requêtes SQL paramétrées (pas d'injection SQL) et connexions toujours fermées
- Tests automatisés (pytest) et intégration continue (GitHub Actions)

## Architecture (version MVC)

```
Utilisateur ──► Contrôleur ──► Modèle ──► SQLite
                    │
                    └────────► Vue (templates Jinja2 + CSS/JS)
```

- **Modèle** (`mvc/models/contact_model.py`) : accès aux données (pattern DAO) et règles de validation
- **Vue** (`mvc/views/`) : templates Jinja2 héritant de `base.html`, CSS et JS statiques
- **Contrôleur** (`mvc/controllers/contact_controller.py`) : routes Flask, coordination modèle/vue
- **Configuration** (`mvc/config.py`) : paramètres par environnement, surchargeables par variables d'environnement

## Installation

Prérequis : Python 3.10 ou supérieur.

```bash
git clone https://github.com/Massyl-999/flask-contacts-mvc.git
cd flask-contacts-mvc

python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate

pip install -r requirements.txt
```

## Lancer l'application

### Version MVC

```bash
cd mvc
python init_database.py           # optionnel : crée la base + 3 contacts d'exemple
python main.py
```

Puis ouvrez <http://127.0.0.1:5000>. La table est créée automatiquement au démarrage si elle n'existe pas.

### Version non structurée

```bash
cd non_mvc
python app_non_mvc.py
```

## Configuration

Variables d'environnement reconnues par la version MVC :

| Variable | Défaut | Rôle |
|---|---|---|
| `APP_ENV` | `development` | `development`, `testing` ou `production` |
| `SECRET_KEY` | clé de développement | Clé secrète Flask (**obligatoire en production**) |
| `DATABASE_PATH` | `mvc/instance/database.db` | Fichier SQLite |
| `HOST` | `127.0.0.1` | Adresse d'écoute (`0.0.0.0` pour exposer sur le réseau) |
| `PORT` | `5000` | Port d'écoute |

Exemple (port 5001) :

```bash
PORT=5001 python main.py                # Windows PowerShell : $env:PORT=5001; python main.py
```

Exemple de déploiement avec Gunicorn :

```bash
pip install gunicorn
cd mvc
APP_ENV=production SECRET_KEY="une-longue-valeur-aleatoire" gunicorn "main:create_app()"
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Structure du dépôt

```
flask-contacts-mvc/
├── mvc/                  # Version structurée (MVC)
│   ├── main.py           # Point d'entrée (application factory)
│   ├── config.py
│   ├── init_database.py
│   ├── controllers/
│   ├── models/
│   └── views/            # templates/ + static/ (css, js)
├── non_mvc/              # Version monolithique (comparaison)
├── tests/                # Tests pytest
├── docs/                 # Rapport et guide d'utilisation
└── .github/workflows/    # Intégration continue
```

## Pistes d'évolution

- Recherche et filtrage des contacts
- Authentification des utilisateurs
- API REST (JSON)
- Passage à un ORM (SQLAlchemy)

## Auteurs

- Massyl Mouheb
- Mohand Sadi
- Syfax Chemloul

## Licence

Distribué sous licence MIT — voir [LICENSE](LICENSE).
