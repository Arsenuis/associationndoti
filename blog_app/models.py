from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Model for blog articles

class Article(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre de l'article")
    contenu = models.TextField(
        verbose_name="Contenu de l'article",
        help_text="Rédigez votre article ici. Utilisez des paragraphes séparés par des lignes vides pour une meilleure mise en forme automatique."
    )
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True, verbose_name="Image de couverture")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon', verbose_name="Statut")

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

# Model for comments on articles
class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="commentaires")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.article.titre}"

# Model for user profiles

class Profile(models.Model):
    ROLE_CHOICES = [
        ('auteur', 'Auteur'),
        ('lecteur', 'Lecteur'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='lecteur')

    def __str__(self):
        return f"Profil de {self.user.username}"

# Model for contact messages
class Contact(models.Model):
    SUJET_CHOICES = [
        ('general', 'Question générale'),
        ('technique', 'Problème technique'),
        ('partenariat', 'Partenariat'),
        ('suggestion', 'Suggestion d\'amélioration'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    sujet = models.CharField(max_length=20, choices=SUJET_CHOICES, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False, verbose_name="Traité")
    
    # Si l'utilisateur est connecté, on peut lier le message à son compte
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"Message de {self.nom} - {self.get_sujet_display()}"


# Model for gallery media
class GalerieMedia(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
    ]

    CATEGORIE_CHOICES = [
        ('evenement', 'Événement'),
        ('action', 'Action de terrain'),
        ('formation', 'Formation'),
        ('sensibilisation', 'Sensibilisation'),
        ('partenariat', 'Partenariat'),
        ('autre', 'Autre'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    type_media = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Type de média")
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='evenement', verbose_name="Catégorie")
    
    # Champs pour les images
    image = models.ImageField(upload_to='galerie/images/', blank=True, null=True, verbose_name="Image")
    
    # Champs pour les vidéos
    video = models.FileField(upload_to='galerie/videos/', blank=True, null=True, verbose_name="Fichier vidéo")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL vidéo (YouTube, Vimeo, etc.)")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    date_evenement = models.DateField(blank=True, null=True, verbose_name="Date de l'événement")
    lieu = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lieu")
    actif = models.BooleanField(default=True, verbose_name="Visible sur le site")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    # Ajouté par
    ajoute_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ajouté par")

    class Meta:
        verbose_name = "Média de galerie"
        verbose_name_plural = "Médias de galerie"
        ordering = ['-ordre', '-date_creation']

    def __str__(self):
        return f"{self.titre} ({self.get_type_media_display()})"

    def total_likes(self):
        """Retourne le nombre total de likes pour ce média"""
        return self.likes.count()

    def is_liked_by(self, user):
        """Vérifie si un utilisateur a liké ce média"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.type_media == 'image' and not self.image:
            raise ValidationError("Une image est requise pour ce type de média.")
        if self.type_media == 'video' and not self.video and not self.video_url:
            raise ValidationError("Un fichier vidéo ou une URL vidéo est requis pour ce type de média.")

    def get_media_url(self):
        """Retourne l'URL du média selon son type"""
        if self.type_media == 'image' and self.image:
            return self.image.url
        elif self.type_media == 'video' and self.video:
            return self.video.url
        elif self.type_media == 'video' and self.video_url:
            return self.video_url
        return None

    def is_youtube_video(self):
        """Vérifie si c'est une vidéo YouTube"""
        if self.video_url:
            return 'youtube.com' in self.video_url or 'youtu.be' in self.video_url
        return False

    def get_youtube_embed_id(self):
        """Extrait l'ID YouTube pour l'embed"""
        if self.is_youtube_video() and self.video_url:
            import re
            patterns = [
                r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]+)',
                r'(?:youtu\.be\/)([a-zA-Z0-9_-]+)',
                r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]+)'
            ]
            for pattern in patterns:
                match = re.search(pattern, self.video_url)
                if match:
                    return match.group(1)
        return None


# Model for likes on articles and gallery media
class Like(models.Model):
    """
    Modèle pour gérer les likes sur les articles et les médias de galerie
    Un utilisateur ne peut liker qu'une seule fois un article ou un média
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name="likes", verbose_name="Article")
    media = models.ForeignKey(GalerieMedia, on_delete=models.CASCADE, null=True, blank=True, related_name="likes", verbose_name="Média")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date du like")

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        # Un utilisateur ne peut liker qu'une fois le même article ou média
        unique_together = [
            ['user', 'article'],
            ['user', 'media']
        ]
        ordering = ['-date_creation']

    def __str__(self):
        if self.article:
            return f"{self.user.username} aime l'article '{self.article.titre}'"
        elif self.media:
            return f"{self.user.username} aime le média '{self.media.titre}'"
        return f"Like de {self.user.username}"

    def clean(self):
        """Validation : un like doit être associé soit à un article, soit à un média (pas les deux)"""
        from django.core.exceptions import ValidationError
        if self.article and self.media:
            raise ValidationError("Un like ne peut être associé qu'à un article OU un média, pas les deux.")
        if not self.article and not self.media:
            raise ValidationError("Un like doit être associé à un article ou un média.")


# Model for donations tracking
class Don(models.Model):
    """
    Modèle pour enregistrer les intentions de dons
    (les paiements réels sont gérés par PayPal)
    """
    TYPE_CHOICES = [
        ('unique', 'Don unique'),
        ('mensuel', 'Don mensuel'),
    ]
    
    MONTANT_CHOICES = [
        (10, '10€'),
        (20, '20€'),
        (50, '50€'),
        (100, '100€'),
        (150, '150€'),
        (250, '250€'),
        (500, '500€'),
        (1000, '1000€'),
        (3000, '3000€'),
        (5000, '5000€'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom du donateur")
    email = models.EmailField(verbose_name="Email")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant (€)")
    type_don = models.CharField(max_length=10, choices=TYPE_CHOICES, default='unique', verbose_name="Type de don")
    message = models.TextField(blank=True, null=True, verbose_name="Message (optionnel)")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    paypal_complete = models.BooleanField(default=False, verbose_name="Paiement PayPal complété")
    
    # Lien optionnel avec un utilisateur connecté
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilisateur")
    
    class Meta:
        verbose_name = "Don"
        verbose_name_plural = "Dons"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Don de {self.montant}€ par {self.nom}"

