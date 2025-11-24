# 🔗 GUIDE DES LIENS RÉSEAUX SOCIAUX

**Date :** 21 octobre 2025  
**Projet :** Ndoti Blog  
**Objectif :** Intégrer les liens vers vos comptes Facebook, Instagram et WhatsApp

---

## 📱 **MODIFICATIONS EFFECTUÉES**

### ✅ **Page d'accueil** (`home.html`)
- ❌ **Supprimé :** Twitter
- ✅ **Conservé :** Facebook, Instagram  
- ✅ **Ajouté :** WhatsApp

### ✅ **Page contact** (`contact.html`)
- ❌ **Supprimé :** Twitter, LinkedIn
- ✅ **Conservé :** Facebook, Instagram
- ✅ **Ajouté :** WhatsApp

---

## 🎯 **OÙ AJOUTER VOS LIENS**

### 📍 **1. PAGE D'ACCUEIL** - Fichier: `blog_app/templates/home.html`

**Lignes à modifier (autour de 461-469) :**

```html
<!-- ⚠️ REMPLACEZ "#" PAR VOTRE LIEN FACEBOOK -->
<a href="#" target="_blank" rel="noopener" title="Facebook Ndoti">
    <i data-lucide="facebook"></i>
</a>
<!-- ⚠️ REMPLACEZ "#" PAR VOTRE LIEN INSTAGRAM -->
<a href="#" target="_blank" rel="noopener" title="Instagram Ndoti">
    <i data-lucide="instagram"></i>
</a>
<!-- ⚠️ REMPLACEZ "#" PAR VOTRE LIEN/NUMÉRO WHATSAPP -->
<a href="#" target="_blank" rel="noopener" title="WhatsApp Ndoti">
    <i data-lucide="message-circle"></i>
</a>
```

### 📍 **2. PAGE CONTACT** - Fichier: `blog_app/templates/contact.html`

**Lignes à modifier (autour de 226-238) :**

```html
<!-- ⚠️ REMPLACEZ "#" PAR VOTRE LIEN FACEBOOK -->
<a href="#" target="_blank" rel="noopener" title="Facebook Ndoti" class="btn btn-outline-primary btn-sm rounded-circle">
    <i class="fab fa-facebook-f"></i>
</a>
<!-- ⚠️ REMPLACEZ "#" PAR VOTRE LIEN INSTAGRAM -->
<a href="#" target="_blank" rel="noopener" title="Instagram Ndoti" class="btn btn-outline-primary btn-sm rounded-circle">
    <i class="fab fa-instagram"></i>
</a>
<!-- ⚠️ REMPLACEZ "#" PAR VOTRE LIEN/NUMÉRO WHATSAPP -->
<a href="#" target="_blank" rel="noopener" title="WhatsApp Ndoti" class="btn btn-outline-primary btn-sm rounded-circle">
    <i class="fab fa-whatsapp"></i>
</a>
```

---

## 🔧 **COMMENT REMPLACER LES LIENS**

### 📘 **Facebook**
**Remplacez :** `href="#"`  
**Par :** `href="https://facebook.com/VOTRE_PAGE_FACEBOOK"`

**Exemple :**
```html
<a href="https://facebook.com/associationndoti" target="_blank">
```

### 📸 **Instagram**
**Remplacez :** `href="#"`  
**Par :** `href="https://instagram.com/VOTRE_COMPTE_INSTAGRAM"`

**Exemple :**
```html
<a href="https://instagram.com/ndoti_association" target="_blank">
```

### 💬 **WhatsApp**
**Option A - Lien vers chat direct :**
**Remplacez :** `href="#"`  
**Par :** `href="https://wa.me/VOTRE_NUMERO"`

**Exemple :**
```html
<a href="https://wa.me/33123456789" target="_blank">
```

**Option B - Lien avec message pré-rempli :**
```html
<a href="https://wa.me/33123456789?text=Bonjour%20Association%20Ndoti" target="_blank">
```

---

## 📝 **ÉTAPES À SUIVRE**

### 1. **Ouvrir les fichiers**
- `blog_app/templates/home.html`
- `blog_app/templates/contact.html`

### 2. **Rechercher les commentaires**
Cherchez les lignes contenant : `⚠️ REMPLACEZ "#"`

### 3. **Remplacer les liens**
- Changez `href="#"` par vos vrais liens
- Gardez `target="_blank" rel="noopener"`

### 4. **Tester**
- Redémarrez le serveur Django
- Vérifiez que les liens s'ouvrent correctement

---

## 🎨 **STYLES APPLIQUÉS**

### **Page d'accueil :**
- Icônes circulaires avec fond vert Ndoti
- Effet hover avec animation
- Utilisation des icônes Lucide

### **Page contact :**
- Boutons circulaires avec bordure
- Icônes Font Awesome (plus détaillées)
- Alignement centré

---

## ⚠️ **IMPORTANT**

### **Format des numéros WhatsApp :**
- **International :** `33123456789` (sans le +)
- **Avec indicatif :** Toujours commencer par l'indicatif pays
- **Sans espaces ni tirets**

### **Test des liens :**
Après modification, testez chaque lien pour vérifier qu'ils :
- ✅ S'ouvrent dans un nouvel onglet
- ✅ Mènent vers la bonne page/chat
- ✅ Fonctionnent sur mobile et desktop

---

## 📞 **EXEMPLE COMPLET**

```html
<!-- Page d'accueil - Facebook -->
<a href="https://facebook.com/associationndoti" target="_blank" rel="noopener" title="Facebook Ndoti">
    <i data-lucide="facebook"></i>
</a>

<!-- Page d'accueil - Instagram -->
<a href="https://instagram.com/ndoti_asso" target="_blank" rel="noopener" title="Instagram Ndoti">
    <i data-lucide="instagram"></i>
</a>

<!-- Page d'accueil - WhatsApp -->
<a href="https://wa.me/33123456789?text=Bonjour%20Association%20Ndoti" target="_blank" rel="noopener" title="WhatsApp Ndoti">
    <i data-lucide="message-circle"></i>
</a>
```

---

**🎯 Une fois les liens mis à jour, vos visiteurs pourront directement accéder à vos réseaux sociaux depuis le blog !**