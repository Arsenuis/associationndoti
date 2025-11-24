/**
 * 💚 Système de Likes Ndoti
 * Gestion AJAX des likes pour articles et médias
 */

// Fonction pour gérer le like/unlike d'un article
function toggleLike(contentType, contentId) {
    const button = document.getElementById(`like-btn-${contentType}-${contentId}`);
    const icon = button.querySelector('.like-icon');
    const countSpan = button.querySelector('.like-count');
    
    // URL de l'action selon le type de contenu
    const url = contentType === 'article' 
        ? `/articles/${contentId}/like/` 
        : `/galerie/${contentId}/like/`;
    
    // Désactiver le bouton pendant la requête
    button.disabled = true;
    
    // Requête AJAX
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
                // Liked : cœur plein rouge
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = '#ef4444';
                button.classList.add('liked');
            } else {
                // Unliked : cœur vide vert
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = '#91CD8C';
                button.classList.remove('liked');
            }
            
            // Mise à jour du compteur
            countSpan.textContent = data.total_likes;
            
            // Animation du bouton
            button.classList.add('pulse-animation');
            setTimeout(() => {
                button.classList.remove('pulse-animation');
            }, 300);
            
            // Message toast (optionnel)
            showToast(data.message, data.liked ? 'success' : 'info');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showToast('Une erreur s\'est produite', 'error');
    })
    .finally(() => {
        // Réactiver le bouton
        button.disabled = false;
    });
}

// Fonction pour récupérer le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fonction pour afficher un message toast
function showToast(message, type = 'info') {
    // Créer le toast s'il n'existe pas
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(toastContainer);
    }
    
    // Créer le toast
    const toast = document.createElement('div');
    toast.className = `toast-message toast-${type}`;
    
    // Couleurs selon le type
    const colors = {
        success: '#91CD8C',
        error: '#ef4444',
        info: '#fbbf24'
    };
    
    toast.style.cssText = `
        background: white;
        color: #1f2937;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 10px;
        border-left: 4px solid ${colors[type] || colors.info};
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideIn 0.3s ease-out;
        min-width: 250px;
    `;
    
    // Icône selon le type
    const icons = {
        success: '<i class="fas fa-heart" style="color: #ef4444;"></i>',
        error: '<i class="fas fa-exclamation-circle" style="color: #ef4444;"></i>',
        info: '<i class="fas fa-heart-broken" style="color: #fbbf24;"></i>'
    };
    
    toast.innerHTML = `
        ${icons[type] || icons.info}
        <span style="font-weight: 500;">${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Supprimer automatiquement après 3 secondes
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Ajouter les animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }
    
    .pulse-animation {
        animation: pulse 0.3s ease-in-out;
    }
    
    .like-button {
        transition: all 0.3s ease;
    }
    
    .like-button:hover {
        transform: translateY(-2px);
    }
    
    .like-button:active {
        transform: translateY(0);
    }
`;
document.head.appendChild(style);
