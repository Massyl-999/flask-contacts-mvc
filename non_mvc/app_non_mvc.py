from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize database
conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    telephone TEXT,
    email TEXT,
    adresse TEXT
)''')
conn.commit()
conn.close()

# HTML template as string
TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Gestion des Contacts</title>
    <style>
        /* Variables CSS pour une meilleure maintenance */
        :root {
            --primary-color: #4a90e2;
            --secondary-color: #2ecc71;
            --danger-color: #e74c3c;
            --background-color: #f7f9fc;
            --text-color: #2c3e50;
            --border-radius: 10px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Reset et style général */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 2rem;
        }

        /* En-têtes */
        h1, h2 {
            text-align: center;
            color: var(--text-color);
            margin-bottom: 2rem;
            font-weight: 600;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 3rem;
            position: relative;
        }

        h1::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-color);
            border-radius: 2px;
        }

        /* Formulaire d'ajout */
        form:not(.inline-form) {
            background: white;
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            max-width: 600px;
            margin: 0 auto 3rem auto;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }

        input[type="text"] {
            width: 100%;
            padding: 0.8rem;
            border: 2px solid #e1e8ed;
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input[type="text"]:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
            outline: none;
        }

        /* Boutons */
        input[type="submit"] {
            background: var(--primary-color);
            color: white;
            padding: 0.8rem 1.5rem;
            border: none;
            border-radius: var(--border-radius);
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input[type="submit"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(74, 144, 226, 0.2);
        }

        /* Tableau */
        table {
            width: 100%;
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 2rem;
            overflow: hidden;
        }

        th {
            background: var(--primary-color);
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 0.5px;
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid #e1e8ed;
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover {
            background: #f8fafd;
        }

        /* Actions dans le tableau */
        td form {
            display: inline-block;
            margin: 0 0.3rem;
        }

        td input[type="submit"][value="Supprimer"] {
            background: var(--danger-color);
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }

        td input[type="submit"][value="Modifier"] {
            background: var(--secondary-color);
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }

        td input[type="text"] {
            width: auto;
            padding: 0.5rem;
            margin: 0.2rem;
            font-size: 0.9rem;
        }

        /* Animation des lignes du tableau */
        tr {
            transition: all 0.3s ease;
        }

        /* Design responsive */
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }

            td input[type="text"] {
                width: 80px;
            }

            h1 {
                font-size: 2rem;
            }
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        form, table {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
</head>
<body>
    <h1>Gestion des Contacts</h1>
    <form method="POST" action="/add">
        Nom: <input type="text" name="nom"><br>
        Prénom: <input type="text" name="prenom"><br>
        Téléphone: <input type="text" name="telephone"><br>
        Email: <input type="text" name="email"><br>
        Adresse: <input type="text" name="adresse"><br>
        <input type="submit" value="Ajouter">
    </form>
    <h2>Liste des Contacts</h2>
    <table border="1">
        <tr><th>ID</th><th>Nom</th><th>Prénom</th><th>Téléphone</th><th>Email</th><th>Adresse</th><th>Actions</th></tr>
        {% for contact in contacts %}
        <tr>
            <td>{{ contact[0] }}</td>
            <td>{{ contact[1] }}</td>
            <td>{{ contact[2] }}</td>
            <td>{{ contact[3] }}</td>
            <td>{{ contact[4] }}</td>
            <td>{{ contact[5] }}</td>
            <td>
                <form method="POST" action="/delete/{{ contact[0] }}">
                    <input type="submit" value="Supprimer">
                </form>
                <form method="POST" action="/edit/{{ contact[0] }}">
                    <input type="text" name="nom" value="{{ contact[1] }}">
                    <input type="text" name="prenom" value="{{ contact[2] }}">
                    <input type="text" name="telephone" value="{{ contact[3] }}">
                    <input type="text" name="email" value="{{ contact[4] }}">
                    <input type="text" name="adresse" value="{{ contact[5] }}">
                    <input type="submit" value="Modifier">
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    nom = request.form['nom']
    prenom = request.form['prenom']
    telephone = request.form['telephone']
    email = request.form['email']
    adresse = request.form['adresse']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (nom, prenom, telephone, email, adresse) VALUES (?, ?, ?, ?, ?)',
                   (nom, prenom, telephone, email, adresse))
    conn.commit()
    conn.close()
    return index()

@app.route('/delete/<int:id>', methods=['POST'])
def delete_contact(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return index()

@app.route('/edit/<int:id>', methods=['POST'])
def edit_contact(id):
    nom = request.form['nom']
    prenom = request.form['prenom']
    telephone = request.form['telephone']
    email = request.form['email']
    adresse = request.form['adresse']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, email = ?, adresse = ? WHERE id = ?',
                   (nom, prenom, telephone, email, adresse, id))
    conn.commit()
    conn.close()
    return index()

if __name__ == '__main__':
    app.run(debug=True)
