from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

def apply_markdown_formatting(text):
    """Applique le formatage Markdown simple - Version simplifiée"""
    # Gras : **texte**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="ndoti-bold">\1</strong>', text)
    
    # Italique : *texte*
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em class="ndoti-italic">\1</em>', text)
    
    return text

@register.filter
def smart_format(content):
    """
    Filtre Django pour formater automatiquement le contenu des articles
    avec une mise en forme intelligente basée sur des patterns textuels.
    """
    if not content:
        return ""
    
    # === ÉTAPE 1: FORMATAGE MARKDOWN SIMPLE ===
    
    # Gras : **texte** → <strong>texte</strong>
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="ndoti-bold">\1</strong>', content)
    
    # Italique : *texte* → <em>texte</em> (attention à ne pas confondre avec **)
    content = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em class="ndoti-italic">\1</em>', content)
    
    # === ÉTAPE 2: DIVISION EN PARAGRAPHES ===
    
    # Normaliser les sauts de ligne
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Diviser en paragraphes (double saut de ligne OU phrases longues)
    if '\n\n' in content:
        paragraphs = content.split('\n\n')
    else:
        # Diviser par points + majuscule
        sentences = re.split(r'(?<=\.)\s+(?=[A-ZÀÁÂÄÇÉÈÊËÏÎÔÙÛÜŸÑ])', content.strip())
        paragraphs = []
        current_para = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            current_para += sentence + " "
            if len(current_para) > 200:  # Nouveau paragraphe si trop long
                paragraphs.append(current_para.strip())
                current_para = ""
        
        if current_para.strip():
            paragraphs.append(current_para.strip())
    
    # === ÉTAPE 3: FORMATAGE DES PARAGRAPHES ===
    formatted_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Nettoyer les sauts de ligne simples
        paragraph = paragraph.replace('\n', ' ')
        
        # === FORMATAGE AUTOMATIQUE DÉSACTIVÉ ===
        # (Les classes colorées automatiques sont désactivées pour garder le texte noir)
        
        # === MISE EN PARAGRAPHES ===
        
        # Premier paragraphe = introduction
        if i == 0:
            formatted_paragraphs.append(f'<p class="intro-paragraph">{paragraph}</p>')
        
        # Titres détectés (MAJUSCULES de 8+ caractères)
        elif re.match(r'^[A-ZÀÁÂÄÇÉÈÊËÏÎÔÙÛÜŸÑ\s]{8,}$', paragraph):
            formatted_paragraphs.append(f'<h3 class="section-title">{paragraph.title()}</h3>')
        
        # Citations (commence par guillemets)
        elif paragraph.startswith(('"', '« ', '«', '"')):
            formatted_paragraphs.append(f'<blockquote class="article-quote">{paragraph}</blockquote>')
        
        # Paragraphe normal
        else:
            formatted_paragraphs.append(f'<p>{paragraph}</p>')
    
    # Joindre tous les paragraphes
    result = '\n'.join(formatted_paragraphs)
    
    return mark_safe(result)


@register.filter
def enhanced_linebreaks(content):
    """
    Version améliorée des linebreaks avec première ligne en évidence
    """
    if not content:
        return ""
        
    paragraphs = content.strip().split('\n\n')
    formatted = []
    
    for i, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue
            
        # Premier paragraphe = intro
        if i == 0:
            formatted.append(f'<p class="intro-paragraph">{paragraph.strip()}</p>')
        else:
            formatted.append(f'<p>{paragraph.strip()}</p>')
    
    return mark_safe('\n'.join(formatted))

@register.filter
def markdown_test(content):
    """
    Test simple pour voir si le filtre fonctionne
    """
    if not content:
        return ""
    
    # Test simple : remplacer **texte** par <strong>texte</strong>
    result = content.replace('**', '<strong>').replace('**', '</strong>')
    
    # Si ça contient encore **, on fait différemment
    import re
    result = re.sub(r'\*\*([^*]+)\*\*', r'<strong style="color: #16a34a; font-weight: bold;">\1</strong>', content)
    
    return mark_safe(result)

@register.filter
def test_markdown(content):
    """
    Test simple pour le Markdown
    """
    if not content:
        return ""
    
    # Test simple : **texte** -> <strong>texte</strong>
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong style="color: #16a34a; font-weight: 700;">\1</strong>', content)
    
    # Test : *texte* -> <em>texte</em>
    content = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em style="color: #6b7280; font-style: italic;">\1</em>', content)
    
    # Test : ==texte== -> surlignage
    content = re.sub(r'==([^=]+)==', r'<span style="background: #fbbf24; padding: 2px 4px; border-radius: 3px;">\1</span>', content)
    
    # Test : ++texte++ -> vert
    content = re.sub(r'\+\+([^+]+)\+\+', r'<span style="color: #16a34a; font-weight: 600; background: rgba(145, 205, 140, 0.1); padding: 2px 4px; border-radius: 3px;">\1</span>', content)
    
    # Test : !!texte!! -> rouge
    content = re.sub(r'!!([^!]+)!!', r'<span style="color: #dc2626; font-weight: 600; background: rgba(220, 38, 38, 0.1); padding: 2px 4px; border-radius: 3px;">\1</span>', content)
    
    # Convertir en paragraphes simples
    paragraphs = content.split('\n\n') if '\n\n' in content else [content]
    
    formatted = []
    for i, para in enumerate(paragraphs):
        para = para.strip().replace('\n', ' ')
        if para:
            if i == 0:
                formatted.append(f'<p style="font-size: 1.1em; color: #16a34a; border-left: 4px solid #fbbf24; padding-left: 1rem; background: rgba(251, 191, 36, 0.1); padding: 1rem; border-radius: 0 8px 8px 0;">{para}</p>')
            else:
                formatted.append(f'<p>{para}</p>')
    
    return mark_safe('<br>'.join(formatted))

@register.filter
def simple_format(content):
    """
    Formatage simple et garanti pour test
    """
    if not content:
        return ""
        
    # Diviser le contenu en phrases
    sentences = re.split(r'(?<=\.)\s+', content.strip())
    
    # Grouper en paragraphes
    paragraphs = []
    current_para = []
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        current_para.append(sentence)
        
        # Nouveau paragraphe toutes les 2 phrases
        if len(current_para) >= 2:
            paragraph_text = ' '.join(current_para)
            
            if i == 0:  # Premier paragraphe
                paragraphs.append(f'<p class="intro-paragraph">{paragraph_text}</p>')
            else:
                paragraphs.append(f'<p>{paragraph_text}</p>')
                
            current_para = []
    
    # Ajouter le dernier paragraphe
    if current_para:
        paragraph_text = ' '.join(current_para)
        if not paragraphs:  # Si c'est le seul paragraphe
            paragraphs.append(f'<p class="intro-paragraph">{paragraph_text}</p>')
        else:
            paragraphs.append(f'<p>{paragraph_text}</p>')
    
    return mark_safe('\n'.join(paragraphs))

@register.filter
def ndoti_format(content):
    """
    Test simple pour voir si le filtre fonctionne
    """
    if not content:
        return ""
    
    try:
        # TEST : Ajouter un marqueur visible pour prouver que le filtre fonctionne
        content = "🔥 FILTRE APPLIQUÉ 🔥 " + content
        
        # Gras : **texte** (fonctionne)
        content = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="ndoti-bold">\1</strong>', content)
        
        # Italique : *texte* (fonctionne)
        content = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em class="ndoti-italic">\1</em>', content)
        
        # TEST AVEC SIMPLE REPLACE (pas regex)
        content = content.replace("==", "🟡EGAL🟡")
        content = content.replace("++", "🟢PLUS🟢") 
        content = content.replace("!!", "🔴EXCLA🔴")
        
        # Retourner juste le contenu avec un paragraphe simple
        return mark_safe(f'<p class="intro-paragraph">{content}</p>')
        
    except Exception as e:
        return mark_safe(f'<p>ERREUR: {str(e)}</p><p>{content}</p>')
    
    # === FORMATAGE SIMPLE PARAGRAPHES ===
    # Juste pour garder les paragraphes de base
    
    paragraphs = content.split('\n\n')
    formatted_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        if i == 0:
            formatted_paragraphs.append(f'<p class="intro-paragraph">{paragraph}</p>')
        else:
            formatted_paragraphs.append(f'<p>{paragraph}</p>')
    
    return mark_safe('\n'.join(formatted_paragraphs))

@register.filter
def simple_format(content):
    """
    Filtre simplifié - Ne garde que ce qui fonctionne : gras et italique
    """
    if not content:
        return ""
    
    # Conversion des sauts de ligne en paragraphes HTML
    paragraphs = content.strip().split('\n\n')
    formatted_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue
            
        # Nettoyage du paragraphe
        paragraph = paragraph.strip().replace('\n', ' ')
        
        # === FORMATAGE MARKDOWN SIMPLE ===
        # Gras : **texte**
        paragraph = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="ndoti-bold">\1</strong>', paragraph)
        
        # Italique : *texte*
        paragraph = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em class="ndoti-italic">\1</em>', paragraph)
        
        # === FORMATAGE AUTOMATIQUE ===
        # Mise en évidence du premier paragraphe
        if i == 0:
            paragraph = f'<p class="intro-paragraph">{paragraph}</p>'
        # Titres en majuscules
        elif paragraph.isupper() and len(paragraph) < 100:
            paragraph = f'<h3 class="section-title">{paragraph}</h3>'
        # Citations entre guillemets
        elif paragraph.startswith('"') and paragraph.endswith('"'):
            paragraph = f'<blockquote class="citation">{paragraph}</blockquote>'
        # Paragraphe normal
        else:
            paragraph = f'<p>{paragraph}</p>'
        
        formatted_paragraphs.append(paragraph)
    
    return mark_safe('\n'.join(formatted_paragraphs))