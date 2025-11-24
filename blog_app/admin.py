from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Article, Commentaire, Profile, Contact, GalerieMedia, Like, Don

# Formulaire personnalisé pour les articles
class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 20, 
                'cols': 80,
                'style': 'width: 100%; font-family: Georgia, serif; font-size: 14px; line-height: 1.6;',
                'placeholder': '''📝 GUIDE DE FORMATAGE NDOTI (Version Simplifiée) :

✨ FORMATAGE MANUEL (utilisez ces marqueurs) :
• **texte** → Texte en GRAS
• *texte* → Texte en italique

🤖 FORMATAGE AUTOMATIQUE :
• Premier paragraphe → Automatiquement mis en évidence
• MOTS EN MAJUSCULES → Automatiquement en gras
• "Citations" → Automatiquement stylées
• 150 personnes, 25% → Chiffres mis en valeur

📖 EXEMPLE D'UTILISATION :
L'association Ndoti a aidé **250 familles** cette année.
C'est un *résultat extraordinaire* qui montre notre engagement.

RÉSULTATS OBTENUS
Grâce à vos dons, nous avons pu scolariser 89 enfants...

"Cette citation importante sera mise en évidence automatiquement."

RÉSULTATS
- Premier point important
- Deuxième point à retenir
- Troisième élément clé

CONCLUSION
Votre conclusion synthétise les points essentiels...
'''
            })
        }

# Register the Article model to make it manageable via the admin interface
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('titre', 'auteur', 'statut_badge', 'date_publication', 'apercu_image')
    list_filter = ('statut', 'date_publication', 'auteur')
    search_fields = ('titre', 'contenu')
    readonly_fields = ('date_publication', 'apercu_image_detail')
    # list_editable retiré car on utilise statut_badge qui est une méthode
    date_hierarchy = 'date_publication'
    list_per_page = 20
    
    # Méthode pour afficher un badge de statut coloré
    def statut_badge(self, obj):
        if obj.statut == 'publie':
            return mark_safe(f'<span style="background: #91CD8C; color: white; padding: 5px 12px; border-radius: 20px; font-weight: 600;">✓ Publié</span>')
        else:
            return mark_safe(f'<span style="background: #fbbf24; color: #1a3009; padding: 5px 12px; border-radius: 20px; font-weight: 600;">✎ Brouillon</span>')
    statut_badge.short_description = 'Statut'
    
    # Aperçu miniature de l'image dans la liste
    def apercu_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />')
        return mark_safe('<span style="color: #999;">📷 Pas d\'image</span>')
    apercu_image.short_description = 'Image'
    
    # Aperçu plus grand dans le détail
    def apercu_image_detail(self, obj):
        if obj.image:
            return mark_safe(f'''
                <div style="text-align: center;">
                    <img src="{obj.image.url}" style="max-width: 500px; max-height: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
                    <p style="margin-top: 10px; color: #666;"><strong>URL:</strong> {obj.image.url}</p>
                </div>
            ''')
        return mark_safe('<p style="text-align: center; color: #999;">📷 Aucune image associée</p>')
    apercu_image_detail.short_description = 'Aperçu de l\'image'
    
    fieldsets = (
        ('📝 Contenu de l\'article', {
            'fields': ('titre', 'image', 'apercu_image_detail'),
            'description': mark_safe('<p style="color: #7ab874; font-weight: 500;">✨ Informations principales de votre article</p>')
        }),
        ('✍️ Rédaction', {
            'fields': ('contenu',),
            'description': mark_safe('''
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #f0f9f0 100%); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #91CD8C; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <h3 style="color: #2d5016; margin-top: 0; font-size: 18px; display: flex; align-items: center; gap: 8px;">
                    💡 Guide de rédaction Ndoti
                    <span style="background: #91CD8C; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">PRO</span>
                </h3>
                <p style="color: #2d5016; margin-bottom: 15px;"><strong>🤖 Votre texte sera automatiquement mis en forme !</strong></p>
                <ul style="color: #2d5016; line-height: 1.8; margin-bottom: 10px;">
                    <li><strong>Paragraphes :</strong> Séparez par des lignes vides pour une meilleure lisibilité</li>
                    <li><strong>Titres :</strong> Écrivez en MAJUSCULES (ex: <code>OBJECTIFS DE L'ACTION</code>)</li>
                    <li><strong>Citations :</strong> Utilisez des guillemets "Comme ceci"</li>
                    <li><strong>Listes :</strong> Commencez par un tiret <code>-</code> pour créer des points</li>
                    <li><strong>Statistiques :</strong> Les chiffres (150 personnes, 25%) seront mis en valeur automatiquement</li>
                    <li><strong>Emphase :</strong> Utilisez <code>**texte**</code> pour du gras et <code>*texte*</code> pour de l'italique</li>
                </ul>
                <div style="background: white; padding: 12px; border-radius: 8px; margin-top: 12px; border: 1px solid #91CD8C;">
                    <strong style="color: #91CD8C;">💬 Astuce Pro :</strong>
                    <span style="color: #666;">Rédigez naturellement, notre système intelligent s'occupe du formatage !</span>
                </div>
            </div>
            ''')
        }),
        ('📄 Publication', {
            'fields': ('auteur', 'statut', 'date_publication'),
            'classes': ('collapse',),
            'description': mark_safe('<p style="color: #7ab874;">⚙️ Paramètres de publication et métadonnées</p>')
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.auteur = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/ndoti-admin.css',)
        }


# Register the Commentaire model
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur_badge', 'article_link', 'extrait_commentaire', 'date_badge')
    list_filter = ('date', 'auteur')
    search_fields = ('contenu', 'auteur__username', 'article__titre')
    readonly_fields = ('date', 'apercu_commentaire')
    date_hierarchy = 'date'
    list_per_page = 25
    
    def auteur_badge(self, obj):
        return mark_safe(f'''
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #91CD8C; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600;">
                    {obj.auteur.username[0].upper()}
                </span>
                <span style="font-weight: 600; color: #2d5016;">{obj.auteur.username}</span>
            </div>
        ''')
    auteur_badge.short_description = 'Auteur'
    
    def article_link(self, obj):
        return mark_safe(f'<a href="/ndoti-admin-secure/blog_app/article/{obj.article.id}/change/" style="color: #91CD8C; text-decoration: none; font-weight: 500;">📰 {obj.article.titre[:40]}...</a>')
    article_link.short_description = 'Article'
    
    def extrait_commentaire(self, obj):
        extrait = obj.contenu[:60] + '...' if len(obj.contenu) > 60 else obj.contenu
        return mark_safe(f'<span style="color: #666; font-style: italic;">"{extrait}"</span>')
    extrait_commentaire.short_description = 'Commentaire'
    
    def date_badge(self, obj):
        return mark_safe(f'<span style="background: #fbbf24; color: #1a3009; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">📅 {obj.date.strftime("%d/%m/%Y")}</span>')
    date_badge.short_description = 'Date'
    
    def apercu_commentaire(self, obj):
        return mark_safe(f'''
            <div style="background: #f9fafb; padding: 20px; border-radius: 12px; border-left: 4px solid #91CD8C;">
                <p style="font-size: 16px; line-height: 1.8; color: #333; margin: 0;">{obj.contenu}</p>
            </div>
        ''')
    apercu_commentaire.short_description = 'Contenu complet'


# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')

# Register the Contact model
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom_badge', 'email_link', 'sujet_badge', 'date_envoi', 'statut_traitement')
    list_filter = ('sujet', 'traite', 'date_envoi')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('date_envoi', 'message_complet')
    date_hierarchy = 'date_envoi'
    list_per_page = 20
    
    def nom_badge(self, obj):
        return mark_safe(f'''
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #91CD8C; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 16px;">
                    {obj.nom[0].upper()}
                </span>
                <strong style="color: #2d5016;">{obj.nom}</strong>
            </div>
        ''')
    nom_badge.short_description = 'Contact'
    
    def email_link(self, obj):
        return mark_safe(f'<a href="mailto:{obj.email}" style="color: #91CD8C; text-decoration: none; font-weight: 500;">✉️ {obj.email}</a>')
    email_link.short_description = 'Email'
    
    def sujet_badge(self, obj):
        couleurs = {
            'general': '#3b82f6',
            'technique': '#ef4444',
            'partenariat': '#8b5cf6',
            'suggestion': '#10b981',
            'autre': '#6b7280'
        }
        couleur = couleurs.get(obj.sujet, '#6b7280')
        return mark_safe(f'<span style="background: {couleur}; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">{obj.get_sujet_display()}</span>')
    sujet_badge.short_description = 'Sujet'
    
    def statut_traitement(self, obj):
        if obj.traite:
            return mark_safe('<span style="background: #91CD8C; color: white; padding: 5px 12px; border-radius: 16px; font-weight: 600;">✓ Traité</span>')
        return mark_safe('<span style="background: #fbbf24; color: #1a3009; padding: 5px 12px; border-radius: 16px; font-weight: 600;">⏳ En attente</span>')
    statut_traitement.short_description = 'Statut'
    
    def message_complet(self, obj):
        return mark_safe(f'''
            <div style="background: #f9fafb; padding: 20px; border-radius: 12px; border-left: 4px solid #91CD8C;">
                <h4 style="color: #91CD8C; margin-top: 0;">Message de {obj.nom}</h4>
                <p style="font-size: 15px; line-height: 1.8; color: #333;">{obj.message}</p>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e5e7eb;">
                    <small style="color: #666;">
                        <strong>Sujet:</strong> {obj.get_sujet_display()} | 
                        <strong>Date:</strong> {obj.date_envoi.strftime("%d/%m/%Y à %H:%M")} |
                        <strong>Email:</strong> <a href="mailto:{obj.email}" style="color: #91CD8C;">{obj.email}</a>
                    </small>
                </div>
            </div>
        ''')
    message_complet.short_description = 'Message complet'
    
    fieldsets = (
        ('👤 Informations du contact', {
            'fields': ('nom', 'email', 'utilisateur')
        }),
        ('📧 Message', {
            'fields': ('sujet', 'message_complet')
        }),
        ('⚙️ Gestion', {
            'fields': ('traite', 'date_envoi')
        })
    )
    
    # Actions personnalisées
    def marquer_traite(self, request, queryset):
        queryset.update(traite=True)
    marquer_traite.short_description = "Marquer comme traité"
    
    def marquer_non_traite(self, request, queryset):
        queryset.update(traite=False)
    marquer_non_traite.short_description = "Marquer comme non traité"
    
    actions = ['marquer_traite', 'marquer_non_traite']


# Register the GalerieMedia model
@admin.register(GalerieMedia)
class GalerieMediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_media', 'categorie', 'date_evenement', 'actif', 'ordre', 'date_creation')
    list_filter = ('type_media', 'categorie', 'actif', 'date_creation', 'date_evenement')
    search_fields = ('titre', 'description', 'lieu')
    readonly_fields = ('date_creation', 'ajoute_par')
    list_editable = ('actif', 'ordre')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'type_media', 'categorie')
        }),
        ('Média', {
            'fields': ('image', 'video', 'video_url'),
            'description': 'Ajoutez soit une image, soit un fichier vidéo, soit une URL vidéo (YouTube, Vimeo, etc.)'
        }),
        ('Détails de l\'événement', {
            'fields': ('date_evenement', 'lieu'),
            'classes': ('collapse',)
        }),
        ('Paramètres d\'affichage', {
            'fields': ('actif', 'ordre')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'ajoute_par'),
            'classes': ('collapse',),
            'description': 'Informations automatiques'
        })
    )
    
    # Actions personnalisées
    def activer_medias(self, request, queryset):
        queryset.update(actif=True)
    activer_medias.short_description = "Activer les médias sélectionnés"
    
    def desactiver_medias(self, request, queryset):
        queryset.update(actif=False)
    desactiver_medias.short_description = "Désactiver les médias sélectionnés"
    
    actions = ['activer_medias', 'desactiver_medias']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.ajoute_par = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimise les requêtes avec select_related"""
        return super().get_queryset(request).select_related('ajoute_par')


# Register the Like model
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user_badge', 'content_link', 'type_badge', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('user__username', 'article__titre', 'media__titre')
    readonly_fields = ('date_creation', 'user', 'article', 'media')
    date_hierarchy = 'date_creation'
    list_per_page = 30
    
    def user_badge(self, obj):
        return mark_safe(f'''
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #91CD8C; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600;">
                    {obj.user.username[0].upper()}
                </span>
                <span style="font-weight: 600; color: #2d5016;">{obj.user.username}</span>
            </div>
        ''')
    user_badge.short_description = 'Utilisateur'
    
    def content_link(self, obj):
        if obj.article:
            return mark_safe(f'<a href="/ndoti-admin-secure/blog_app/article/{obj.article.id}/change/" style="color: #91CD8C; text-decoration: none; font-weight: 500;">📰 {obj.article.titre[:50]}...</a>')
        elif obj.media:
            return mark_safe(f'<a href="/ndoti-admin-secure/blog_app/galeriemedia/{obj.media.id}/change/" style="color: #91CD8C; text-decoration: none; font-weight: 500;">📸 {obj.media.titre[:50]}...</a>')
        return "Aucun contenu"
    content_link.short_description = 'Contenu liké'
    
    def type_badge(self, obj):
        if obj.article:
            return mark_safe('<span style="background: #3b82f6; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">📰 Article</span>')
        elif obj.media:
            return mark_safe('<span style="background: #8b5cf6; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">📸 Média</span>')
        return mark_safe('<span style="background: #6b7280; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">❓ Inconnu</span>')
    type_badge.short_description = 'Type'
    
    def has_add_permission(self, request):
        # Les likes sont créés via l'interface publique, pas l'admin
        return False
    
    def has_change_permission(self, request, obj=None):
        # Les likes ne peuvent pas être modifiés
        return False

# Admin pour les dons
@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'montant_badge', 'type_don_badge', 'email', 'paypal_badge', 'date_creation', 'utilisateur_link')
    list_filter = ('type_don', 'paypal_complete', 'date_creation', 'montant')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('date_creation', 'utilisateur')
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)
    
    fieldsets = (
        ('📋 Informations du donateur', {
            'fields': ('nom', 'email', 'utilisateur')
        }),
        ('💰 Détails du don', {
            'fields': ('montant', 'type_don', 'message')
        }),
        ('✅ Statut PayPal', {
            'fields': ('paypal_complete', 'date_creation')
        }),
    )
    
    def montant_badge(self, obj):
        """Affiche le montant avec un badge coloré"""
        if obj.montant >= 1000:
            color = '#10b981'  # Vert pour gros montants
        elif obj.montant >= 100:
            color = '#fbbf24'  # Jaune pour montants moyens
        else:
            color = '#91CD8C'  # Vert clair pour petits montants
        return mark_safe(f'<span style="background: {color}; color: white; padding: 5px 12px; border-radius: 16px; font-size: 13px; font-weight: 600;">💶 {obj.montant}€</span>')
    montant_badge.short_description = 'Montant'
    
    def type_don_badge(self, obj):
        """Affiche le type de don avec un badge"""
        if obj.type_don == 'unique':
            return mark_safe('<span style="background: #3b82f6; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">🎁 Don unique</span>')
        else:
            return mark_safe('<span style="background: #8b5cf6; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">🔄 Don mensuel</span>')
    type_don_badge.short_description = 'Type'
    
    def paypal_badge(self, obj):
        """Affiche le statut PayPal avec un badge"""
        if obj.paypal_complete:
            return mark_safe('<span style="background: #10b981; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">✅ Complété</span>')
        else:
            return mark_safe('<span style="background: #ef4444; color: white; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">⏳ En attente</span>')
    paypal_badge.short_description = 'Statut PayPal'
    
    def utilisateur_link(self, obj):
        """Affiche un lien vers le profil de l'utilisateur si disponible"""
        if obj.utilisateur:
            return mark_safe(f'<a href="/admin/auth/user/{obj.utilisateur.id}/change/" style="color: #91CD8C; font-weight: 600;">👤 {obj.utilisateur.username}</a>')
        return mark_safe('<span style="color: #9ca3af;">👤 Anonyme</span>')
    utilisateur_link.short_description = 'Utilisateur'
    
    def has_add_permission(self, request):
        # Les dons sont créés via l'interface publique, pas l'admin
        return False
