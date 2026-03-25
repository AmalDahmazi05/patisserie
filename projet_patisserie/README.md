# 🍰 La Belle Miette – Pâtisserie en Ligne

Application web complète pour une pâtisserie artisanale avec commande en ligne.

## 📁 Structure du projet

```
patisserie/
├── frontend/
│   └── index.html          # Application SPA (tout-en-un)
└── backend/
    ├── app.py              # Serveur Flask (API REST)
    ├── requirements.txt    # Dépendances Python
    └── data/
        ├── products.json   # Base de données produits
        └── orders.json     # Base de données commandes
```

---

## 🚀 Instructions d'installation

### Prérequis
- **Python 3.8+** installé
- Un navigateur moderne (Chrome, Firefox, Edge)

---

### Étape 1 – Installer les dépendances Python

```bash
cd patisserie/backend
pip install -r requirements.txt
```

---

### Étape 2 – Lancer le serveur backend

```bash
cd patisserie/backend
python app.py
```

Le serveur démarre sur **http://localhost:5000**

Vous devriez voir :
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Étape 3 – Ouvrir le frontend

Ouvrez directement le fichier dans votre navigateur :

```
patisserie/frontend/index.html
```

Double-cliquez sur le fichier, ou glissez-le dans votre navigateur.

> ⚠️ **Note :** Si le backend n'est pas lancé, l'application fonctionne en **mode démo** avec des données intégrées.

---

## 🔑 Accès Admin

| Champ       | Valeur           |
|-------------|------------------|
| Identifiant | `admin`          |
| Mot de passe| `patisserie123`  |

Cliquez sur **Admin** dans la navigation.

---

## 🌐 API Endpoints

| Méthode | URL                    | Description                  | Auth |
|---------|------------------------|------------------------------|------|
| GET     | /api/products          | Liste des produits           | Non  |
| POST    | /api/products          | Ajouter un produit           | Oui  |
| PUT     | /api/products/:id      | Modifier un produit          | Oui  |
| DELETE  | /api/products/:id      | Supprimer un produit         | Oui  |
| POST    | /api/orders            | Créer une commande           | Non  |
| GET     | /api/orders            | Lister les commandes (admin) | Oui  |
| PUT     | /api/orders/:id        | Changer le statut            | Oui  |
| POST    | /api/admin/login       | Se connecter                 | —    |
| POST    | /api/admin/logout      | Se déconnecter               | —    |
| GET     | /api/admin/check       | Vérifier la session          | —    |

---

## ✨ Fonctionnalités

### Frontend
- ✅ Page d'accueil avec héro, galerie et fonctionnalités
- ✅ Menu complet avec filtres par catégorie
- ✅ Panier (ajouter, supprimer, modifier quantités)
- ✅ Formulaire de commande avec validation
- ✅ Page de confirmation
- ✅ Interface admin avec login
- ✅ Dashboard admin (produits + commandes)
- ✅ Design responsive (mobile, tablette, desktop)
- ✅ Fonctionne en mode démo sans backend

### Backend
- ✅ API REST avec Flask
- ✅ Données stockées en JSON (simple et léger)
- ✅ Validation des données côté serveur
- ✅ Authentification session admin
- ✅ CORS configuré pour le développement local

---

## 🛠️ Personnalisation

### Modifier les produits
Éditez `backend/data/products.json` directement, ou utilisez l'interface admin.

### Changer les identifiants admin
Dans `backend/app.py`, modifiez :
```python
ADMIN_USER = "admin"
ADMIN_PASS = "patisserie123"
```

### Changer le nom de la pâtisserie
Cherchez `La Belle Miette` dans `frontend/index.html` et remplacez par votre nom.

---

## 📦 Technologies utilisées

| Couche    | Technologie                     |
|-----------|---------------------------------|
| Frontend  | HTML5, CSS3, JavaScript vanilla |
| Backend   | Python 3, Flask, Flask-CORS     |
| Données   | Fichiers JSON (pas de DB)       |
| Polices   | Google Fonts (Playfair Display) |
| Images    | Unsplash (CDN, gratuites)       |
