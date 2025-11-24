# Guide d'utilisation de la Galerie Ndoti

## 📸 Galerie Ndoti - Guide Administrateur

### Vue d'ensemble
La galerie Ndoti permet de partager et mettre en valeur les actions, événements et moments marquants de l'association. Les administrateurs peuvent facilement ajouter, modifier et organiser les médias via l'interface d'administration Django.

### 🔧 Fonctionnalités principales

#### Pour les administrateurs :
- **Ajout de médias** : Images et vidéos (fichiers locaux ou URLs YouTube/Vimeo)
- **Catégorisation** : Organisation par type d'activité (événement, formation, action, etc.)
- **Ordre d'affichage** : Contrôle de la position des médias dans la galerie
- **Gestion du statut** : Activation/désactivation des médias
- **Métadonnées complètes** : Titre, description, lieu, date de l'événement

#### Pour les visiteurs :
- **Navigation intuitive** : Grille responsive avec filtres par catégorie et type
- **Vue détaillée** : Affichage complet avec métadonnées et médias similaires
- **Lightbox pour images** : Zoom et navigation fluide
- **Intégration vidéo** : Support YouTube/Vimeo et vidéos locales
- **Design moderne** : Interface cohérente avec la charte Ndoti

### 📝 Comment ajouter un média

1. **Accéder à l'administration** : `/admin/`
2. **Aller dans "Galerie"** → "Médias de galerie"
3. **Cliquer "Ajouter média de galerie"**
4. **Remplir les informations** :
   - Titre et description
   - Type de média (Image ou Vidéo)
   - Catégorie (Événement, Formation, Action, etc.)
   - Fichier média OU URL vidéo
   - Date et lieu de l'événement
   - Ordre d'affichage (plus élevé = affiché en premier)

### 🎯 Types de médias supportés

#### Images :
- Formats : JPG, PNG, GIF, WebP
- Taille recommandée : 1920x1080px minimum
- Optimisation automatique pour l'affichage web

#### Vidéos :
- **Fichiers locaux** : MP4, WebM (max 100MB recommandé)
- **URLs externes** : YouTube, Vimeo, etc.
- **Miniatures automatiques** : Générées pour YouTube

### 🏷️ Catégories disponibles

- **Événement** : Fêtes, célébrations, rassemblements
- **Action de terrain** : Interventions directes, aide communautaire
- **Formation** : Sessions éducatives, ateliers
- **Sensibilisation** : Campagnes de communication
- **Partenariat** : Collaborations, signatures d'accords
- **Autre** : Contenu divers

### 🚀 Bonnes pratiques

1. **Titres descriptifs** : Utilisez des titres clairs et engageants
2. **Descriptions complètes** : Contextualisez chaque média
3. **Dates précises** : Indiquez la date réelle de l'événement
4. **Lieux spécifiques** : Mentionnez la localisation exacte
5. **Ordre logique** : Organisez par importance ou chronologie
6. **Qualité des images** : Privilégiez des images haute résolution
7. **Métadonnées cohérentes** : Maintenez une nomenclature uniforme

### 🔗 Intégration

La galerie est automatiquement intégrée dans :
- **Navigation principale** : Lien "Galerie" dans le menu
- **Page d'accueil** : Bouton "Voir notre galerie" dans la section CTA
- **Administration** : Interface complète pour la gestion

### 📱 Responsive Design

La galerie s'adapte automatiquement à tous les écrans :
- **Desktop** : Grille 3 colonnes avec animations
- **Tablette** : Grille 2 colonnes optimisée
- **Mobile** : Colonne unique avec navigation tactile

### 🎨 Cohérence visuelle

Tous les éléments respectent la charte graphique Ndoti :
- **Couleurs** : Vert principal (#91CD8C) et jaune (#fbbf24)
- **Typographie** : Cohérente avec le reste du site
- **Animations** : Transitions fluides et modernes

---

**💡 Astuce** : Pour un impact maximal, alternez entre images et vidéos dans votre galerie et mettez régulièrement à jour le contenu pour maintenir l'engagement des visiteurs.