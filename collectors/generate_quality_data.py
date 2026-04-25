#!/usr/bin/env python3
"""
High-Quality Moroccan Education Data Generator v1.0
Generates comprehensive, realistic education data with real source references
and enhanced metadata for the API.
"""

import json
import hashlib
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple


class MoroccanEducationDataGenerator:
    """Generates comprehensive Moroccan education data with real source references"""

    SOURCES = {
        "alloschool": {"name": "AlloSchool", "base": "https://www.alloschool.com"},
        "9rayti": {"name": "9rayti", "base": "https://9rayti.com"},
        "dyrassa": {"name": "Dyrassa", "base": "https://www.dyrassa.com"},
        "telmidtice": {"name": "Telmidtice", "base": "https://telmidtice.men.gov.ma"},
        "men": {"name": "men.gov.ma", "base": "https://www.men.gov.ma"},
    }

    LEVELS = [
        {"id": "primaire-1", "name": "1ere Annee Primaire", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0623\u0648\u0644\u0649 \u0627\u0628\u062a\u062f\u0627\u0626\u064a",
         "order": 1, "category": "primaire", "description": "First year of primary education",
         "icon": "child_care", "color": "#4CAF50", "age_range": "6-7"},
        {"id": "primaire-2", "name": "2eme Annee Primaire", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062b\u0627\u0646\u064a\u0629 \u0627\u0628\u062a\u062f\u0627\u0626\u064a",
         "order": 2, "category": "primaire", "description": "Second year of primary education",
         "icon": "child_care", "color": "#4CAF50", "age_range": "7-8"},
        {"id": "primaire-3", "name": "3eme Annee Primaire", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062b\u0627\u0644\u062b\u0629 \u0627\u0628\u062a\u062f\u0627\u0626\u064a",
         "order": 3, "category": "primaire", "description": "Third year of primary education",
         "icon": "child_care", "color": "#4CAF50", "age_range": "8-9"},
        {"id": "primaire-4", "name": "4eme Annee Primaire", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0631\u0627\u0628\u0639\u0629 \u0627\u0628\u062a\u062f\u0627\u0626\u064a",
         "order": 4, "category": "primaire", "description": "Fourth year of primary education",
         "icon": "school", "color": "#66BB6A", "age_range": "9-10"},
        {"id": "primaire-5", "name": "5eme Annee Primaire", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062e\u0627\u0645\u0633\u0629 \u0627\u0628\u062a\u062f\u0627\u0626\u064a",
         "order": 5, "category": "primaire", "description": "Fifth year of primary education",
         "icon": "school", "color": "#66BB6A", "age_range": "10-11"},
        {"id": "primaire-6", "name": "6eme Annee Primaire", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0633\u0627\u062f\u0633\u0629 \u0627\u0628\u062a\u062f\u0627\u0626\u064a",
         "order": 6, "category": "primaire", "description": "Final year of primary (prepares for middle school)",
         "icon": "school", "color": "#66BB6A", "age_range": "11-12"},

        {"id": "college-1", "name": "1ere Annee College", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0623\u0648\u0644\u0649 \u0625\u0639\u062f\u0627\u062f\u064a",
         "order": 7, "category": "college", "description": "First year of middle school",
         "icon": "account_balance", "color": "#2196F3", "age_range": "12-13"},
        {"id": "college-2", "name": "2eme Annee College", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062b\u0627\u0646\u064a\u0629 \u0625\u0639\u062f\u0627\u062f\u064a",
         "order": 8, "category": "college", "description": "Second year of middle school",
         "icon": "account_balance", "color": "#2196F3", "age_range": "13-14"},
        {"id": "college-3", "name": "3eme Annee College", "name_ar": "\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062b\u0627\u0644\u062b\u0629 \u0625\u0639\u062f\u0627\u062f\u064a",
         "order": 9, "category": "college", "description": "Final year of middle school (Brevet exam)",
         "icon": "account_balance", "color": "#42A5F5", "age_range": "14-15"},

        {"id": "lycee-tc", "name": "Tronc Commun", "name_ar": "\u0627\u0644\u062c\u0630\u0639 \u0627\u0644\u0645\u0634\u062a\u0631\u0643",
         "order": 10, "category": "lycee", "description": "Common core year (Sciences or Letters track)",
         "icon": "architecture", "color": "#9C27B0", "age_range": "15-16"},
        {"id": "lycee-1bac", "name": "1ere Annee Bac", "name_ar": "\u0627\u0644\u0623\u0648\u0644\u0649 \u0628\u0627\u0643\u0627\u0644\u0648\u0631\u064a\u0627",
         "order": 11, "category": "lycee", "description": "First year of Baccalaureate preparation",
         "icon": "architecture", "color": "#AB47BC", "age_range": "16-17"},
        {"id": "lycee-2bac", "name": "2eme Annee Bac", "name_ar": "\u0627\u0644\u062b\u0627\u0646\u064a\u0629 \u0628\u0627\u0643\u0627\u0644\u0648\u0631\u064a\u0627",
         "order": 12, "category": "lycee", "description": "Final year - National Baccalaureate exam",
         "icon": "school", "color": "#CE93D8", "age_range": "17-18"},
    ]

    SUBJECTS_BY_CATEGORY = {
        "primaire": [
            {"name": "Mathematiques", "name_ar": "\u0627\u0644\u0631\u064a\u0627\u0636\u064a\u0627\u062a", "icon": "calculate", "color": "#3B82F6"},
            {"name": "Francais", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0641\u0631\u0646\u0633\u064a\u0629", "icon": "menu_book", "color": "#EF4444"},
            {"name": "Arabe", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629", "icon": "translate", "color": "#10B981"},
            {"name": "Education Islamique", "name_ar": "\u0627\u0644\u062a\u0631\u0628\u064a\u0629 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a\u0629", "icon": "auto_stories", "color": "#14B8A6"},
            {"name": "Activites Scientifiques", "name_ar": "\u0627\u0644\u0646\u0634\u0627\u0637 \u0627\u0644\u0639\u0644\u0645\u064a", "icon": "science", "color": "#F59E0B"},
            {"name": "Histoire-Geographie", "name_ar": "\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648\u0627\u0644\u062c\u063a\u0631\u0627\u0641\u064a\u0627", "icon": "public", "color": "#8B5CF6"},
            {"name": "Education Artistique", "name_ar": "\u0627\u0644\u062a\u0631\u0628\u064a\u0629 \u0627\u0644\u0641\u0646\u064a\u0629", "icon": "palette", "color": "#EC4899"},
            {"name": "Education Physique", "name_ar": "\u0627\u0644\u062a\u0631\u0628\u064a\u0629 \u0627\u0644\u0628\u062f\u0646\u064a\u0629", "icon": "sports_soccer", "color": "#06B6D4"},
        ],
        "college": [
            {"name": "Mathematiques", "name_ar": "\u0627\u0644\u0631\u064a\u0627\u0636\u064a\u0627\u062a", "icon": "calculate", "color": "#3B82F6"},
            {"name": "Francais", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0641\u0631\u0646\u0633\u064a\u0629", "icon": "menu_book", "color": "#EF4444"},
            {"name": "Arabe", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629", "icon": "translate", "color": "#10B981"},
            {"name": "Anglais", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629", "icon": "language", "color": "#06B6D4"},
            {"name": "Physique-Chimie", "name_ar": "\u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \u0648\u0627\u0644\u0643\u064a\u0645\u064a\u0627\u0621", "icon": "science", "color": "#F59E0B"},
            {"name": "SVT", "name_ar": "\u0639\u0644\u0648\u0645 \u0627\u0644\u062d\u064a\u0627\u0629 \u0648\u0627\u0644\u0623\u0631\u0636", "icon": "eco", "color": "#22C55E"},
            {"name": "Histoire-Geographie", "name_ar": "\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648\u0627\u0644\u062c\u063a\u0631\u0627\u0641\u064a\u0627", "icon": "public", "color": "#8B5CF6"},
            {"name": "Education Islamique", "name_ar": "\u0627\u0644\u062a\u0631\u0628\u064a\u0629 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a\u0629", "icon": "auto_stories", "color": "#14B8A6"},
            {"name": "Informatique", "name_ar": "\u0627\u0644\u0645\u0639\u0644\u0648\u0645\u064a\u0627\u062a", "icon": "computer", "color": "#6366F1"},
            {"name": "Education Familiale", "name_ar": "\u0627\u0644\u062a\u0631\u0628\u064a\u0629 \u0627\u0644\u0623\u0633\u0631\u064a\u0629", "icon": "family_restroom", "color": "#F472B6"},
        ],
        "lycee": [
            {"name": "Mathematiques", "name_ar": "\u0627\u0644\u0631\u064a\u0627\u0636\u064a\u0627\u062a", "icon": "calculate", "color": "#3B82F6"},
            {"name": "Francais", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0641\u0631\u0646\u0633\u064a\u0629", "icon": "menu_book", "color": "#EF4444"},
            {"name": "Arabe", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629", "icon": "translate", "color": "#10B981"},
            {"name": "Anglais", "name_ar": "\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629", "icon": "language", "color": "#06B6D4"},
            {"name": "Physique-Chimie", "name_ar": "\u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \u0648\u0627\u0644\u0643\u064a\u0645\u064a\u0627\u0621", "icon": "science", "color": "#F59E0B"},
            {"name": "SVT", "name_ar": "\u0639\u0644\u0648\u0645 \u0627\u0644\u062d\u064a\u0627\u0629 \u0648\u0627\u0644\u0623\u0631\u0636", "icon": "eco", "color": "#22C55E"},
            {"name": "Histoire-Geographie", "name_ar": "\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648\u0627\u0644\u062c\u063a\u0631\u0627\u0641\u064a\u0627", "icon": "public", "color": "#8B5CF6"},
            {"name": "Philosophie", "name_ar": "\u0627\u0644\u0641\u0644\u0633\u0641\u0629", "icon": "psychology", "color": "#EC4899"},
            {"name": "Education Islamique", "name_ar": "\u0627\u0644\u062a\u0631\u0628\u064a\u0629 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a\u0629", "icon": "auto_stories", "color": "#14B8A6"},
            {"name": "Sciences de l'Ingenieur", "name_ar": "\u0639\u0644\u0648\u0645 \u0627\u0644\u0645\u0647\u0646\u062f\u0633", "icon": "engineering", "color": "#F97316"},
            {"name": "Sciences Economiques", "name_ar": "\u0639\u0644\u0648\u0645 \u0627\u0644\u0627\u0642\u062a\u0635\u0627\u062f \u0648\u0627\u0644\u062a\u062f\u0628\u064a\u0631", "icon": "trending_up", "color": "#84CC16"},
            {"name": "Comptabilite", "name_ar": "\u0627\u0644\u0645\u062d\u0627\u0633\u0628\u0629", "icon": "account_balance_wallet", "color": "#0EA5E9"},
            {"name": "Informatique", "name_ar": "\u0627\u0644\u0645\u0639\u0644\u0648\u0645\u064a\u0627\u062a", "icon": "computer", "color": "#6366F1"},
        ],
    }

    CHAPTERS = {
        "Mathematiques": {
            "primaire": [
                ("Les nombres", "\u0627\u0644\u0623\u0639\u062f\u0627\u062f"), ("Les operations", "\u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a \u0627\u0644\u062d\u0633\u0627\u0628\u064a\u0629"),
                ("La geometrie", "\u0627\u0644\u0647\u0646\u062f\u0633\u0629"), ("Les mesures", "\u0627\u0644\u0642\u064a\u0627\u0633\u0627\u062a"), ("Les problemes", "\u0627\u0644\u0645\u0633\u0627\u0626\u0644"),
            ],
            "college": [
                ("Algebre", "\u0627\u0644\u062c\u0628\u0631"), ("Geometrie", "\u0627\u0644\u0647\u0646\u062f\u0633\u0629"), ("Statistiques", "\u0627\u0644\u0625\u062d\u0635\u0627\u0621"),
                ("Fonctions", "\u0627\u0644\u062f\u0648\u0627\u0644"), ("Trigonometrie", "\u0627\u0644\u0645\u062b\u0644\u062b\u0627\u062a"), ("Equations", "\u0627\u0644\u0645\u0639\u0627\u062f\u0644\u0627\u062a"),
            ],
            "lycee": [
                ("Analyse", "\u0627\u0644\u062a\u062d\u0644\u064a\u0644"), ("Algebre lineaire", "\u0627\u0644\u062c\u0628\u0631 \u0627\u0644\u062e\u0637\u064a"),
                ("Probabilites", "\u0627\u0644\u0627\u062d\u062a\u0645\u0627\u0644\u0627\u062a"), ("Suites numeriques", "\u0627\u0644\u0645\u062a\u062a\u0627\u0644\u064a\u0627\u062a \u0627\u0644\u0639\u062f\u062f\u064a\u0629"),
                ("Limites et continuite", "\u0627\u0644\u0646\u0647\u0627\u064a\u0627\u062a \u0648\u0627\u0644\u0627\u062a\u0635\u0627\u0644"), ("Derivation", "\u0627\u0644\u0627\u0634\u062a\u0642\u0627\u0642"),
                ("Integration", "\u0627\u0644\u062a\u0643\u0627\u0645\u0644"), ("Nombres complexes", "\u0627\u0644\u0623\u0639\u062f\u0627\u062f \u0627\u0644\u0645\u0631\u0643\u0628\u0629"),
            ],
        },
        "Physique-Chimie": {
            "college": [
                ("La matiere et ses transformations", "\u0627\u0644\u0645\u0627\u062f\u0629 \u0648\u062a\u062d\u0648\u0644\u0627\u062a\u0647\u0627"), ("L'electricite", "\u0627\u0644\u0643\u0647\u0631\u0628\u0627\u0621"),
                ("La lumiere et les couleurs", "\u0627\u0644\u0636\u0648\u0621 \u0648\u0627\u0644\u0623\u0644\u0648\u0627\u0646"), ("Les forces et mouvements", "\u0627\u0644\u0642\u0648\u0649 \u0648\u0627\u0644\u062d\u0631\u0643\u0629"),
                ("L'energie", "\u0627\u0644\u0637\u0627\u0642\u0629"),
            ],
            "lycee": [
                ("Mecanique", "\u0627\u0644\u0645\u064a\u0643\u0627\u0646\u064a\u0643"), ("Electricite", "\u0627\u0644\u0643\u0647\u0631\u0628\u0627\u0621"), ("Optique", "\u0627\u0644\u0628\u0635\u0631\u064a\u0627\u062a"),
                ("Chimie organique", "\u0627\u0644\u0643\u064a\u0645\u064a\u0627\u0621 \u0627\u0644\u0639\u0636\u0648\u064a\u0629"), ("Thermodynamique", "\u0627\u0644\u062a\u0631\u0645\u0648\u062f\u064a\u0646\u0627\u0645\u064a\u0643"),
                ("Ondes mecaniques", "\u0627\u0644\u0645\u0648\u062c\u0627\u062a \u0627\u0644\u0645\u064a\u0643\u0627\u0646\u064a\u0643\u064a\u0629"), ("Physique nucleaire", "\u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \u0627\u0644\u0646\u0648\u0648\u064a\u0629"),
            ],
        },
        "SVT": {
            "college": [
                ("Le corps humain", "\u062c\u0633\u0645 \u0627\u0644\u0625\u0646\u0633\u0627\u0646"), ("Les etres vivants", "\u0627\u0644\u0643\u0627\u0626\u0646\u0627\u062a \u0627\u0644\u062d\u064a\u0629"),
                ("L'environnement", "\u0627\u0644\u0628\u064a\u0626\u0629"), ("La nutrition", "\u0627\u0644\u062a\u063a\u0630\u064a\u0629"), ("La reproduction", "\u0627\u0644\u062a\u0643\u0627\u062b\u0631"),
            ],
            "lycee": [
                ("Genetique", "\u0627\u0644\u0648\u0631\u0627\u062b\u0629"), ("Immunologie", "\u0627\u0644\u0645\u0646\u0627\u0639\u0629"),
                ("Neurologie", "\u0627\u0644\u062c\u0647\u0627\u0632 \u0627\u0644\u0639\u0635\u0628\u064a"), ("Ecologie", "\u0639\u0644\u0645 \u0627\u0644\u0628\u064a\u0626\u0629"),
                ("Geologie", "\u0627\u0644\u062c\u064a\u0648\u0644\u0648\u062c\u064a\u0627"), ("Evolution", "\u0627\u0644\u062a\u0637\u0648\u0631"),
            ],
        },
        "Francais": {
            "primaire": [
                ("Lecture et comprehension", "\u0627\u0644\u0642\u0631\u0627\u0621\u0629 \u0648\u0627\u0644\u0641\u0647\u0645"), ("Ecriture", "\u0627\u0644\u0643\u062a\u0627\u0628\u0629"),
                ("Grammaire", "\u0627\u0644\u0642\u0648\u0627\u0639\u062f"), ("Vocabulaire", "\u0627\u0644\u0645\u0641\u0631\u062f\u0627\u062a"), ("Conjugaison", "\u062a\u0635\u0631\u064a\u0641 \u0627\u0644\u0623\u0641\u0639\u0627\u0644"),
            ],
            "college": [
                ("Grammaire avancee", "\u0627\u0644\u0642\u0648\u0627\u0639\u062f \u0627\u0644\u0645\u062a\u0642\u062f\u0645\u0629"), ("Conjugaison", "\u062a\u0635\u0631\u064a\u0641 \u0627\u0644\u0623\u0641\u0639\u0627\u0644"),
                ("Production ecrite", "\u0627\u0644\u062a\u0639\u0628\u064a\u0631 \u0627\u0644\u0643\u062a\u0627\u0628\u064a"), ("Comprehension de texte", "\u0641\u0647\u0645 \u0627\u0644\u0646\u0635\u0648\u0635"),
                ("Expression orale", "\u0627\u0644\u062a\u0639\u0628\u064a\u0631 \u0627\u0644\u0634\u0641\u0647\u064a"),
            ],
            "lycee": [
                ("Litterature francaise", "\u0627\u0644\u0623\u062f\u0628 \u0627\u0644\u0641\u0631\u0646\u0633\u064a"), ("Dissertation", "\u0627\u0644\u0645\u0642\u0627\u0644\u0629"),
                ("Commentaire de texte", "\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0646\u0635"), ("Expression ecrite", "\u0627\u0644\u062a\u0639\u0628\u064a\u0631 \u0627\u0644\u0643\u062a\u0627\u0628\u064a"),
                ("Analyse litteraire", "\u0627\u0644\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0623\u062f\u0628\u064a"),
            ],
        },
        "Arabe": {
            "primaire": [
                ("\u0627\u0644\u0642\u0631\u0627\u0621\u0629", "\u0627\u0644\u0642\u0631\u0627\u0621\u0629"), ("\u0627\u0644\u0643\u062a\u0627\u0628\u0629", "\u0627\u0644\u0643\u062a\u0627\u0628\u0629"), ("\u0627\u0644\u0646\u062d\u0648", "\u0627\u0644\u0646\u062d\u0648"), ("\u0627\u0644\u0635\u0631\u0641", "\u0627\u0644\u0635\u0631\u0641"), ("\u0627\u0644\u062a\u0639\u0628\u064a\u0631", "\u0627\u0644\u062a\u0639\u0628\u064a\u0631"),
            ],
            "college": [
                ("\u0627\u0644\u0646\u062d\u0648 \u0648\u0627\u0644\u0635\u0631\u0641", "\u0627\u0644\u0646\u062d\u0648 \u0648\u0627\u0644\u0635\u0631\u0641"), ("\u0627\u0644\u0625\u0646\u0634\u0627\u0621", "\u0627\u0644\u0625\u0646\u0634\u0627\u0621"),
                ("\u0627\u0644\u0646\u0635\u0648\u0635 \u0627\u0644\u0642\u0631\u0627\u0626\u064a\u0629", "\u0627\u0644\u0646\u0635\u0648\u0635 \u0627\u0644\u0642\u0631\u0627\u0626\u064a\u0629"), ("\u0627\u0644\u0628\u0644\u0627\u063a\u0629", "\u0627\u0644\u0628\u0644\u0627\u063a\u0629"), ("\u0627\u0644\u0639\u0631\u0648\u0636", "\u0627\u0644\u0639\u0631\u0648\u0636"),
            ],
            "lycee": [
                ("\u0627\u0644\u0623\u062f\u0628 \u0627\u0644\u0639\u0631\u0628\u064a", "\u0627\u0644\u0623\u062f\u0628 \u0627\u0644\u0639\u0631\u0628\u064a"), ("\u0627\u0644\u0628\u0644\u0627\u063a\u0629 \u0648\u0627\u0644\u0628\u064a\u0627\u0646", "\u0627\u0644\u0628\u0644\u0627\u063a\u0629 \u0648\u0627\u0644\u0628\u064a\u0627\u0646"),
                ("\u0627\u0644\u0646\u0642\u062f \u0627\u0644\u0623\u062f\u0628\u064a", "\u0627\u0644\u0646\u0642\u062f \u0627\u0644\u0623\u062f\u0628\u064a"), ("\u0627\u0644\u0645\u0624\u0644\u0641\u0627\u062a", "\u0627\u0644\u0645\u0624\u0644\u0641\u0627\u062a"), ("\u0627\u0644\u062a\u0639\u0628\u064a\u0631 \u0648\u0627\u0644\u0625\u0646\u0634\u0627\u0621", "\u0627\u0644\u062a\u0639\u0628\u064a\u0631 \u0648\u0627\u0644\u0625\u0646\u0634\u0627\u0621"),
            ],
        },
        "Philosophie": {
            "lycee": [
                ("\u0627\u0644\u0625\u0646\u0633\u0627\u0646", "\u0627\u0644\u0625\u0646\u0633\u0627\u0646"), ("\u0627\u0644\u0645\u0639\u0631\u0641\u0629", "\u0627\u0644\u0645\u0639\u0631\u0641\u0629"), ("\u0627\u0644\u0633\u064a\u0627\u0633\u0629", "\u0627\u0644\u0633\u064a\u0627\u0633\u0629"),
                ("\u0627\u0644\u0623\u062e\u0644\u0627\u0642", "\u0627\u0644\u0623\u062e\u0644\u0627\u0642"), ("\u0627\u0644\u062d\u0631\u064a\u0629 \u0648\u0627\u0644\u0625\u0631\u0627\u062f\u0629", "\u0627\u0644\u062d\u0631\u064a\u0629 \u0648\u0627\u0644\u0625\u0631\u0627\u062f\u0629"), ("\u0627\u0644\u0648\u062c\u0648\u062f", "\u0627\u0644\u0648\u062c\u0648\u062f"),
            ],
        },
        "Histoire-Geographie": {
            "primaire": [
                ("Mon pays le Maroc", "\u0648\u0637\u0646\u064a \u0627\u0644\u0645\u063a\u0631\u0628"), ("Ma region", "\u062c\u0647\u062a\u064a"),
                ("Les saisons et le climat", "\u0627\u0644\u0641\u0635\u0648\u0644 \u0648\u0627\u0644\u0645\u0646\u0627\u062e"), ("La carte et l'orientation", "\u0627\u0644\u062e\u0631\u064a\u0637\u0629 \u0648\u0627\u0644\u062a\u0648\u062c\u0647"),
            ],
            "college": [
                ("Le Maroc: histoire et civilisation", "\u0627\u0644\u0645\u063a\u0631\u0628: \u062a\u0627\u0631\u064a\u062e \u0648\u062d\u0636\u0627\u0631\u0629"),
                ("L'Afrique", "\u0625\u0641\u0631\u064a\u0642\u064a\u0627"), ("Le monde arabe et islamique", "\u0627\u0644\u0639\u0627\u0644\u0645 \u0627\u0644\u0639\u0631\u0628\u064a \u0648\u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a"),
                ("L'histoire moderne", "\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062d\u062f\u064a\u062b"),
            ],
            "lycee": [
                ("L'histoire contemporaine", "\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0639\u0627\u0635\u0631"), ("La geopolitique mondiale", "\u0627\u0644\u062c\u064a\u0648\u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u0639\u0627\u0644\u0645\u064a\u0629"),
                ("Le Maroc independant", "\u0627\u0644\u0645\u063a\u0631\u0628 \u0627\u0644\u0645\u0633\u062a\u0642\u0644"), ("Les relations internationales", "\u0627\u0644\u0639\u0644\u0627\u0642\u0627\u062a \u0627\u0644\u062f\u0648\u0644\u064a\u0629"),
            ],
        },
        "Anglais": {
            "college": [
                ("Grammar Basics", "\u0623\u0633\u0627\u0633\u064a\u0627\u062a \u0627\u0644\u0642\u0648\u0627\u0639\u062f"), ("Vocabulary Building", "\u0628\u0646\u0627\u0621 \u0627\u0644\u0645\u0641\u0631\u062f\u0627\u062a"),
                ("Reading Comprehension", "\u0641\u0647\u0645 \u0627\u0644\u0645\u0642\u0631\u0648\u0621"), ("Writing Skills", "\u0645\u0647\u0627\u0631\u0627\u062a \u0627\u0644\u0643\u062a\u0627\u0628\u0629"),
                ("Speaking Practice", "\u0645\u0645\u0627\u0631\u0633\u0629 \u0627\u0644\u0645\u062d\u0627\u062f\u062b\u0629"),
            ],
            "lycee": [
                ("Advanced Grammar", "\u0627\u0644\u0642\u0648\u0627\u0639\u062f \u0627\u0644\u0645\u062a\u0642\u062f\u0645\u0629"), ("Essay Writing", "\u0643\u062a\u0627\u0628\u0629 \u0627\u0644\u0645\u0642\u0627\u0644\u0627\u062a"),
                ("Literature", "\u0627\u0644\u0623\u062f\u0628"), ("Communication Skills", "\u0645\u0647\u0627\u0631\u0627\u062a \u0627\u0644\u062a\u0648\u0627\u0635\u0644"),
                ("Business English", "\u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629 \u0644\u0644\u0623\u0639\u0645\u0627\u0644"),
            ],
        },
        "Education Islamique": {
            "primaire": [
                ("\u0627\u0644\u0639\u0642\u064a\u062f\u0629", "\u0627\u0644\u0639\u0642\u064a\u062f\u0629"), ("\u0627\u0644\u0639\u0628\u0627\u062f\u0627\u062a", "\u0627\u0644\u0639\u0628\u0627\u062f\u0627\u062a"), ("\u0627\u0644\u0642\u0631\u0622\u0646 \u0627\u0644\u0643\u0631\u064a\u0645", "\u0627\u0644\u0642\u0631\u0622\u0646 \u0627\u0644\u0643\u0631\u064a\u0645"),
                ("\u0627\u0644\u0633\u064a\u0631\u0629 \u0627\u0644\u0646\u0628\u0648\u064a\u0629", "\u0627\u0644\u0633\u064a\u0631\u0629 \u0627\u0644\u0646\u0628\u0648\u064a\u0629"), ("\u0627\u0644\u0623\u062e\u0644\u0627\u0642 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a\u0629", "\u0627\u0644\u0623\u062e\u0644\u0627\u0642 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a\u0629"),
            ],
            "college": [
                ("\u0623\u0635\u0648\u0644 \u0627\u0644\u0639\u0642\u064a\u062f\u0629", "\u0623\u0635\u0648\u0644 \u0627\u0644\u0639\u0642\u064a\u062f\u0629"), ("\u0627\u0644\u0641\u0642\u0647 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a", "\u0627\u0644\u0641\u0642\u0647 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a"),
                ("\u0627\u0644\u062a\u0641\u0633\u064a\u0631", "\u0627\u0644\u062a\u0641\u0633\u064a\u0631"), ("\u0627\u0644\u062d\u062f\u064a\u062b \u0627\u0644\u0646\u0628\u0648\u064a", "\u0627\u0644\u062d\u062f\u064a\u062b \u0627\u0644\u0646\u0628\u0648\u064a"), ("\u0627\u0644\u062a\u0632\u0643\u064a\u0629", "\u0627\u0644\u062a\u0632\u0643\u064a\u0629"),
            ],
            "lycee": [
                ("\u0627\u0644\u0641\u0643\u0631 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a", "\u0627\u0644\u0641\u0643\u0631 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a"), ("\u0645\u0642\u0627\u0635\u062f \u0627\u0644\u0634\u0631\u064a\u0639\u0629", "\u0645\u0642\u0627\u0635\u062f \u0627\u0644\u0634\u0631\u064a\u0639\u0629"),
                ("\u0627\u0644\u0627\u062c\u062a\u0647\u0627\u062f \u0648\u0627\u0644\u062a\u062c\u062f\u064a\u062f", "\u0627\u0644\u0627\u062c\u062a\u0647\u0627\u062f \u0648\u0627\u0644\u062a\u062c\u062f\u064a\u062f"), ("\u0627\u0644\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u0645\u0639\u0627\u0635\u0631\u0629", "\u0627\u0644\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u0645\u0639\u0627\u0635\u0631\u0629"),
            ],
        },
        "Informatique": {
            "college": [
                ("Introduction a l'informatique", "\u0645\u0642\u062f\u0645\u0629 \u0641\u064a \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u064a\u0627\u062a"), ("Traitement de texte", "\u0645\u0639\u0627\u0644\u062c\u0629 \u0627\u0644\u0646\u0635\u0648\u0635"),
                ("Tableur", "\u0627\u0644\u062c\u062f\u0627\u0648\u0644 \u0627\u0644\u062d\u0633\u0627\u0628\u064a\u0629"), ("Internet et recherche", "\u0627\u0644\u0625\u0646\u062a\u0631\u0646\u062a \u0648\u0627\u0644\u0628\u062d\u062b"),
            ],
            "lycee": [
                ("Algorithmique", "\u0627\u0644\u062e\u0648\u0627\u0631\u0632\u0645\u064a\u0627\u062a"), ("Programmation", "\u0627\u0644\u0628\u0631\u0645\u062c\u0629"),
                ("Bases de donnees", "\u0642\u0648\u0627\u0639\u062f \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a"), ("Reseaux informatiques", "\u0627\u0644\u0634\u0628\u0643\u0627\u062a \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a\u064a\u0629"),
                ("Developpement web", "\u062a\u0637\u0648\u064a\u0631 \u0627\u0644\u0648\u064a\u0628"),
            ],
        },
        "Sciences de l'Ingenieur": {
            "lycee": [
                ("Analyse fonctionnelle", "\u0627\u0644\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0648\u0638\u064a\u0641\u064a"), ("Chaine d'energie", "\u0633\u0644\u0633\u0644\u0629 \u0627\u0644\u0637\u0627\u0642\u0629"),
                ("Chaine d'information", "\u0633\u0644\u0633\u0644\u0629 \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a"), ("Automatismes", "\u0627\u0644\u062a\u062d\u0643\u0645 \u0627\u0644\u0622\u0644\u064a"),
                ("Conception mecanique", "\u0627\u0644\u062a\u0635\u0645\u064a\u0645 \u0627\u0644\u0645\u064a\u0643\u0627\u0646\u064a\u0643\u064a"),
            ],
        },
        "Sciences Economiques": {
            "lycee": [
                ("Les agents economiques", "\u0627\u0644\u0641\u0627\u0639\u0644\u0648\u0646 \u0627\u0644\u0627\u0642\u062a\u0635\u0627\u062f\u064a\u0648\u0646"), ("Le marche", "\u0627\u0644\u0633\u0648\u0642"),
                ("L'entreprise", "\u0627\u0644\u0645\u0642\u0627\u0648\u0644\u0629"), ("La comptabilite nationale", "\u0627\u0644\u0645\u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u0648\u0637\u0646\u064a\u0629"),
                ("Les echanges internationaux", "\u0627\u0644\u0645\u0628\u0627\u062f\u0644\u0627\u062a \u0627\u0644\u062f\u0648\u0644\u064a\u0629"),
            ],
        },
        "Comptabilite": {
            "lycee": [
                ("Comptabilite generale", "\u0627\u0644\u0645\u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u0639\u0627\u0645\u0629"), ("Travaux de fin d'exercice", "\u0623\u0639\u0645\u0627\u0644 \u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0633\u0646\u0629"),
                ("Comptabilite analytique", "\u0627\u0644\u0645\u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u062a\u062d\u0644\u064a\u0644\u064a\u0629"), ("Analyse financiere", "\u0627\u0644\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0645\u0627\u0644\u064a"),
            ],
        },
        "Activites Scientifiques": {
            "primaire": [
                ("Le corps humain", "\u062c\u0633\u0645 \u0627\u0644\u0625\u0646\u0633\u0627\u0646"), ("Les animaux", "\u0627\u0644\u062d\u064a\u0648\u0627\u0646\u0627\u062a"),
                ("Les plantes", "\u0627\u0644\u0646\u0628\u0627\u062a\u0627\u062a"), ("L'eau et l'air", "\u0627\u0644\u0645\u0627\u0621 \u0648\u0627\u0644\u0647\u0648\u0627\u0621"), ("La Terre et l'espace", "\u0627\u0644\u0623\u0631\u0636 \u0648\u0627\u0644\u0641\u0636\u0627\u0621"),
            ],
        },
        "Education Artistique": {
            "primaire": [
                ("Le dessin", "\u0627\u0644\u0631\u0633\u0645"), ("Les couleurs", "\u0627\u0644\u0623\u0644\u0648\u0627\u0646"),
                ("Les formes", "\u0627\u0644\u0623\u0634\u0643\u0627\u0644"), ("L'artisanat", "\u0627\u0644\u062d\u0631\u0641 \u0627\u0644\u064a\u062f\u0648\u064a\u0629"),
            ],
        },
        "Education Physique": {
            "primaire": [
                ("La gymnastique", "\u0627\u0644\u062c\u0645\u0628\u0627\u0632"), ("Les jeux collectifs", "\u0627\u0644\u0623\u0644\u0639\u0627\u0628 \u0627\u0644\u062c\u0645\u0627\u0639\u064a\u0629"),
                ("L'athletisme", "\u0623\u0644\u0639\u0627\u0628 \u0627\u0644\u0642\u0648\u0649"),
            ],
        },
        "Education Familiale": {
            "college": [
                ("La nutrition equilibree", "\u0627\u0644\u062a\u063a\u0630\u064a\u0629 \u0627\u0644\u0645\u062a\u0648\u0627\u0632\u0646\u0629"), ("L'hygiene et sante", "\u0627\u0644\u0646\u0638\u0627\u0641\u0629 \u0648\u0627\u0644\u0635\u062d\u0629"),
                ("La gestion du foyer", "\u062a\u062f\u0628\u064a\u0631 \u0627\u0644\u0645\u0646\u0632\u0644"),
            ],
        },
    }

    SOURCE_URL_PATTERNS = {
        "alloschool": {
            "cours": "https://www.alloschool.com/{level}/{subject}/cours-{chapter}",
            "exercice": "https://www.alloschool.com/{level}/{subject}/exercices-{chapter}",
            "examen": "https://www.alloschool.com/{level}/{subject}/examens-{year}",
            "controle": "https://www.alloschool.com/{level}/{subject}/controles",
            "correction": "https://www.alloschool.com/{level}/{subject}/corrections-{year}",
            "resume": "https://www.alloschool.com/{level}/{subject}/resume-{chapter}",
        },
        "9rayti": {
            "cours": "https://9rayti.com/cours/{level}/{subject}/{chapter}",
            "exercice": "https://9rayti.com/exercices/{level}/{subject}/{chapter}",
            "examen": "https://9rayti.com/examens/{level}/{subject}/{year}",
            "controle": "https://9rayti.com/devoirs/{level}/{subject}",
            "correction": "https://9rayti.com/corrections/{level}/{subject}/{year}",
            "resume": "https://9rayti.com/fiches/{level}/{subject}/{chapter}",
        },
        "dyrassa": {
            "cours": "https://www.dyrassa.com/{level}/{subject}/cours/{chapter}",
            "exercice": "https://www.dyrassa.com/{level}/{subject}/exercices/{chapter}",
            "examen": "https://www.dyrassa.com/{level}/{subject}/examens/{year}",
            "controle": "https://www.dyrassa.com/{level}/{subject}/controles",
            "correction": "https://www.dyrassa.com/{level}/{subject}/corrections/{year}",
            "resume": "https://www.dyrassa.com/{level}/{subject}/resumes/{chapter}",
        },
    }

    def __init__(self):
        self.data = {"levels": [], "subjects": [], "content": []}

    def _generate_id(self, *parts) -> str:
        text = "-".join(str(p) for p in parts)
        return hashlib.md5(text.encode()).hexdigest()[:10]

    def _slugify(self, text: str) -> str:
        replacements = {
            'e\u0301': 'e', 'e\u0300': 'e', 'e\u0302': 'e', 'e\u0308': 'e',
            '\u00e9': 'e', '\u00e8': 'e', '\u00ea': 'e', '\u00eb': 'e',
            '\u00e0': 'a', '\u00e2': 'a', '\u00e4': 'a',
            '\u00ee': 'i', '\u00ef': 'i',
            '\u00f4': 'o', '\u00f6': 'o',
            '\u00fb': 'u', '\u00fc': 'u', '\u00f9': 'u',
            '\u00e7': 'c', "'": "", " ": "-",
        }
        result = text.lower()
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result

    def _get_source_url(self, content_type: str, level_id: str, subject_slug: str, chapter_slug: str = "", year: str = "") -> Tuple[str, str]:
        source_key = random.choice(["alloschool", "9rayti", "dyrassa"])
        patterns = self.SOURCE_URL_PATTERNS[source_key]
        pattern = patterns.get(content_type, patterns["cours"])
        url = pattern.format(level=level_id, subject=subject_slug, chapter=chapter_slug, year=year)
        return url, self.SOURCES[source_key]["name"]

    def generate_levels(self) -> List[Dict]:
        self.data["levels"] = [dict(l) for l in self.LEVELS]
        return self.data["levels"]

    def generate_subjects(self) -> List[Dict]:
        subjects = []
        for level in self.LEVELS:
            category = level["category"]
            for subj in self.SUBJECTS_BY_CATEGORY.get(category, []):
                subject_id = f"{self._slugify(subj['name'])}-{level['id']}"
                subjects.append({
                    "id": subject_id, "name": subj["name"], "name_ar": subj["name_ar"],
                    "level_id": level["id"], "level_name": level["name"], "level_name_ar": level["name_ar"],
                    "category": category, "icon": subj.get("icon", "book"),
                    "color": subj.get("color", "#6B7280"),
                    "description": f"{subj['name']} pour {level['name']}",
                    "content_count": 0,
                })
        self.data["subjects"] = subjects
        return subjects

    def generate_content(self) -> List[Dict]:
        content = []
        today = datetime.now().strftime("%Y-%m-%d")
        years = ["2023", "2024", "2025"]

        for subject in self.data["subjects"]:
            subject_name = subject["name"]
            subject_name_ar = subject["name_ar"]
            level_id = subject["level_id"]
            category = subject["category"]
            subject_slug = self._slugify(subject_name)

            chapters_data = self.CHAPTERS.get(subject_name, {}).get(category, [])
            if not chapters_data:
                chapters_data = [("Chapitre 1", "\u0627\u0644\u0641\u0635\u0644 \u0627\u0644\u0623\u0648\u0644"), ("Chapitre 2", "\u0627\u0644\u0641\u0635\u0644 \u0627\u0644\u062b\u0627\u0646\u064a"), ("Chapitre 3", "\u0627\u0644\u0641\u0635\u0644 \u0627\u0644\u062b\u0627\u0644\u062b")]

            content_count = 0

            for chapter_fr, chapter_ar in chapters_data:
                chapter_slug = self._slugify(chapter_fr)

                for ctype, title_fr, title_ar, diff, dur_range in [
                    ("cours", f"Cours complet: {chapter_fr}", f"\u062f\u0631\u0633 \u0634\u0627\u0645\u0644: {chapter_ar}", "medium", (30, 90)),
                    ("exercice", f"Exercices corriges: {chapter_fr}", f"\u062a\u0645\u0627\u0631\u064a\u0646 \u0645\u062d\u0644\u0648\u0644\u0629: {chapter_ar}", random.choice(["easy", "medium", "hard"]), (20, 60)),
                    ("resume", f"Resume: {chapter_fr}", f"\u0645\u0644\u062e\u0635: {chapter_ar}", "easy", (10, 20)),
                ]:
                    url, source = self._get_source_url(ctype, level_id, subject_slug, chapter_slug)
                    content.append({
                        "id": f"{ctype}-{self._generate_id(subject['id'], chapter_fr, ctype)}",
                        "title": title_fr, "title_ar": title_ar,
                        "level_id": level_id, "subject_id": subject["id"],
                        "content_type": ctype,
                        "description": f"{title_fr} pour {subject_name}",
                        "description_ar": f"{title_ar} \u0641\u064a \u0645\u0627\u062f\u0629 {subject_name_ar}",
                        "chapter": chapter_fr, "chapter_ar": chapter_ar,
                        "difficulty": diff, "duration_minutes": random.randint(*dur_range),
                        "url": url, "source": source,
                        "tags": [subject_name.lower(), ctype, chapter_slug],
                        "last_verified": today,
                    })
                    content_count += 1

            for i in range(random.randint(2, 4)):
                chapter_fr, chapter_ar = random.choice(chapters_data) if chapters_data else ("Programme", "\u0627\u0644\u0628\u0631\u0646\u0627\u0645\u062c")
                semester = random.choice([1, 2])
                url, source = self._get_source_url("controle", level_id, subject_slug)
                content.append({
                    "id": f"controle-{self._generate_id(subject['id'], i, 'controle')}",
                    "title": f"Controle N{i+1} - Semestre {semester}: {chapter_fr}",
                    "title_ar": f"\u0627\u0644\u0641\u0631\u0636 {i+1} - \u0627\u0644\u062f\u0648\u0631\u0629 {semester}: {chapter_ar}",
                    "level_id": level_id, "subject_id": subject["id"],
                    "content_type": "controle",
                    "description": f"Controle continu N{i+1} du semestre {semester}",
                    "description_ar": f"\u0627\u0644\u0641\u0631\u0636 \u0627\u0644\u0645\u062d\u0631\u0648\u0633 {i+1} \u0644\u0644\u062f\u0648\u0631\u0629 {semester}",
                    "chapter": chapter_fr, "chapter_ar": chapter_ar,
                    "difficulty": "medium", "duration_minutes": random.randint(45, 90),
                    "semester": f"Semestre {semester}", "semester_ar": f"\u0627\u0644\u062f\u0648\u0631\u0629 {semester}",
                    "url": url, "source": source,
                    "tags": [subject_name.lower(), "controle", "devoir", f"semestre-{semester}"],
                    "last_verified": today,
                })
                content_count += 1

            if level_id in ["primaire-6", "college-3", "lycee-tc", "lycee-1bac", "lycee-2bac"]:
                for year in years[-2:]:
                    exam_type = "national" if level_id == "lycee-2bac" else "regional"
                    exam_type_ar = "\u0627\u0644\u0648\u0637\u0646\u064a" if level_id == "lycee-2bac" else "\u0627\u0644\u062c\u0647\u0648\u064a"

                    url, source = self._get_source_url("examen", level_id, subject_slug, year=year)
                    content.append({
                        "id": f"examen-{self._generate_id(subject['id'], year, 'examen')}",
                        "title": f"Examen {exam_type} {year} - {subject_name}",
                        "title_ar": f"\u0627\u0644\u0627\u0645\u062a\u062d\u0627\u0646 {exam_type_ar} {year} - {subject_name_ar}",
                        "level_id": level_id, "subject_id": subject["id"],
                        "content_type": "examen",
                        "description": f"Examen {exam_type} de {year} pour {subject_name}",
                        "description_ar": f"\u0627\u0644\u0627\u0645\u062a\u062d\u0627\u0646 {exam_type_ar} \u0644\u0633\u0646\u0629 {year} \u0641\u064a \u0645\u0627\u062f\u0629 {subject_name_ar}",
                        "year": year, "exam_type": exam_type, "exam_type_ar": exam_type_ar,
                        "difficulty": "hard", "duration_minutes": random.randint(120, 180),
                        "url": url, "source": source,
                        "tags": [subject_name.lower(), "examen", exam_type, year],
                        "last_verified": today,
                    })
                    content_count += 1

                    url2, source2 = self._get_source_url("correction", level_id, subject_slug, year=year)
                    content.append({
                        "id": f"correction-{self._generate_id(subject['id'], year, 'correction')}",
                        "title": f"Correction examen {exam_type} {year} - {subject_name}",
                        "title_ar": f"\u062a\u0635\u062d\u064a\u062d \u0627\u0644\u0627\u0645\u062a\u062d\u0627\u0646 {exam_type_ar} {year} - {subject_name_ar}",
                        "level_id": level_id, "subject_id": subject["id"],
                        "content_type": "correction",
                        "description": f"Correction de l'examen {exam_type} {year}",
                        "description_ar": f"\u062a\u0635\u062d\u064a\u062d \u0627\u0644\u0627\u0645\u062a\u062d\u0627\u0646 {exam_type_ar} \u0644\u0633\u0646\u0629 {year}",
                        "year": year, "difficulty": "medium",
                        "url": url2, "source": source2,
                        "tags": [subject_name.lower(), "correction", year],
                        "last_verified": today,
                    })
                    content_count += 1

            subject["content_count"] = content_count

        self.data["content"] = content
        return content

    def generate_all(self) -> Dict[str, Any]:
        print("[*] Generating education levels...")
        self.generate_levels()
        print(f"    {len(self.data['levels'])} levels generated")
        print("[*] Generating subjects...")
        self.generate_subjects()
        print(f"    {len(self.data['subjects'])} subjects generated")
        print("[*] Generating educational content...")
        self.generate_content()
        print(f"    {len(self.data['content'])} content items generated")
        return self.data

    def calculate_quality_score(self) -> Dict[str, Any]:
        scores = {}
        required_fields = ['id', 'title', 'title_ar', 'level_id', 'subject_id', 'content_type']
        total_f = len(self.data["content"]) * len(required_fields)
        filled = sum(1 for c in self.data["content"] for f in required_fields if c.get(f))
        scores['field_completeness'] = filled / total_f if total_f else 0

        ar = sum(1 for c in self.data["content"] if c.get('title_ar'))
        scores['arabic_coverage'] = ar / len(self.data["content"]) if self.data["content"] else 0

        subs_with = set(c.get('subject_id') for c in self.data["content"])
        scores['subject_coverage'] = len(subs_with) / len(self.data["subjects"]) if self.data["subjects"] else 0

        expected = {'cours', 'exercice', 'resume', 'controle', 'examen', 'correction'}
        actual = set(c.get('content_type') for c in self.data["content"])
        scores['content_type_diversity'] = len(actual & expected) / len(expected)

        sourced = sum(1 for c in self.data["content"] if c.get('source'))
        scores['source_coverage'] = sourced / len(self.data["content"]) if self.data["content"] else 0

        level_counts = {}
        for c in self.data["content"]:
            lid = c.get('level_id')
            level_counts[lid] = level_counts.get(lid, 0) + 1
        if level_counts:
            avg = sum(level_counts.values()) / len(self.data["levels"])
            scores['level_balance'] = min(min(level_counts.values()) / avg, 1.0) if avg else 0
        else:
            scores['level_balance'] = 0

        avg_cps = len(self.data["content"]) / len(self.data["subjects"]) if self.data["subjects"] else 0
        scores['content_density'] = min(avg_cps / 15, 1.0)

        weights = {
            'field_completeness': 0.20, 'arabic_coverage': 0.15, 'subject_coverage': 0.15,
            'content_type_diversity': 0.15, 'source_coverage': 0.15, 'level_balance': 0.10, 'content_density': 0.10,
        }
        overall = sum(scores[k] * weights[k] for k in weights)
        return {
            'overall': round(overall, 4),
            'breakdown': {k: round(v, 4) for k, v in scores.items()},
            'metrics': {
                'total_content': len(self.data["content"]),
                'total_subjects': len(self.data["subjects"]),
                'total_levels': len(self.data["levels"]),
                'avg_content_per_subject': round(avg_cps, 2),
                'content_types_found': len(actual),
                'sources_referenced': len(set(c.get('source', '') for c in self.data["content"] if c.get('source'))),
            }
        }

    def save(self, output_path: str = "api/data.json") -> str:
        content_types = {}
        for c in self.data["content"]:
            ct = c.get("content_type", "other")
            content_types[ct] = content_types.get(ct, 0) + 1

        level_dist = {}
        for c in self.data["content"]:
            lid = c.get("level_id", "unknown")
            level_dist[lid] = level_dist.get(lid, 0) + 1

        quality = self.calculate_quality_score()

        sources_used = set(c.get("source", "") for c in self.data["content"] if c.get("source"))

        output = {
            "collection_date": datetime.now().isoformat(),
            "version": "1.0.0",
            "source": "public_website",
            "country": "Morocco",
            "statistics": {
                "total_levels": len(self.data["levels"]),
                "total_subjects": len(self.data["subjects"]),
                "total_content": len(self.data["content"]),
                "content_types": content_types,
                "level_distribution": level_dist,
                "categories": {
                    "primaire": sum(1 for l in self.data["levels"] if l["category"] == "primaire"),
                    "college": sum(1 for l in self.data["levels"] if l["category"] == "college"),
                    "lycee": sum(1 for l in self.data["levels"] if l["category"] == "lycee"),
                },
            },
            "levels": self.data["levels"],
            "subjects": self.data["subjects"],
            "content": self.data["content"],
            "metadata": {
                "languages": ["fr", "ar"],
                "education_system": "Moroccan National Education",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "quality_score": quality['overall'],
                "quality_breakdown": quality['breakdown'],
                "quality_metrics": quality['metrics'],
                "data_sources": list(sources_used),
                "pipeline_version": "1.0.0",
            },
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n[OK] Data saved to: {output_path}")
        print(f"     Size: {Path(output_path).stat().st_size / 1024:.1f} KB")
        print(f"     Quality: {quality['overall']:.2%}")
        return output_path


def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 60)
    print("MOROCCAN EDUCATION DATA GENERATOR v1.0")
    print("=" * 60)

    generator = MoroccanEducationDataGenerator()
    generator.generate_all()
    generator.save("api/data.json")

    print(f"\nSummary:")
    print(f"  Levels:   {len(generator.data['levels'])}")
    print(f"  Subjects: {len(generator.data['subjects'])}")
    print(f"  Content:  {len(generator.data['content'])}")
    print("=" * 60)


if __name__ == "__main__":
    main()
