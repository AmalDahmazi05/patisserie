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
    ├── Procfile            # Configuration déploiement cloud
    └── data/
        └── patisserie.db   # Base de données SQLite (créée automatiquement)
```

---

## 🚀 Lancer en local

### Étape 1 – Installer les dépendances Python

```bash
cd backend
pip install -r requirements.txt
```

### Étape 2 – Lancer le serveur

```bash
python app.py
```

### Étape 3 – Ouvrir l'application

Ouvre ton navigateur et va sur :

```
http://localhost:5000
```

La base de données SQLite est créée automatiquement au premier démarrage.

---

## ☁️ Déploiement Azure

L'application est configurée pour Azure App Service.

- Le fichier `Procfile` indique à Azure comment lancer l'app avec Gunicorn
- La base SQLite se crée automatiquement au démarrage
- Le frontend est servi directement par Flask (pas besoin de serveur séparé)

---

## 🔑 Accès Admin

| Champ        | Valeur          |
|--------------|-----------------|
| Identifiant  | `admin`         |
| Mot de passe | `patisserie123` |

Clique sur **Admin** dans la navigation.

---

## 🌐 API Endpoints

| Méthode | URL               | Description                  | Auth |
|---------|-------------------|------------------------------|------|
| GET     | /api/products     | Liste des produits           | Non  |
| POST    | /api/products     | Ajouter un produit           | Non  |
| PUT     | /api/products/:id | Modifier un produit          | Non  |
| DELETE  | /api/products/:id | Supprimer un produit         | Non  |
| POST    | /api/orders       | Créer une commande           | Non  |
| GET     | /api/orders       | Lister les commandes (admin) | Non  |
| PUT     | /api/orders/:id   | Changer le statut            | Non  |
| POST    | /api/admin/login  | Se connecter                 | —    |

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

### Backend
- ✅ API REST avec Flask
- ✅ Base de données SQLite (persistante)
- ✅ Validation des données côté serveur
- ✅ CORS configuré
- ✅ Servi par Gunicorn en production

---

## 📦 Technologies utilisées

| Couche   | Technologie                     |
|----------|---------------------------------|
| Frontend | HTML5, CSS3, JavaScript vanilla |
| Backend  | Python 3, Flask, Flask-CORS     |
| Données  | SQLite                          |
| Serveur  | Gunicorn (production)           |
| Polices  | Google Fonts (Playfair Display) |

