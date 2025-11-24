# Script pour créer des données de test pour la galerie
# Exécuter avec: python manage.py shell < test_galerie.py

from django.contrib.auth.models import User
from blog_app.models import GalerieMedia
from datetime import date, datetime

# Récupérer ou créer un utilisateur admin
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@ndoti.com'}
)

if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("Utilisateur admin créé")

# Créer des médias de test
medias_test = [
    {
        'titre': 'Formation professionnelle des jeunes',
        'description': 'Session de formation en informatique pour les jeunes du quartier. Cette formation a permis à 25 jeunes d\'apprendre les bases de la programmation et du développement web.',
        'type_media': 'image',
        'categorie': 'formation',
        'date_evenement': date(2024, 10, 15),
        'lieu': 'Centre Ndoti, Kinshasa',
        'ajoute_par': admin_user,
        'ordre': 10
    },
    {
        'titre': 'Sensibilisation dans les écoles',
        'description': 'Campagne de sensibilisation sur l\'importance de l\'éducation et la découverte des talents cachés chez les jeunes.',
        'type_media': 'video',
        'categorie': 'sensibilisation',
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # URL d'exemple
        'date_evenement': date(2024, 9, 20),
        'lieu': 'École Primaire de Kinshasa',
        'ajoute_par': admin_user,
        'ordre': 9
    },
    {
        'titre': 'Événement communautaire',
        'description': 'Grande fête communautaire organisée par Ndoti pour rassembler les familles et célébrer les réussites de nos jeunes.',
        'type_media': 'image',
        'categorie': 'evenement',
        'date_evenement': date(2024, 8, 12),
        'lieu': 'Place centrale de Kinshasa',
        'ajoute_par': admin_user,
        'ordre': 8
    },
    {
        'titre': 'Action de terrain - Distribution de fournitures',
        'description': 'Distribution de fournitures scolaires aux enfants défavorisés dans le cadre de notre mission d\'accompagnement éducatif.',
        'type_media': 'image',
        'categorie': 'action',
        'date_evenement': date(2024, 7, 30),
        'lieu': 'Quartier populaire de Kinshasa',
        'ajoute_par': admin_user,
        'ordre': 7
    },
    {
        'titre': 'Partenariat avec les entreprises locales',
        'description': 'Signature d\'un partenariat stratégique avec plusieurs entreprises locales pour faciliter l\'insertion professionnelle de nos jeunes.',
        'type_media': 'video',
        'categorie': 'partenariat',
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'date_evenement': date(2024, 6, 18),
        'lieu': 'Siège de Ndoti',
        'ajoute_par': admin_user,
        'ordre': 6
    }
]

# Créer les médias s'ils n'existent pas déjà
for media_data in medias_test:
    media, created = GalerieMedia.objects.get_or_create(
        titre=media_data['titre'],
        defaults=media_data
    )
    if created:
        print(f"Média créé: {media.titre}")
    else:
        print(f"Média existe déjà: {media.titre}")

print(f"Total des médias dans la galerie: {GalerieMedia.objects.count()}")