from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),

    # Authentification
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logout.html'
    ), name='logout'),
    
    # Profils utilisateur
    path('profil/', views.profil, name='profil'),
    path('profil/edit/', views.edit_profil, name='edit_profil'),
    path('profil/change-password/', views.change_password, name='change_password'),
    path('profil/delete-account/', views.delete_account, name='delete_account'),
    path('profil/<str:username>/', views.profil_public, name='profil_public'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Galerie
    path('galerie/', views.galerie, name='galerie'),
    path('galerie/<int:media_id>/', views.galerie_detail, name='galerie_detail'),
    
    # Likes
    path('articles/<int:article_id>/like/', views.toggle_like_article, name='toggle_like_article'),
    path('galerie/<int:media_id>/like/', views.toggle_like_media, name='toggle_like_media'),
    
    # Dons
    path('faire-un-don/', views.faire_un_don, name='faire_un_don'),
    path('dons/paypal/<int:don_id>/', views.paypal_redirect, name='paypal_redirect'),
    path('dons/success/', views.don_success, name='don_success'),
    path('dons/cancel/', views.don_cancel, name='don_cancel'),
    
    # Debug
    path('debug-profil/', views.debug_profil, name='debug_profil'),
]

