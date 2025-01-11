# Traduction

## Méthodologie d'évaluation des traductions Wolof-Français

Ce document décrit la méthodologie utilisée pour évaluer la qualité des traductions automatiques du Wolof vers le Français dans notre système.

### Vue d'ensemble

Notre système utilise une approche multi-métrique qui combine plusieurs aspects de la traduction pour fournir une évaluation complète et nuancée. Cette approche a été spécialement conçue pour tenir compte des particularités de la traduction entre le Wolof et le Français.

### Métriques d'évaluation

#### 1. Similarité Sémantique (70% du score final)
- Évalue à quel point le sens de la phrase originale est préservé dans la traduction
- Utilise une comparaison mot à mot intelligente qui :
  - Ignore les mots non significatifs (stop words)
  - Prend en compte les variations lexicales
  - Calcule la similarité entre les mots à l'aide de l'algorithme SequenceMatcher
- Formule : moyenne des meilleures correspondances pour chaque mot significatif

#### 2. Ratio de Longueur (20% du score final)
- Évalue l'équilibre structurel entre la traduction et la référence
- Compare le nombre de mots significatifs entre les deux phrases
- Formule : min(len(traduction) / len(référence), len(référence) / len(traduction))
- Pénalise les traductions trop courtes ou trop longues

#### 3. Correspondance Exacte (10% du score final)
- Bonus accordé aux traductions exactement identiques à la référence
- Score binaire : 1.0 pour une correspondance parfaite, 0.0 sinon
- Encourage la précision tout en restant flexible

### Prétraitement des textes

Avant l'évaluation, les textes subissent plusieurs étapes de normalisation :
1. Conversion en minuscules
2. Suppression de la ponctuation
3. Suppression des espaces superflus
4. Filtrage des mots vides (stop words)

### Stop Words

Le système utilise une liste personnalisée de mots vides français incluant :
- Articles : le, la, les, un, une, des
- Prépositions : de, du, en, dans, par, pour, sur
- Pronoms : je, tu, il, elle, nous, vous, ils, elles
- Autres mots fonctionnels : ce, ça, et, ou, à, au, aux

### Équivalences Sémantiques

Le système intègre des équivalences spécifiques au Wolof-Français pour améliorer l'évaluation :
```python
semantic_equivalences = {
    'mangui gui fi': ['je suis là', 'je vais bien'],
    'kay gnou': ['allons', 'viens on'],
    'na nga def': ['comment vas-tu', 'comment allez-vous']
}
```

### Interprétation des Scores

Le score final est calculé sur une échelle de 0 à 1, où :
- 0.8 - 1.0 : Excellente traduction
- 0.6 - 0.8 : Bonne traduction
- 0.4 - 0.6 : Traduction acceptable
- < 0.4 : Traduction à améliorer

### Format de Sortie

Les résultats de l'évaluation sont enregistrés dans un fichier CSV contenant :
- No : Identifiant de la phrase
- Wolof : Phrase originale en Wolof
- Français : Traduction de référence
- Traduction : Traduction générée
- Score_Final : Score global de la traduction
- Similarite_Semantique : Score de similarité sémantique
- Ratio_Longueur : Score du ratio de longueur
- Correspondance_Exacte : Score de correspondance exacte

### Exemple d'évaluation

```
Phrase Wolof : "Na nga def ?"
Référence    : "Comment vas tu ?"
Traduction   : "Comment vas-tu ?"
Scores :
- Score final            : 0.825
- Similarité sémantique  : 0.875
- Ratio de longueur      : 1.000
- Correspondance exacte  : 0.000
```

### Limitations actuelles

1. Le système ne prend pas en compte :
   - L'ordre des mots spécifique au Wolof
   - Les expressions idiomatiques complexes
   - Les variations dialectales

2. Les équivalences sémantiques doivent être enrichies manuellement

### Perspectives d'amélioration

1. Enrichissement des équivalences sémantiques
2. Ajout de règles spécifiques pour les expressions idiomatiques
3. Prise en compte de la structure grammaticale du Wolof
4. Intégration de variations dialectales
5. Ajout de métriques supplémentaires pour des aspects spécifiques de la traduction

### Utilisation du code

Pour utiliser le système d'évaluation :

```python
# Initialisation de l'évaluateur
evaluator = SimpleMetricEvaluator()

# Évaluation d'une traduction
scores = evaluator.evaluate(reference, traduction)

# Accès aux scores
score_final = scores['score_final']
similarite = scores['similarite_semantique']
ratio = scores['ratio_longueur']
exacte = scores['correspondance_exacte']
```