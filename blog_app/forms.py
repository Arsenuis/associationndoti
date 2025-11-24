from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Commentaire, Profile, Contact, Don

# Formulaire d'inscription personnalisé
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Mot de passe"}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirmer mot de passe"}),
        }

# Formulaire de connexion personnalisé
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Mot de passe"})
    )

# Formulaire pour les commentaires
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Partagez votre réflexion sur cet article...',
                'rows': 4,
                'style': 'resize: vertical; border-color: var(--ndoti-green);'
            })
        }
        labels = {
            'contenu': 'Votre commentaire'
        }

# Formulaire pour éditer le profil utilisateur
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Choisissez une image JPG ou PNG de maximum 5MB'
            })
        }
        labels = {
            'avatar': 'Photo de profil'
        }

# Formulaire pour modifier les informations utilisateur
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur',
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'adresse@email.com',
                'autocomplete': 'email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de famille',
                'autocomplete': 'family-name'
            })
        }
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse email',
            'first_name': 'Prénom',
            'last_name': 'Nom'
        }

# Formulaire personnalisé pour changer le mot de passe
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe actuel',
            'autocomplete': 'current-password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe',
            'autocomplete': 'new-password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le nouveau mot de passe',
            'autocomplete': 'new-password'
        })
        
        # Mise à jour des labels
        self.fields['old_password'].label = 'Mot de passe actuel'
        self.fields['new_password1'].label = 'Nouveau mot de passe'
        self.fields['new_password2'].label = 'Confirmer le nouveau mot de passe'

# Formulaire de contact
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre@email.com',
                'autocomplete': 'email'
            }),
            'sujet': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez votre demande, question ou suggestion en détail...',
                'rows': 6,
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'nom': 'Nom complet',
            'email': 'Adresse email',
            'sujet': 'Sujet de votre message',
            'message': 'Votre message'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si un utilisateur est connecté, pré-remplir ses informations
        if user and user.is_authenticated:
            self.fields['nom'].initial = f"{user.first_name} {user.last_name}".strip() or user.username
            self.fields['email'].initial = user.email

# Formulaire de don
class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['nom', 'email', 'montant', 'type_don', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre@email.com',
                'autocomplete': 'email'
            }),
            'montant': forms.Select(attrs={
                'class': 'form-select',
                'id': 'montant-select'
            }),
            'type_don': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message optionnel pour l\'association (sera visible dans nos remerciements)...',
                'rows': 4,
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'nom': 'Nom complet',
            'email': 'Adresse email',
            'montant': 'Montant du don',
            'type_don': 'Type de don',
            'message': 'Message (optionnel)'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si un utilisateur est connecté, pré-remplir ses informations
        if user and user.is_authenticated:
            self.fields['nom'].initial = f"{user.first_name} {user.last_name}".strip() or user.username
            self.fields['email'].initial = user.email
            
        # Rendre le message optionnel
        self.fields['message'].required = False
