# 🔐 Guide d'accès administrateur - Ndoti Blog

## 📋 Informations de connexion

### URL d'administration
```
🌐 Production : https://votre-domaine.com/ndoti-admin-secure/
🛠️ Développement : http://localhost:8000/ndoti-admin-secure/
```

### Identifiants (à communiquer séparément au client)
- **Nom d'utilisateur :** [À remplir]
- **Mot de passe :** [À communiquer de manière sécurisée]

---

## 🛡️ Options de sécurisation recommandées

### Option 1 : URL personnalisée (APPLIQUÉE ✅)
L'URL a été changée de `/admin/` vers `/ndoti-admin-secure/` :
```python
# Dans blog_projet/urls.py
urlpatterns = [
    path('ndoti-admin-secure/', admin.site.urls),  # URL personnalisée ACTIVE
    path('', include('blog_app.urls')),
]
```

### Option 2 : Accès via lien privé dans le footer
Ajouter un lien discret visible seulement pour les administrateurs connectés.

### Option 3 : Page de connexion dédiée
Créer une page intermédiaire avec authentification supplémentaire.

---

## 📱 Comment le client accèdera à l'administration

### 1. **Marque-page/Favori** (CONFIGURATION ACTIVE ✅)
- Le client sauvegarde l'URL d'admin dans ses favoris
- URL secrète : `https://votre-domaine.com/ndoti-admin-secure/`
- Accès direct et sécurisé (Option A choisie)

### 2. **URL directe**
- Taper manuellement : `https://votre-domaine.com/ndoti-admin-secure/`
- Aucun lien visible sur le site public pour maximum de sécurité

### 3. **Communication privée** ✅
- L'URL d'administration sera communiquée au client en privé
- Aucune exposition publique de l'interface d'administration

---

## 🎯 Fonctionnalités disponibles dans l'admin

✅ **Gestion des articles**
- Créer, modifier, supprimer des articles
- Gérer le statut (brouillon/publié)
- Upload d'images

✅ **Gestion des utilisateurs**
- Voir les inscriptions
- Gérer les rôles et permissions
- Modérer les commentaires

✅ **Gestion des commentaires**
- Approuver/rejeter les commentaires
- Supprimer les spams

---

## 🔒 Bonnes pratiques de sécurité

1. **Mot de passe fort** : Au moins 12 caractères avec majuscules, minuscules, chiffres et symboles
2. **Connexion sécurisée** : Toujours utiliser HTTPS en production
3. **Sessions** : Se déconnecter après utilisation
4. **Accès limité** : Ne partager les identifiants qu'avec les personnes autorisées
5. **Surveillance** : Vérifier régulièrement les logs de connexion

---

## 📞 Support technique

En cas de problème d'accès :
1. Vérifier l'URL (avec ou sans slash final)
2. Vérifier les identifiants (attention à la casse)
3. Effacer le cache du navigateur
4. Contacter le développeur si le problème persiste