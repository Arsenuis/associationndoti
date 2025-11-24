from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def ndoti_format(content):
    """
    Filtre simple et efficace pour formater les articles Ndoti
    """
    if not content:
        return ""
    
    # Normaliser les sauts de ligne
    content = content.replace('\r\n', '\n').replace('\r', '\n').strip()
    
    # === ÉTAPE 1: APPLIQUER LE MARKDOWN ===
    
    # Gras : **texte**
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="ndoti-bold">\1</strong>', content)
    
    # Italique : *texte* 
    content = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em class="ndoti-italic">\1</em>', content)
    
    # Surlignage jaune : ==texte==
    content = re.sub(r'==([^=]+)==', r'<span class="ndoti-highlight">\1</span>', content)
    
    # Vert Ndoti : ++texte++
    content = re.sub(r'\+\+([^+]+)\+\+', r'<span class="ndoti-green-text">\1</span>', content)
    
    # Rouge urgent : !!texte!!
    content = re.sub(r'!!([^!]+)!!', r'<span class="ndoti-urgent">\1</span>', content)
    
    # === ÉTAPE 2: CRÉER LES PARAGRAPHES ===
    
    # Diviser par doubles sauts de ligne OU créer des paragraphes automatiquement
    if '\n\n' in content:
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    else:
        # Diviser par phrases pour créer des paragraphes
        sentences = re.split(r'(?<=\.)\s+(?=[A-ZÀÁÂÄÇÉÈÊËÏÎÔÙÛÜŸÑ])', content)
        paragraphs = []
        current = ""
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            current += sentence + " "
            
            # Nouveau paragraphe toutes les 2 phrases OU si trop long
            if (i + 1) % 2 == 0 or len(current) > 250:
                paragraphs.append(current.strip())
                current = ""
        
        # Ajouter le dernier paragraphe
        if current.strip():
            paragraphs.append(current.strip())
    
    # === ÉTAPE 3: FORMATTER CHAQUE PARAGRAPHE ===
    
    formatted_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue
        
        # Premier paragraphe = introduction
        if i == 0:
            formatted_paragraphs.append(f'<p class="intro-paragraph">{paragraph}</p>')
        
        # Détecter les titres (MAJUSCULES)
        elif re.match(r'^[A-ZÀÁÂÄÇÉÈÊËÏÎÔÙÛÜŸÑ\s]{8,}$', paragraph.strip()):
            formatted_paragraphs.append(f'<h3 class="section-title">{paragraph.title()}</h3>')
        
        # Détecter les citations (commencent par guillemets)
        elif paragraph.strip().startswith(('"', '« ', '«')):
            formatted_paragraphs.append(f'<blockquote class="article-quote">{paragraph}</blockquote>')
        
        # Paragraphe normal
        else:
            # Mettre en évidence les chiffres automatiquement
            paragraph = re.sub(
                r'\b(\d+(?:[.,]\d+)?)\s*(%|€|\$|personnes?|enfants?|familles?|participants?)\b',
                r'<span class="stat-highlight">\1 \2</span>',
                paragraph, flags=re.IGNORECASE
            )
            
            formatted_paragraphs.append(f'<p>{paragraph}</p>')
    
    result = '\n'.join(formatted_paragraphs)
    return mark_safe(result)


@register.filter  
def simple_test(content):
    """Filtre de test ultra simple"""
    if not content:
        return ""
    
    # Juste remplacer **texte** par <strong>texte</strong>
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong style="color: #16a34a; font-weight: bold;">\1</strong>', content)
    
    # Et créer des paragraphes de base
    paragraphs = content.split('\n\n')
    result = ""
    for i, para in enumerate(paragraphs):
        if para.strip():
            if i == 0:
                result += f'<p class="intro-paragraph">{para.strip()}</p>\n'
            else:
                result += f"<p>{para.strip()}</p>\n"
    
    return mark_safe(result)