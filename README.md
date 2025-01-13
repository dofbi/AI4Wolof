# AI4Wolof

Evaluating the performance of Large Language Models (LLM) in Wolof language

## Introduction

### 1. Objectifs du Document

L'objectif de ce projet est d'évaluer les performances des modèles de grande envergure (LLM) en langue Wolof. Cette évaluation comprendra la traduction, la génération de texte, la compréhension de texte et l'analyse grammaticale. Les résultats de cette évaluation seront publiés sur un site web dédié, afin de promouvoir l'utilisation des LLM dans le traitement de la langue Wolof et d'encourager les développements futurs.

### 2. Contexte et Importance de la Langue Wolof

Le Wolof est l'une des langues les plus parlées au Sénégal et dans certaines régions de la Gambie et de la Mauritanie. Malgré sa prévalence, il y a un manque significatif de ressources numériques et d'outils de traitement automatique pour cette langue. À une époque où les technologies de traitement de la langue naturelle (NLP) jouent un rôle crucial dans l'amélioration de la communication et de l'accessibilité de l'information, il est essentiel de développer et d'évaluer des modèles capables de comprendre et de générer du texte en Wolof.

Les technologies NLP peuvent grandement contribuer à la préservation et à la promotion des langues africaines comme le Wolof, en facilitant leur intégration dans les services numériques modernes et en améliorant l'accès à l'information pour les locuteurs natifs. Ce projet vise à combler une partie de ce fossé en fournissant une évaluation systématique et détaillée des capacités des LLM en Wolof.

---

## 2. Tâches

### 1. [Traduction](evaluation/traduction.md)

| N° | Models  | Wolof Scores (0-1)  |
|---|---|---|
| 1 | [gemini-2.0-flash-exp](data/output/traduction/gemini-2.0-flash-exp.csv)  | 0.685  |
| 2 | [anthropic:claude-3-5-sonnet-latest](data/output/traduction/anthropic-claude-3-5-sonnet-latest.csv)  | 0.663  |
| 3 | [openai/chatgpt-4o-latest](data/output/traduction/openai-chatgpt-4o-latest.csv)  | 0.658  |
| 4 | [openai/gpt-4o-mini](data/output/traduction/openai-gpt-4o-mini.csv)  | 0.532  |
| 5 | [anthropic:claude-3-5-haiku-latest](data/output/traduction/anthropic-claude-3-5-haiku-latest.csv)  | 0.505  |
| 6 | [mistralai/mistral-large-2411](data/output/traduction/mistralai-mistral-large-2411.csv)  | 0.454  |
| 7 | [deepseek/deepseek-chat](data/output/traduction/deepseek-deepseek-chat.csv)  | 0.444  |
| 8 | [groq:llama-3.3-70b-versatile](data/output/traduction/groq-llama-3.3-70b-versatile.csv)  | 0.416  |
| 9 | [eva-unit-01/eva-qwen-2.5-72b](data/output/traduction/eva-unit-01-eva-qwen-2.5-72b.csv)  | 0.414  |
| 10 | [gemini-1.5-flash](data/output/traduction/gemini-1.5-flash.csv)  | 0.412  |
| 11 | [meta-llama/llama-3.3-70b-instruct](data/output/traduction/meta-llama-llama-3.3-70b-instruct.csv)  | 0.409  |

### 2. Génération d'Histoires
### 3. Compréhension de Texte
### 4. Analyse Grammaticale


---

Très bien, passons à la rédaction de la partie 2 sur le corpus :

---

## 3. Corpus

### 1. Sélection et Préparation des Données

Pour évaluer les performances des LLM en langue Wolof, il est crucial de disposer d'un corpus diversifié et représentatif. Ce corpus comprendra des textes couvrant divers domaines tels que les conversations quotidiennes, les articles de presse, les œuvres littéraires, et les documents techniques. Les sources des données incluront :
- **Conversations courantes** : Textes issus de dialogues informels pour évaluer la compréhension du langage usuel.
- **Articles de presse** : Extraits de journaux pour tester la capacité à traiter l'information structurée.
- **Œuvres littéraires** : Passages de livres pour analyser la compréhension de la prose complexe.
- **Documents techniques** : Textes spécialisés pour évaluer la gestion du vocabulaire technique.

### 2. Diversité et Complexité des Textes

Le corpus sera composé de textes variés en termes de style, de registre et de complexité grammaticale. Cela permettra d'évaluer la performance du modèle sur :
- **Des phrases simples** : Pour tester la précision de base.
- **Des phrases complexes** : Incluant des idiomes et des structures grammaticales variées.
- **Vocabulaire spécialisé** : Pour examiner la gestion des termes techniques ou moins courants.

Ces textes seront soigneusement sélectionnés pour couvrir un large éventail de contextes et de niveaux de difficulté, garantissant ainsi une évaluation complète et équilibrée du modèle.

### 3. Sources

- [Waxtane](https://github.com/MedouneSGB/Waxtane)

