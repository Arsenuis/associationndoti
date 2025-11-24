# 📚 Documentation Technique Complète - Ndoti Blog

## Table des Matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Architecture du projet](#architecture-du-projet)
3. [Structure des fichiers](#structure-des-fichiers)
4. [Configuration de la base de données](#configuration-de-la-base-de-données)
5. [Modèles de données (Models)](#modèles-de-données-models)
6. [Vues (Views)](#vues-views)
7. [Templates et Interface](#templates-et-interface)
8. [Système d'administration](#système-dadministration)
9. [Guide d'installation Django + PostgreSQL](#guide-dinstallation-django--postgresql)
10. [Déploiement](#déploiement)

---

## 1. Vue d'ensemble du projet

Le **Ndoti Blog** est une application web Django complète développée pour l'Association Ndoti. Il s'agit d'une plateforme de blog moderne avec les fonctionnalités suivantes :

### Fonctionnalités principales :
- **Système de gestion d'articles** avec éditeur riche
- **Système de commentaires** interactif
- **Galerie multimédia** (images et vidéos)
- **Système de likes** AJAX
- **Gestion des profils utilisateurs** avec avatars
- **Formulaire de contact** avancé
- **Système de dons** intégré avec PayPal
- **Interface d'administration** personnalisée avec Jazzmin
- **Design responsive** avec Bootstrap 5

### Technologies utilisées :
- **Backend** : Django 3.2.25, Python
- **Frontend** : Bootstrap 5, JavaScript (AJAX), CSS personnalisé
- **Base de données** : PostgreSQL (avec SQLite pour le développement)
- **Médias** : Gestion d'uploads d'images et vidéos
- **Interface admin** : Django Admin + Jazzmin

---

## 2. Architecture du projet

### Structure MVC (Model-View-Controller) de Django

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     MODELS      │    │      VIEWS      │    │    TEMPLATES    │
│                 │    │                 │    │                 │
│ • Article       │◄──►│ • home()        │◄──►│ • base.html     │
│ • Commentaire   │    │ • article_list()│    │ • home.html     │
│ • Profile       │    │ • article_detail│    │ • article_*.html│
│ • Contact       │    │ • profil()      │    │ • profil_*.html │
│ • GalerieMedia  │    │ • galerie()     │    │ • galerie_*.html│
│ • Like          │    │ • contact()     │    │ • contact.html  │
│ • Don           │    │ • toggle_like() │    │ • dons_*.html   │
│                 │    │ • faire_don()   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DATABASE      │    │      URLS       │    │      STATIC     │
│                 │    │                 │    │                 │
│ PostgreSQL      │    │ • blog_projet/  │    │ • CSS           │
│ Tables:         │    │   urls.py       │    │ • JavaScript    │
│ • blog_app_*    │    │ • blog_app/     │    │ • Images        │
│ • auth_user     │    │   urls.py       │    │ • Videos        │
│ • django_*      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flow de données

1. **Requête utilisateur** → URLs → Views
2. **Views** → Models (récupération/modification données)
3. **Models** ↔ Database (PostgreSQL)
4. **Views** → Templates (rendu HTML)
5. **Templates** → Response utilisateur

---

## 3. Structure des fichiers

```
ndoti_blog/
├── manage.py                    # Script de gestion Django
├── db.sqlite3                   # Base de données SQLite (dev)
├── .env                         # Variables d'environnement
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation utilisateur
├── DOCUMENTATION_TECHNIQUE_COMPLETE.md  # Cette documentation
│
├── blog_projet/                 # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py              # Configuration globale
│   ├── urls.py                  # URLs racine
│   ├── wsgi.py                  # Interface WSGI
│   └── asgi.py                  # Interface ASGI
│
├── blog_app/                    # Application principale
│   ├── __init__.py
│   ├── models.py                # Modèles de données
│   ├── views.py                 # Logique métier
│   ├── urls.py                  # Routage URLs
│   ├── forms.py                 # Formulaires Django
│   ├── admin.py                 # Interface d'administration
│   ├── apps.py                  # Configuration app
│   ├── tests.py                 # Tests unitaires
│   │
│   ├── migrations/              # Migrations base de données
│   │   ├── 0001_initial.py
│   │   ├── 0002_commentaire.py
│   │   ├── 0003_profile.py
│   │   ├── 0004_contact.py
│   │   ├── 0005_galeriemedia.py
│   │   ├── 0006_auto_20251018_1744.py
│   │   ├── 0007_like.py
│   │   └── 0008_don.py
│   │
│   ├── templates/               # Templates HTML
│   │   ├── base.html            # Template de base
│   │   ├── home.html            # Page d'accueil
│   │   ├── contact.html         # Page contact
│   │   ├── articles/
│   │   │   ├── article_list.html
│   │   │   └── article_detail.html
│   │   ├── galerie/
│   │   │   ├── galerie.html
│   │   │   └── detail.html
│   │   ├── profil/
│   │   │   ├── profil.html
│   │   │   ├── edit_profil.html
│   │   │   ├── profil_public.html
│   │   │   ├── change_password.html
│   │   │   └── delete_account.html
│   │   ├── dons/
│   │   │   ├── faire_un_don.html
│   │   │   ├── don_success.html
│   │   │   └── paypal_redirect.html
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── logout.html
│   │   └── admin/
│   │       ├── base.html
│   │       └── base_site.html
│   │
│   └── templatetags/            # Filtres personnalisés
│       ├── __init__.py
│       ├── article_filters.py   # Formatage articles
│       └── clean_filters.py
│
├── static/                      # Fichiers statiques
│   ├── css/
│   │   └── style.css            # CSS principal
│   ├── js/
│   │   └── likes.js             # JavaScript AJAX
│   ├── images/                  # Images statiques
│   └── videos/                  # Vidéos statiques
│
├── media/                       # Fichiers uploadés
│   ├── articles/images/         # Images d'articles
│   ├── galerie/
│   │   ├── images/
│   │   └── videos/
│   ├── profiles/                # Avatars utilisateurs
│   └── uploads/
│
└── staticfiles/                 # Fichiers statiques collectés (prod)
    ├── admin/
    ├── css/
    ├── js/
    └── jazzmin/
```

---

## 4. Configuration de la base de données

### 4.1 Configuration PostgreSQL

Le projet utilise PostgreSQL en production et SQLite pour le développement.

#### Fichier `.env` (variables d'environnement) :
```env
DB_NAME=ndoti_blog_db
DB_USER=ndoti_user
DB_PASSWORD=votre_mot_de_passe_securise
DB_HOST=localhost
DB_PORT=5432
```

#### Configuration dans `settings.py` :
```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

### 4.2 Structure de la base de données

#### Tables principales créées par Django :

1. **Tables système Django :**
   - `django_migrations` : Historique des migrations
   - `django_content_type` : Types de contenu
   - `django_session` : Sessions utilisateur
   - `auth_user` : Utilisateurs Django
   - `auth_group` : Groupes d'utilisateurs
   - `auth_permission` : Permissions

2. **Tables de l'application (`blog_app_*`) :**

```sql
-- Table des articles
blog_app_article
├── id (BigAutoField, PK)
├── titre (CharField, max_length=200)
├── contenu (TextField)
├── image (ImageField)
├── date_publication (DateTimeField, auto_now_add=True)
├── statut (CharField, choices=['brouillon', 'publie'])
└── auteur_id (ForeignKey → auth_user.id)

-- Table des commentaires
blog_app_commentaire
├── id (BigAutoField, PK)
├── contenu (TextField)
├── date (DateTimeField, auto_now_add=True)
├── article_id (ForeignKey → blog_app_article.id)
└── auteur_id (ForeignKey → auth_user.id)

-- Table des profils
blog_app_profile
├── id (BigAutoField, PK)
├── avatar (ImageField)
├── bio (TextField, nullable)
├── role (CharField, choices=['auteur', 'lecteur', 'admin'])
└── user_id (OneToOneField → auth_user.id)

-- Table des contacts
blog_app_contact
├── id (BigAutoField, PK)
├── nom (CharField, max_length=100)
├── email (EmailField)
├── sujet (CharField, choices)
├── message (TextField)
├── date_envoi (DateTimeField, auto_now_add=True)
├── traite (BooleanField, default=False)
└── utilisateur_id (ForeignKey → auth_user.id, nullable)

-- Table de la galerie
blog_app_galeriemedia
├── id (BigAutoField, PK)
├── titre (CharField, max_length=200)
├── description (TextField, nullable)
├── type_media (CharField, choices=['image', 'video'])
├── categorie (CharField, choices)
├── image (ImageField, nullable)
├── video (FileField, nullable)
├── video_url (URLField, nullable)
├── date_creation (DateTimeField, auto_now_add=True)
├── date_evenement (DateField, nullable)
├── lieu (CharField, nullable)
├── actif (BooleanField, default=True)
├── ordre (PositiveIntegerField, default=0)
└── ajoute_par_id (ForeignKey → auth_user.id, nullable)

-- Table des likes
blog_app_like
├── id (BigAutoField, PK)
├── date_creation (DateTimeField, auto_now_add=True)
├── user_id (ForeignKey → auth_user.id)
├── article_id (ForeignKey → blog_app_article.id, nullable)
└── media_id (ForeignKey → blog_app_galeriemedia.id, nullable)
-- Contraintes : UNIQUE(user_id, article_id), UNIQUE(user_id, media_id)

-- Table des dons
blog_app_don
├── id (BigAutoField, PK)
├── nom (CharField, max_length=100)
├── email (EmailField)
├── montant (DecimalField, max_digits=10, decimal_places=2)
├── type_don (CharField, choices=['unique', 'mensuel'])
├── message (TextField, nullable)
├── date_creation (DateTimeField, auto_now_add=True)
├── paypal_complete (BooleanField, default=False)
└── utilisateur_id (ForeignKey → auth_user.id, nullable)
```

### 4.3 Relations entre les tables

```
auth_user (Django)
├─── blog_app_article (auteur_id) [1:N]
├─── blog_app_commentaire (auteur_id) [1:N]
├─── blog_app_profile (user_id) [1:1]
├─── blog_app_contact (utilisateur_id) [1:N, optional]
├─── blog_app_galeriemedia (ajoute_par_id) [1:N, optional]
├─── blog_app_like (user_id) [1:N]
└─── blog_app_don (utilisateur_id) [1:N, optional]

blog_app_article
├─── blog_app_commentaire (article_id) [1:N]
└─── blog_app_like (article_id) [1:N, optional]

blog_app_galeriemedia
└─── blog_app_like (media_id) [1:N, optional]
```

---

## 5. Modèles de données (Models)

### 5.1 Modèle Article

```python
class Article(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre de l'article")
    contenu = models.TextField(verbose_name="Contenu de l'article")
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon')

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre

    def total_likes(self):
        """Retourne le nombre total de likes pour cet article"""
        return self.likes.count()

    def is_liked_by(self, user):
        """Vérifie si un utilisateur a liké cet article"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
```

**Fonctionnalités :**
- Gestion de statuts (brouillon/publié)
- Upload d'images avec organisation par dossiers
- Méthodes utilitaires pour les likes
- Relations avec commentaires et likes via `related_name`

### 5.2 Modèle Like (Système de likes AJAX)

```python
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    media = models.ForeignKey(GalerieMedia, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ['user', 'article'],
            ['user', 'media']
        ]

    def clean(self):
        """Validation : un like doit être associé soit à un article, soit à un média"""
        if self.article and self.media:
            raise ValidationError("Un like ne peut être associé qu'à un article OU un média.")
        if not self.article and not self.media:
            raise ValidationError("Un like doit être associé à un article ou un média.")
```

**Particularités :**
- Table polymorphe (peut liker un article OU un média)
- Contraintes d'unicité pour éviter les doublons
- Validation personnalisée dans `clean()`

---

## 6. Vues (Views)

### 6.1 Architecture des vues

Le fichier `views.py` contient 508 lignes et organise les vues par fonctionnalité :

#### Structure :
1. **Vues publiques** : home, article_list, article_detail
2. **Authentification** : register, login, logout
3. **Profils** : profil, edit_profil, change_password, delete_account
4. **Contact** : contact
5. **Galerie** : galerie, galerie_detail
6. **Likes AJAX** : toggle_like_article, toggle_like_media
7. **Dons** : faire_un_don, paypal_redirect, don_success

### 6.2 Exemple de vue complexe : `article_detail`

```python
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, statut='publie')
    commentaires = article.commentaires.all().order_by('-date')
    
    # Calcul du temps de lecture (200 mots/minute)
    nombre_mots = len(article.contenu.split())
    temps_lecture = max(1, round(nombre_mots / 200))
    
    # Navigation article précédent/suivant
    article_precedent = Article.objects.filter(
        date_publication__lt=article.date_publication,
        statut='publie'
    ).order_by('-date_publication').first()
    
    article_suivant = Article.objects.filter(
        date_publication__gt=article.date_publication,
        statut='publie'
    ).order_by('date_publication').first()
    
    # Vérifier si l'utilisateur a liké cet article
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(user=request.user, article=article).exists()
    
    # Traitement du formulaire de commentaire
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.save()
            messages.success(request, 'Votre commentaire a été ajouté avec succès !')
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentaireForm()
    
    context = {
        'article': article,
        'commentaires': commentaires,
        'form': form,
        'commentaires_count': commentaires.count(),
        'temps_lecture': temps_lecture,
        'article_precedent': article_precedent,
        'article_suivant': article_suivant,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'articles/article_detail.html', context)
```

**Fonctionnalités avancées :**
- Calcul automatique du temps de lecture
- Navigation entre articles (précédent/suivant)
- Gestion des likes utilisateur
- Formulaire de commentaire intégré
- Optimisation des requêtes SQL

### 6.3 Vues AJAX pour les likes

```python
@login_required
@require_POST
def toggle_like_article(request, article_id):
    """Vue AJAX pour liker/unliker un article"""
    article = get_object_or_404(Article, id=article_id, statut='publie')
    
    like_exists = Like.objects.filter(user=request.user, article=article).first()
    
    if like_exists:
        like_exists.delete()
        liked = False
        message = "Vous n'aimez plus cet article"
    else:
        Like.objects.create(user=request.user, article=article)
        liked = True
        message = "Vous aimez cet article !"
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'total_likes': article.total_likes(),
        'message': message
    })
```

---

## 7. Templates et Interface

### 7.1 Template de base (`base.html`)

Le template de base utilise Bootstrap 5 et définit la structure commune :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Ndoti Blog{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body class="bg-light">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #91CD8C;">
        <!-- Navigation content -->
    </nav>

    <!-- Contenu principal -->
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="mt-5 py-5 text-white" style="background: linear-gradient(135deg, #91CD8C 0%, #10b981 100%);">
        <!-- Footer content -->
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 7.2 Template tags personnalisés

#### Filtre de formatage intelligent (`article_filters.py`)

```python
@register.filter
def smart_format(content):
    """Formatage automatique du contenu avec Markdown simplifié"""
    if not content:
        return ""
    
    # Formatage Markdown simple
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="ndoti-bold">\1</strong>', content)
    content = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em class="ndoti-italic">\1</em>', content)
    
    # Division en paragraphes intelligente
    if '\n\n' in content:
        paragraphs = content.split('\n\n')
    else:
        # Division automatique par phrases
        sentences = re.split(r'(?<=\.)\s+(?=[A-ZÀÁÂÄÇÉÈÊËÏÎÔÙÛÜŸÑ])', content.strip())
        # ... logique de regroupement
    
    # Formatage contextuel
    formatted_paragraphs = []
    for i, paragraph in enumerate(paragraphs):
        if i == 0:
            # Premier paragraphe = introduction
            formatted_paragraphs.append(f'<p class="intro-paragraph">{paragraph}</p>')
        elif re.match(r'^[A-ZÀÁÂÄÇÉÈÊËÏÎÔÙÛÜŸÑ\s]{8,}$', paragraph):
            # Titre détecté (MAJUSCULES)
            formatted_paragraphs.append(f'<h3 class="section-title">{paragraph.title()}</h3>')
        elif paragraph.startswith(('"', '« ', '«', '"')):
            # Citations
            formatted_paragraphs.append(f'<blockquote class="article-quote">{paragraph}</blockquote>')
        else:
            # Paragraphe normal
            formatted_paragraphs.append(f'<p>{paragraph}</p>')
    
    return mark_safe('\n'.join(formatted_paragraphs))
```

### 7.3 JavaScript AJAX (`likes.js`)

```javascript
function toggleLike(contentType, contentId) {
    const button = document.getElementById(`like-btn-${contentType}-${contentId}`);
    const icon = button.querySelector('.like-icon');
    const countSpan = button.querySelector('.like-count');
    
    const url = contentType === 'article' 
        ? `/articles/${contentId}/like/` 
        : `/galerie/${contentId}/like/`;
    
    button.disabled = true;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mise à jour de l'interface
            if (data.liked) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = '#ef4444';
                button.classList.add('liked');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = '#91CD8C';
                button.classList.remove('liked');
            }
            
            countSpan.textContent = data.total_likes;
            
            // Animation
            button.classList.add('pulse-animation');
            setTimeout(() => button.classList.remove('pulse-animation'), 300);
            
            showToast(data.message, data.liked ? 'success' : 'info');
        }
    })
    .finally(() => {
        button.disabled = false;
    });
}
```

---

## 8. Système d'administration

### 8.1 Configuration Jazzmin

Interface d'administration moderne avec Jazzmin :

```python
JAZZMIN_SETTINGS = {
    # Branding
    "site_title": "Ndoti Admin Pro",
    "site_header": "🌱 Espace Administration Ndoti",
    "site_brand": "Ndoti Blog",
    "site_icon": "🌱",
    "welcome_sign": "Bienvenue dans votre espace d'administration professionnel",
    "copyright": "© 2025 Association Ndoti - Tous droits réservés",
    
    # Recherche intelligente
    "search_model": [
        "blog_app.Article", 
        "blog_app.Commentaire", 
        "blog_app.Contact",
        "auth.User"
    ],
    
    # Icônes personnalisées
    "icons": {
        "auth": "fas fa-shield-alt",
        "auth.user": "fas fa-user-shield",
        "blog_app": "fas fa-blog",
        "blog_app.Article": "fas fa-newspaper",
        "blog_app.Commentaire": "fas fa-comments",
        "blog_app.Profile": "fas fa-user-circle",
        "blog_app.Contact": "fas fa-envelope-open-text",
        "blog_app.GalerieMedia": "fas fa-photo-video",
    },
    
    # Thème visuel
    "theme": "flatly",
    "sidebar": "sidebar-dark-success",
}
```

### 8.2 Admin personnalisés

#### Admin des articles avec prévisualisation :

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'statut_badge', 'date_publication', 'apercu_image')
    list_filter = ('statut', 'date_publication', 'auteur')
    search_fields = ('titre', 'contenu')
    readonly_fields = ('date_publication', 'apercu_image_detail')
    
    def statut_badge(self, obj):
        if obj.statut == 'publie':
            return mark_safe(f'<span style="background: #91CD8C; color: white; padding: 5px 12px; border-radius: 20px; font-weight: 600;">✓ Publié</span>')
        else:
            return mark_safe(f'<span style="background: #fbbf24; color: #1a3009; padding: 5px 12px; border-radius: 20px; font-weight: 600;">✎ Brouillon</span>')
    
    def apercu_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />')
        return mark_safe('<span style="color: #999;">📷 Pas d\'image</span>')
```

---

## 9. Guide d'installation Django + PostgreSQL

### 9.1 Prérequis

1. **Python 3.8+** installé
2. **PostgreSQL** installé et configuré
3. **pip** pour la gestion des paquets Python
4. **Git** pour le versioning

### 9.2 Installation étape par étape

#### Étape 1 : Créer l'environnement virtuel

```bash
# Créer un dossier pour le projet
mkdir mon_projet_django
cd mon_projet_django

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Activer l'environnement (Linux/Mac)
source venv/bin/activate
```

#### Étape 2 : Installer Django et dépendances

```bash
# Installer Django
pip install django==3.2.25

# Installer les dépendances PostgreSQL
pip install psycopg2-binary

# Installer les autres dépendances
pip install python-decouple  # Pour les variables d'environnement
pip install Pillow           # Pour les images
pip install django-jazzmin   # Pour l'admin moderne
```

#### Étape 3 : Créer le projet Django

```bash
# Créer le projet
django-admin startproject mon_projet .

# Créer l'application
python manage.py startapp mon_app
```

#### Étape 4 : Configuration PostgreSQL

1. **Créer la base de données** :
```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer la base de données
CREATE DATABASE mon_projet_db;

-- Créer un utilisateur
CREATE USER mon_user WITH PASSWORD 'mot_de_passe_securise';

-- Donner les privilèges
GRANT ALL PRIVILEGES ON DATABASE mon_projet_db TO mon_user;

-- Quitter
\q
```

2. **Créer le fichier `.env`** :
```env
DB_NAME=mon_projet_db
DB_USER=mon_user
DB_PASSWORD=mot_de_passe_securise
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=votre_cle_secrete_django
DEBUG=True
```

#### Étape 5 : Configuration Django (`settings.py`)

```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = []

# Applications
INSTALLED_APPS = [
    'jazzmin',  # Avant django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Votre application
    'mon_app',
]

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True
```

#### Étape 6 : Créer les modèles

**Exemple de modèle simple** (`mon_app/models.py`) :

```python
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu")
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon')
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication']
    
    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Commentaire de {self.auteur.username}"
```

#### Étape 7 : Créer et appliquer les migrations

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

#### Étape 8 : Configurer les URLs

**Projet principal** (`mon_projet/urls.py`) :
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mon_app.urls')),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Application** (`mon_app/urls.py`) :
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
]
```

#### Étape 9 : Créer les vues

**Exemple de vues** (`mon_app/views.py`) :
```python
from django.shortcuts import render, get_object_or_404
from .models import Article, Commentaire

def home(request):
    articles_recents = Article.objects.filter(statut='publie')[:6]
    return render(request, 'home.html', {'articles': articles_recents})

def article_list(request):
    articles = Article.objects.filter(statut='publie').order_by('-date_publication')
    return render(request, 'articles/article_list.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id, statut='publie')
    commentaires = article.commentaires.all().order_by('-date')
    
    context = {
        'article': article,
        'commentaires': commentaires,
    }
    return render(request, 'articles/article_detail.html', context)
```

#### Étape 10 : Créer les templates

**Structure des templates** :
```
mon_app/templates/
├── base.html
├── home.html
└── articles/
    ├── article_list.html
    └── article_detail.html
```

**Template de base** (`templates/base.html`) :
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mon Blog{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Mon Blog</a>
        </div>
    </nav>
    
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### Étape 11 : Configurer l'admin

**Admin basique** (`mon_app/admin.py`) :
```python
from django.contrib import admin
from .models import Article, Commentaire

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'statut', 'date_publication')
    list_filter = ('statut', 'date_publication', 'auteur')
    search_fields = ('titre', 'contenu')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.auteur = request.user
        super().save_model(request, obj, form, change)

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'date')
    list_filter = ('date',)
```

#### Étape 12 : Lancer le serveur

```bash
# Collecter les fichiers statiques (si nécessaire)
python manage.py collectstatic

# Lancer le serveur de développement
python manage.py runserver

# Le site sera accessible à : http://127.0.0.1:8000/
# L'admin sera accessible à : http://127.0.0.1:8000/admin/
```

### 9.3 Bonnes pratiques

#### Structure des fichiers

```bash
# Générer le fichier requirements.txt
pip freeze > requirements.txt

# Créer un .gitignore
echo "venv/
*.pyc
__pycache__/
.env
db.sqlite3
media/
staticfiles/" > .gitignore
```

#### Variables d'environnement

Toujours utiliser un fichier `.env` pour :
- `SECRET_KEY`
- Informations de base de données
- Clés API
- Configuration DEBUG/PRODUCTION

#### Sécurité

1. **Ne jamais commiter le fichier `.env`**
2. **Utiliser des mots de passe forts** pour PostgreSQL
3. **Désactiver DEBUG en production**
4. **Configurer ALLOWED_HOSTS** pour la production

---

## 10. Déploiement

### 10.1 Préparation pour la production

#### Configuration pour la production (`settings.py`) :

```python
import os
from decouple import config

# Sécurité production
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Base de données production
if config('RAILWAY_ENVIRONMENT', default=False):
    # Configuration Railway/Heroku
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('PGDATABASE'),
            'USER': config('PGUSER'),
            'PASSWORD': config('PGPASSWORD'),
            'HOST': config('PGHOST'),
            'PORT': config('PGPORT', default=5432),
        }
    }
else:
    # Configuration locale
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }

# Configuration des fichiers statiques pour la production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuration des médias (utiliser un service cloud en production)
if config('USE_S3', default=False, cast=bool):
    # Configuration AWS S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
```

#### Fichier `requirements.txt` complet :

```txt
Django==3.2.25
psycopg2-binary==2.9.7
python-decouple==3.8
Pillow==10.0.0
django-jazzmin==2.6.0
gunicorn==21.2.0
whitenoise==6.5.0
boto3==1.28.57  # Pour AWS S3 (optionnel)
django-storages==1.13.2  # Pour le stockage cloud (optionnel)
```

### 10.2 Déploiement sur Railway

#### 1. Préparer le projet

```bash
# Créer un fichier Procfile
echo "web: gunicorn mon_projet.wsgi --log-file -" > Procfile

# Configurer whitenoise pour les fichiers statiques
pip install whitenoise
```

Ajouter whitenoise au `MIDDLEWARE` dans `settings.py` :
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajouter ici
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... autres middlewares
]
```

#### 2. Variables d'environnement Railway

```bash
# Variables à configurer sur Railway
DB_NAME=railway_postgres_db
DB_USER=postgres
DB_PASSWORD=generated_password
DB_HOST=containers-us-west-x.railway.app
DB_PORT=5432
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,localhost
RAILWAY_ENVIRONMENT=True
```

### 10.3 Commandes de déploiement

```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (en production)
python manage.py createsuperuser
```

---

## Conclusion

Cette documentation technique complète couvre tous les aspects du projet Ndoti Blog :

1. **Architecture Django MVC** bien structurée
2. **Base de données PostgreSQL** avec relations complexes
3. **Interface utilisateur moderne** avec Bootstrap 5 et AJAX
4. **Administration personnalisée** avec Jazzmin
5. **Fonctionnalités avancées** : likes, galerie, dons, etc.
6. **Guide complet d'installation** Django + PostgreSQL
7. **Bonnes pratiques** de développement et déploiement

Le projet Ndoti Blog démontre une maîtrise complète du framework Django et des technologies web modernes, avec une architecture scalable et maintenable.

---

*© 2025 Association Ndoti - Documentation technique rédigée le 8 novembre 2025*