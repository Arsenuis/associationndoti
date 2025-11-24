# 🌟 Ndoti Blog

**« Tout commence par un rêve »**

Un blog Django moderne pour l'Association Ndoti, axé sur l'éducation, la santé et le développement communautaire.

## 📋 Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure de la base de données](#structure-de-la-base-de-données)
- [Interface d'administration](#interface-dadministration)
- [Personnalisation du design](#personnalisation-du-design)
- [Déploiement](#déploiement)
- [Contribution](#contribution)
- [Licence](#licence)

## 🎯 À propos

Le **Ndoti Blog** est une plateforme web développée pour l'Association Ndoti, une organisation dédiée à l'amélioration des conditions de vie des communautés à travers trois piliers principaux :

- **🎓 Éducation** : Accès à l'éducation pour tous les enfants
- **🏥 Santé** : Soins de santé de qualité et accessibles
- **🌱 Développement** : Autonomisation des communautés

## ✨ Fonctionnalités

### 🔐 Authentification
- Inscription et connexion des utilisateurs
- Gestion des profils utilisateur avec avatars
- Système de rôles (Auteur, Lecteur, Admin)
- Formulaires personnalisés avec Bootstrap

### 📰 Gestion des articles
- Publication d'articles avec images
- Système de brouillons et publication
- Affichage chronologique des articles
- Page de détail pour chaque article
- Support des images avec upload automatique

### 💬 Système de commentaires
- Commentaires liés aux articles
- Affichage des commentaires avec dates
- Gestion par utilisateur authentifié

### 🎨 Design moderne
- Interface responsive avec Bootstrap 5
- Thème personnalisé aux couleurs de Ndoti (Vert/Jaune/Blanc)
- Navigation intuitive
- Animations et transitions CSS

### ⚡ Administration
- Interface d'administration Django complète
- Gestion des articles, commentaires et profils
- Filtres et recherche avancée
- Gestion des statuts de publication

## 🏗️ Architecture du projet

```
ndoti_blog/
├── 📁 blog_projet/                 # Configuration Django principale
│   ├── __init__.py
│   ├── settings.py                 # Configuration générale
│   ├── urls.py                     # URLs principales
│   ├── wsgi.py                     # Configuration WSGI
│   └── asgi.py                     # Configuration ASGI
├── 📁 blog_app/                    # Application principale
│   ├── 📁 migrations/              # Migrations de base de données
│   ├── 📁 templates/               # Templates HTML
│   │   ├── base.html               # Template de base
│   │   ├── home.html               # Page d'accueil
│   │   ├── 📁 articles/            # Templates articles
│   │   └── 📁 registration/        # Templates authentification
│   ├── models.py                   # Modèles de données
│   ├── views.py                    # Vues/contrôleurs
│   ├── urls.py                     # URLs de l'application
│   ├── forms.py                    # Formulaires personnalisés
│   ├── admin.py                    # Configuration admin
│   └── apps.py                     # Configuration app
├── 📁 static/                      # Fichiers statiques
│   └── 📁 css/
│       └── style.css               # Styles personnalisés
├── 📁 media/                       # Fichiers uploadés
│   ├── 📁 articles/images/         # Images des articles
│   └── 📁 profiles/                # Avatars des profils
├── 📁 venv/                        # Environnement virtuel Python
├── manage.py                       # Utilitaire de gestion Django
├── db.sqlite3                      # Base de données (développement)
└── .env                           # Variables d'environnement
```

## 🛠️ Technologies utilisées

### Backend
- **Django 3.2.25** - Framework web Python
- **Python 3.6+** - Langage de programmation
- **PostgreSQL** - Base de données (production)
- **SQLite** - Base de données (développement)

### Frontend
- **HTML5** & **CSS3** - Structure et style
- **Bootstrap 5.3.0** - Framework CSS responsive
- **JavaScript** - Interactions côté client
- **Lucide Icons** - Icônes modernes

### Dépendances Python
- **Pillow** - Traitement d'images
- **python-decouple** - Gestion des variables d'environnement
- **psycopg2-binary** - Connecteur PostgreSQL

## 🚀 Installation

### Prérequis
- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)
- PostgreSQL (pour la production)

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone [URL_DU_REPO]
cd ndoti_blog
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install django==3.2.25
pip install pillow
pip install python-decouple
pip install psycopg2-binary  # Pour PostgreSQL
```

5. **Configuration de la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

Le site sera accessible à l'adresse : `http://127.0.0.1:8000/`

## ⚙️ Configuration

### Variables d'environnement (.env)

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Base de données PostgreSQL (Production)
DB_NAME=ndoti_blog_db
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432

# Sécurité Django
SECRET_KEY=votre_clé_secrète_django
DEBUG=False  # True pour le développement
```

### Configuration des médias

Les fichiers uploadés sont stockés dans le dossier `media/` :
- **Articles** : `media/articles/images/`
- **Profils** : `media/profiles/`

### Configuration statique

Les fichiers CSS, JS et images statiques sont dans `static/` :
- **CSS personnalisé** : `static/css/style.css`

## 🎮 Utilisation

### Interface utilisateur

1. **Page d'accueil** (`/`)
   - Présentation de l'association Ndoti
   - Affichage des 6 derniers articles publiés
   - Section héro avec les valeurs de l'association

2. **Liste des articles** (`/articles/`)
   - Tous les articles publiés par ordre chronologique
   - Liens vers les détails de chaque article

3. **Détail d'un article** (`/articles/<id>/`)
   - Contenu complet de l'article
   - Image associée (si présente)
   - Commentaires des utilisateurs
   - Informations sur l'auteur et la date

4. **Authentification**
   - **Inscription** (`/register/`) : Création de compte
   - **Connexion** (`/login/`) : Authentification
   - **Déconnexion** (`/logout/`) : Fermeture de session

### Interface d'administration

Accédez à l'administration via `/admin/` avec vos identifiants superutilisateur :

- **Gestion des articles** : Création, modification, publication
- **Gestion des commentaires** : Modération des commentaires
- **Gestion des utilisateurs** : Profils et rôles
- **Statistiques** : Vue d'ensemble du contenu

## 🗄️ Structure de la base de données

### Modèle Article
```python
- titre (CharField) : Titre de l'article
- contenu (TextField) : Contenu principal
- image (ImageField) : Image illustrative (optionnelle)
- auteur (ForeignKey vers User) : Auteur de l'article
- date_publication (DateTimeField) : Date de création
- statut (CharField) : 'brouillon' ou 'publie'
```

### Modèle Commentaire
```python
- article (ForeignKey vers Article) : Article commenté
- auteur (ForeignKey vers User) : Auteur du commentaire
- contenu (TextField) : Contenu du commentaire
- date (DateTimeField) : Date de création
```

### Modèle Profile
```python
- user (OneToOneField vers User) : Utilisateur associé
- avatar (ImageField) : Photo de profil (optionnelle)
- bio (TextField) : Biographie (optionnelle)  
- role (CharField) : 'auteur', 'lecteur' ou 'admin'
```

## 🎨 Personnalisation du design

### Thème couleurs Ndoti
Le design utilise une palette de couleurs spécifique :

```css
:root {
    --ndoti-green: #16a34a;      /* Vert principal */
    --ndoti-yellow: #fbbf24;     /* Jaune accent */
    --ndoti-white: #ffffff;      /* Blanc */
}
```

### Composants stylisés
- **Navigation** : Navbar sticky avec effets de survol
- **Boutons** : Styles personnalisés aux couleurs Ndoti
- **Cards** : Design moderne avec ombres et bordures arrondies
- **Formulaires** : Intégration Bootstrap avec styles personnalisés

### Responsive Design
- Optimisé pour mobile, tablette et desktop
- Grid responsive pour les articles
- Navigation mobile avec menu hamburger

## 🚀 Déploiement

### Production avec PostgreSQL

1. **Configurer PostgreSQL**
```bash
# Créer la base de données
createdb ndoti_blog_db
```

2. **Configurer les variables d'environnement**
```env
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
```

3. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic
```

4. **Appliquer les migrations**
```bash
python manage.py migrate
```

### Recommandations de sécurité
- Changez la `SECRET_KEY` en production
- Configurez `ALLOWED_HOSTS` appropriément
- Utilisez HTTPS
- Configurez un serveur web (Nginx/Apache)
- Utilisez un serveur d'application (Gunicorn/uWSGI)

## 🤝 Contribution

### Workflow de développement

1. Fork du projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit des changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

### Standards de code
- Suivre les conventions PEP 8 pour Python
- Commenter le code en français
- Utiliser des noms de variables explicites
- Tester les nouvelles fonctionnalités

## 📝 Améliorations futures

### Fonctionnalités envisagées
- [ ] **Système de tags** pour les articles
- [ ] **Recherche** dans les articles
- [ ] **Newsletter** par email
- [ ] **Partage** sur réseaux sociaux
- [ ] **API REST** pour applications mobiles
- [ ] **Système de likes** pour les articles
- [ ] **Notifications** pour les nouveaux commentaires
- [ ] **Editeur WYSIWYG** pour les articles
- [ ] **Catégories** d'articles
- [ ] **Pagination** avancée

### Optimisations techniques
- [ ] **Cache** pour améliorer les performances
- [ ] **CDN** pour les fichiers statiques
- [ ] **Compression** d'images automatique
- [ ] **Tests unitaires** complets
- [ ] **Monitoring** et logs
- [ ] **Sauvegarde** automatique

## 📄 Licence

Ce projet est développé pour l'Association Ndoti. Tous droits réservés.

## 📞 Contact

**Association Ndoti**
- 🌐 Site web : [En développement]
- 📧 Email : [contact@ndoti.org]
- 📍 Localisation : [À préciser]

---

### 🙏 Remerciements

Merci à tous les contributeurs qui participent au développement de cette plateforme pour soutenir la mission de l'Association Ndoti.

*« Tout commence par un rêve » - Association Ndoti*