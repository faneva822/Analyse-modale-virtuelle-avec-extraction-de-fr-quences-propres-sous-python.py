 Analyse Module d'une Poutre

Description

Ce programme réalise une **analyse modale par éléments finis** d'une poutre soumise à différentes conditions d'appui. Il calcule les fréquences propres, les modes de vibration et génère une Fonction de Réponse en Fréquence (FRF).

 Fonctionnalités

- **Saisie interactive** des paramètres physiques et géométriques
- **8 types de profilés** disponibles
- **Conditions d'appui** personnalisables
- **Calculs** des fréquences propres et déformées modales
- **Visualisations** complètes des résultats

Prérequis

```bash
pip install numpy matplotlib scipy

Exemple de session
=== ANALYSE MODALE POUTRE ===
Longueur (m) : 5
Module de Young (Pa) : 2.1e11
Masse volumique (kg/m3) : 7850
Nombre de noeuds (ex: 40) : 50

=== PROFIL ===
1 Rectangle | 2 Carré | 3 Cercle
4 Tube circulaire | 5 IPE | 6 UPN | 7 Cornière | 8 Tube rect
Choix : 5

1 - IPE 100 (h=0.1, b=0.055)
2 - IPE 200 (h=0.2, b=0.1)
3 - IPE 300 (h=0.3, b=0.15)
Choix : 2

1 Encastre | 2 Deux appuis
Choix : 2
Appui 1 (m): 0
Appui 2 (m): 5
[Visualisation du profil]
[Schéma des appuis]
[Calcul des fréquences]
[Affichage FRF et mode propre]
--- FRÉQUENCES PROPRES CALCULÉES ---
Fréquence propre fondamentale f1 = 12.34 Hz
Fréquence propre 2 = 49.38 Hz
Fréquence propre 3 = 111.11 Hz
Surface = 0.00384 m²
Inertie = 1.94e-06 m⁴

VISUALISATION DES RÉSULTATS
Deux graphiques s'affichent simultanément :
Graphique 1 : FRF (Fonction de Réponse en Fréquence)
•	Courbe noire : réponse fréquentielle
•	Points rouges : pics identifiés automatiquement
•	Lignes pointillées : fréquences propres théoriques
•	Axe Y : échelle logarithmique
Graphique 2 : Premier Mode Propre
•	Courbe bleue : déformée modale normalisée
•	Ligne horizontale : position de référence
•	Triangles rouges : positions des appuis

