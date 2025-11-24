from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Article, Commentaire, Profile, Contact, GalerieMedia, Like, Don
from .forms import CustomUserCreationForm, CommentaireForm, ProfileForm, UserUpdateForm, CustomPasswordChangeForm, ContactForm, DonForm

# Page d'accueil avec les derniers articles
def home(request):
    articles = Article.objects.filter(statut='publie').order_by('-date_publication')[:6]
    return render(request, 'home.html', {'articles': articles})

# Liste de tous les articles avec recherche (B.3)
def article_list(request):
    articles = Article.objects.filter(statut='publie').order_by('-date_publication')
    
    # B.3 - Système de recherche
    query = request.GET.get('q', None)  # None si pas de paramètre 'q'
    
    # Si le paramètre 'q' existe mais est vide ou juste des espaces, rediriger
    if query is not None:
        query = query.strip()
        if not query:  # Si vide après strip
            return redirect('/articles/')  # Redirection pour nettoyer l'URL
    else:
        query = ''  # Pas de paramètre 'q' du tout
    
    # Filtrer seulement si query a du contenu réel
    if query:
        from django.db.models import Q
        articles = articles.filter(
            Q(titre__icontains=query) | 
            Q(contenu__icontains=query) |
            Q(auteur__username__icontains=query)
        )
    
    context = {
        'articles': articles,
        'query': query,  # Pour afficher la recherche dans le formulaire
    }
    return render(request, 'articles/article_list.html', context)

# Détail d'un article avec commentaires
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, statut='publie')
    commentaires = article.commentaires.all().order_by('-date')
    
    # A.1 - Calcul du temps de lecture (basé sur 200 mots/minute)
    nombre_mots = len(article.contenu.split())
    temps_lecture = max(1, round(nombre_mots / 200))
    
    # B.2 - Navigation article précédent/suivant
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

# Inscription des utilisateurs
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connecter automatiquement l'utilisateur après inscription
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Votre compte a été créé avec succès.')
            return redirect('profil')  # Rediriger vers le profil après inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Vue profil utilisateur
@login_required
def profil(request):
    """Affichage du profil de l'utilisateur connecté"""
    user = request.user
    
    # Récupérer ou créer le profil
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Récupérer les commentaires de l'utilisateur
    commentaires_utilisateur = Commentaire.objects.filter(auteur=user).order_by('-date')[:10]
    
    # Calculer la dernière activité (dernier commentaire ou date de connexion)
    dernier_commentaire = Commentaire.objects.filter(auteur=user).order_by('-date').first()
    if dernier_commentaire:
        derniere_activite = dernier_commentaire.date
    else:
        derniere_activite = user.last_login or user.date_joined
    
    # Statistiques utilisateur
    stats = {
        'total_commentaires': Commentaire.objects.filter(auteur=user).count(),
        'articles_commentes': Commentaire.objects.filter(auteur=user).values('article').distinct().count(),
        'derniere_activite': derniere_activite,
    }
    
    context = {
        'user': user,
        'profile': profile,
        'commentaires_recents': commentaires_utilisateur,
        'stats': stats,
    }
    return render(request, 'profil/profil.html', context)

# Vue profil public d'un utilisateur
def profil_public(request, user_id):
    """Affichage du profil public d'un utilisateur"""
    user = get_object_or_404(User, id=user_id)
    
    # Récupérer le profil
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    # Récupérer les commentaires publics de l'utilisateur
    commentaires_utilisateur = Commentaire.objects.filter(auteur=user).order_by('-date')[:5]
    
    # Calculer la dernière activité (dernier commentaire ou date de connexion)
    dernier_commentaire = Commentaire.objects.filter(auteur=user).order_by('-date').first()
    if dernier_commentaire:
        derniere_activite = dernier_commentaire.date
    else:
        derniere_activite = user.last_login or user.date_joined
    
    # Statistiques utilisateur
    stats = {
        'total_commentaires': Commentaire.objects.filter(auteur=user).count(),
        'articles_commentes': Commentaire.objects.filter(auteur=user).values('article').distinct().count(),
        'derniere_activite': derniere_activite,
    }
    
    context = {
        'user_profile': user,
        'profile': profile,
        'commentaires_recents': commentaires_utilisateur,
        'stats': stats,
    }
    return render(request, 'profil/profil_public.html', context)

# Vue de debug pour tester les profils
def debug_profil(request):
    """Page de debug pour tester le système de profils"""
    return render(request, 'debug_profil.html')

@login_required
def edit_profil(request):
    """Vue pour éditer le profil utilisateur"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profil')
        else:
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'profil/edit_profil.html', context)

@login_required
def change_password(request):
    """Vue pour changer le mot de passe"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour garder l'utilisateur connecté
            messages.success(request, 'Votre mot de passe a été modifié avec succès!')
            return redirect('profil')
        else:
            messages.error(request, 'Une erreur s\'est produite. Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form
    }
    return render(request, 'profil/change_password.html', context)

@login_required
def delete_account(request):
    """Vue pour supprimer le compte utilisateur"""
    if request.method == 'POST':
        if request.POST.get('confirm_delete') == 'SUPPRIMER':
            user = request.user
            user.delete()
            messages.success(request, 'Votre compte a été supprimé avec succès.')
            return redirect('home')
        else:
            messages.error(request, 'Veuillez taper "SUPPRIMER" pour confirmer la suppression de votre compte.')
    
    return render(request, 'profil/delete_account.html')

def contact(request):
    """Vue pour le formulaire de contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            contact_message = form.save(commit=False)
            # Si l'utilisateur est connecté, lier le message à son compte
            if request.user.is_authenticated:
                contact_message.utilisateur = request.user
            contact_message.save()
            
            messages.success(
                request, 
                f'Merci {contact_message.nom} ! Votre message a été envoyé avec succès. '
                'Nous vous répondrons dans les plus brefs délais.'
            )
            return redirect('contact')
        else:
            messages.error(request, 'Une erreur s\'est produite. Veuillez corriger les informations ci-dessous.')
    else:
        form = ContactForm(user=request.user if request.user.is_authenticated else None)
    
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


# Vues pour la galerie
def galerie(request):
    """Vue principale de la galerie avec filtrage par catégorie et type"""
    # Récupérer les paramètres de filtrage
    categorie_filter = request.GET.get('categorie', '')
    type_filter = request.GET.get('type', '')
    
    # Requête de base : médias actifs seulement
    medias = GalerieMedia.objects.filter(actif=True)
    
    # Appliquer les filtres
    if categorie_filter:
        medias = medias.filter(categorie=categorie_filter)
    if type_filter:
        medias = medias.filter(type_media=type_filter)
    
    # Ordonner par ordre d'affichage puis par date
    medias = medias.order_by('-ordre', '-date_creation')
    
    # Récupérer toutes les catégories disponibles pour le filtre
    categories_disponibles = GalerieMedia.objects.filter(actif=True).values_list('categorie', flat=True).distinct()
    
    # Statistiques pour l'affichage
    total_medias = medias.count()
    total_images = medias.filter(type_media='image').count()
    total_videos = medias.filter(type_media='video').count()
    
    context = {
        'medias': medias,
        'categories_disponibles': categories_disponibles,
        'categorie_choices': GalerieMedia.CATEGORIE_CHOICES,
        'type_choices': GalerieMedia.TYPE_CHOICES,
        'categorie_filter': categorie_filter,
        'type_filter': type_filter,
        'total_medias': total_medias,
        'total_images': total_images,
        'total_videos': total_videos,
    }
    return render(request, 'galerie/galerie.html', context)


def galerie_detail(request, media_id):
    """Vue détaillée d'un média de la galerie"""
    media = get_object_or_404(GalerieMedia, id=media_id, actif=True)
    
    # Récupérer les médias suivant et précédent de la même catégorie
    media_precedent = GalerieMedia.objects.filter(
        actif=True,
        categorie=media.categorie,
        id__lt=media.id
    ).order_by('-id').first()
    
    media_suivant = GalerieMedia.objects.filter(
        actif=True,
        categorie=media.categorie,
        id__gt=media.id
    ).order_by('id').first()
    
    # Récupérer d'autres médias de la même catégorie (max 6)
    medias_similaires = GalerieMedia.objects.filter(
        actif=True,
        categorie=media.categorie
    ).exclude(id=media.id).order_by('-ordre', '-date_creation')[:6]
    
    # Vérifier si l'utilisateur a liké ce média
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(user=request.user, media=media).exists()
    
    context = {
        'media': media,
        'media_precedent': media_precedent,
        'media_suivant': media_suivant,
        'medias_similaires': medias_similaires,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'galerie/detail.html', context)


# ============================================
# 💚 SYSTÈME DE LIKES
# ============================================

@login_required
@require_POST
def toggle_like_article(request, article_id):
    """
    Vue pour liker/unliker un article
    Retourne une réponse JSON pour une mise à jour AJAX
    """
    article = get_object_or_404(Article, id=article_id, statut='publie')
    
    # Vérifier si l'utilisateur a déjà liké cet article
    like_exists = Like.objects.filter(user=request.user, article=article).first()
    
    if like_exists:
        # Unlike : supprimer le like
        like_exists.delete()
        liked = False
        message = "Vous n'aimez plus cet article"
    else:
        # Like : créer un nouveau like
        Like.objects.create(user=request.user, article=article)
        liked = True
        message = "Vous aimez cet article !"
    
    # Retourner une réponse JSON
    return JsonResponse({
        'success': True,
        'liked': liked,
        'total_likes': article.total_likes(),
        'message': message
    })


@login_required
@require_POST
def toggle_like_media(request, media_id):
    """
    Vue pour liker/unliker un média de galerie
    Retourne une réponse JSON pour une mise à jour AJAX
    """
    media = get_object_or_404(GalerieMedia, id=media_id, actif=True)
    
    # Vérifier si l'utilisateur a déjà liké ce média
    like_exists = Like.objects.filter(user=request.user, media=media).first()
    
    if like_exists:
        # Unlike : supprimer le like
        like_exists.delete()
        liked = False
        message = "Vous n'aimez plus ce média"
    else:
        # Like : créer un nouveau like
        Like.objects.create(user=request.user, media=media)
        liked = True
        message = "Vous aimez ce média !"
    
    # Retourner une réponse JSON
    return JsonResponse({
        'success': True,
        'liked': liked,
        'total_likes': media.total_likes(),
        'message': message
    })


# ======================
# VUES POUR LES DONS
# ======================

def faire_un_don(request):
    """
    Vue pour afficher le formulaire de don et gérer la soumission
    """
    if request.method == 'POST':
        form = DonForm(request.POST, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            don = form.save(commit=False)
            
            # Associer l'utilisateur connecté s'il existe
            if request.user.is_authenticated:
                don.utilisateur = request.user
            
            don.save()
            
            # Stocker l'ID du don en session pour pouvoir le mettre à jour après PayPal
            request.session['don_id'] = don.id
            
            messages.success(request, f'Merci {don.nom} ! Vous allez être redirigé vers PayPal pour finaliser votre don de {don.montant}€.')
            
            # Rediriger vers PayPal
            return redirect('paypal_redirect', don_id=don.id)
    else:
        form = DonForm(user=request.user if request.user.is_authenticated else None)
    
    context = {
        'form': form,
        'page_title': 'Faire un don à Ndoti',
    }
    return render(request, 'dons/faire_un_don.html', context)


def paypal_redirect(request, don_id):
    """
    Vue pour rediriger vers PayPal avec les informations du don
    """
    don = get_object_or_404(Don, id=don_id)
    
    # URL PayPal (pour l'instant, redirection simple vers la page PayPal.me)
    paypal_url = f"https://www.paypal.com/paypalme/NdotiAssociation/{don.montant}"
    
    context = {
        'don': don,
        'paypal_url': paypal_url,
        'page_title': 'Redirection vers PayPal',
    }
    return render(request, 'dons/paypal_redirect.html', context)


def don_success(request):
    """
    Vue de confirmation après un don réussi via PayPal
    """
    don_id = request.session.get('don_id')
    
    if don_id:
        don = get_object_or_404(Don, id=don_id)
        # Marquer le don comme complété
        don.paypal_complete = True
        don.save()
        
        # Nettoyer la session
        del request.session['don_id']
        
        messages.success(request, f'Merci infiniment {don.nom} pour votre don de {don.montant}€ ! Votre générosité fait la différence pour Ndoti.')
        
        context = {
            'don': don,
            'page_title': 'Don réussi',
        }
        return render(request, 'dons/don_success.html', context)
    else:
        messages.warning(request, 'Aucun don en cours.')
        return redirect('home')


def don_cancel(request):
    """
    Vue si l'utilisateur annule le paiement PayPal
    """
    messages.info(request, 'Votre don a été annulé. Vous pouvez réessayer à tout moment.')
    return redirect('faire_un_don')
