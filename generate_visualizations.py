import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

# Créer le dossier pour les graphiques
output_dir = Path("results/visualizations")
output_dir.mkdir(parents=True, exist_ok=True)

# Données des résultats
images = ["10 colis\n(2)", "10 colis", "12 colis", "26 colis", "28.30 colis", "52 colis"]
attendus = [10, 10, 12, 26, 28, 52]

# Résultats par solution
opencv_results = [32, 22, 17, 4, 11, 3]
chatgpt_results = [6, 8, 18, 20, 45, 80]
detr_results = [0, 15, 0, None, None, None]  # Données incomplètes

print("=" * 80)
print("GÉNÉRATION DES GRAPHIQUES - COMPTAGE DE COLIS")
print("=" * 80)

# Configuration du style
plt.style.use('seaborn-v0_8-darkgrid')
colors_custom = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

# ============================================================================
# GRAPHIQUE 1: Comparaison Détecté vs Attendu par Image
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

x = np.arange(len(images))
width = 0.25

bars1 = ax.bar(x - width, attendus, width, label='Attendu', color='#2C7873', alpha=0.9)
bars2 = ax.bar(x, opencv_results, width, label='OpenCV', color='#E63946', alpha=0.8)
bars3 = ax.bar(x + width, chatgpt_results, width, label='ChatGPT', color='#457B9D', alpha=0.8)

ax.set_xlabel('Images', fontsize=14, fontweight='bold')
ax.set_ylabel('Nombre de colis', fontsize=14, fontweight='bold')
ax.set_title('Comparaison des détections par solution', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(images, fontsize=11)
ax.legend(fontsize=12, loc='upper left')
ax.grid(axis='y', alpha=0.3)

# Ajouter les valeurs sur les barres
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'comparaison_detections.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 1 créé: comparaison_detections.png")
plt.close()

# ============================================================================
# GRAPHIQUE 2: Erreurs absolues par solution
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

opencv_errors = [abs(o - a) for o, a in zip(opencv_results, attendus)]
chatgpt_errors = [abs(c - a) for c, a in zip(chatgpt_results, attendus)]

x = np.arange(len(images))
width = 0.35

bars1 = ax.bar(x - width/2, opencv_errors, width, label='OpenCV', color='#E63946', alpha=0.8)
bars2 = ax.bar(x + width/2, chatgpt_errors, width, label='ChatGPT', color='#457B9D', alpha=0.8)

ax.set_xlabel('Images', fontsize=14, fontweight='bold')
ax.set_ylabel('Erreur absolue (nombre de colis)', fontsize=14, fontweight='bold')
ax.set_title('Erreurs de comptage par image', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(images, fontsize=11)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

# Ajouter les valeurs
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Ajouter une ligne de référence à 0
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

plt.tight_layout()
plt.savefig(output_dir / 'erreurs_absolues.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 2 créé: erreurs_absolues.png")
plt.close()

# ============================================================================
# GRAPHIQUE 3: Erreur moyenne par solution
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 7))

solutions = ['OpenCV', 'ChatGPT']
erreurs_moyennes = [
    np.mean(opencv_errors),
    np.mean(chatgpt_errors)
]

bars = ax.barh(solutions, erreurs_moyennes, color=['#E63946', '#457B9D'], alpha=0.8)
ax.set_xlabel('Erreur moyenne (colis)', fontsize=14, fontweight='bold')
ax.set_title('Erreur moyenne de comptage par solution', fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Ajouter les valeurs
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2.,
            f'{erreurs_moyennes[i]:.1f} colis',
            ha='left', va='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'erreur_moyenne.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 3 créé: erreur_moyenne.png")
plt.close()

# ============================================================================
# GRAPHIQUE 4: Précision par taille de palette
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 8))

# Regrouper par taille
petites = [0, 1]  # 10 colis
moyennes = [2, 3, 4]  # 12-28 colis
grandes = [5]  # 52 colis

def calc_precision(indices, results, attendus):
    errors = [abs(results[i] - attendus[i]) / attendus[i] * 100 for i in indices]
    return 100 - np.mean(errors)

categories = ['Petites\n(10 colis)', 'Moyennes\n(12-28 colis)', 'Grandes\n(52 colis)']

opencv_precision = [
    calc_precision(petites, opencv_results, attendus),
    calc_precision(moyennes, opencv_results, attendus),
    calc_precision(grandes, opencv_results, attendus)
]

chatgpt_precision = [
    calc_precision(petites, chatgpt_results, attendus),
    calc_precision(moyennes, chatgpt_results, attendus),
    calc_precision(grandes, chatgpt_results, attendus)
]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, opencv_precision, width, label='OpenCV', color='#E63946', alpha=0.8)
bars2 = ax.bar(x + width/2, chatgpt_precision, width, label='ChatGPT', color='#457B9D', alpha=0.8)

ax.set_ylabel('Précision (%)', fontsize=14, fontweight='bold')
ax.set_xlabel('Taille de palette', fontsize=14, fontweight='bold')
ax.set_title('Précision par taille de palette', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(-150, 100)

# Ajouter les valeurs
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height < 0:
            va = 'top'
            y_offset = -3
        else:
            va = 'bottom'
            y_offset = 3
        ax.text(bar.get_x() + bar.get_width()/2., height + y_offset,
                f'{height:.0f}%',
                ha='center', va=va, fontsize=10, fontweight='bold')

# Ligne de référence à 100%
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Seuil acceptable')

plt.tight_layout()
plt.savefig(output_dir / 'precision_par_taille.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 4 créé: precision_par_taille.png")
plt.close()

# ============================================================================
# GRAPHIQUE 5: Coût et précision - Trade-off
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 8))

solutions_cost = ['OpenCV', 'ChatGPT', 'YOLOv8\n(après training)', 'DETR\n(pré-entraîné)']
costs = [0, 15, 0, 0]  # €/mois pour 1000 images
precisions = [0, 58, 95, 30]  # % estimé

# Taille des bulles proportionnelle à la facilité d'implémentation
ease_of_use = [500, 1000, 300, 400]  # Taille relative

colors_map = ['#E63946', '#457B9D', '#06A77D', '#F18F01']

for i, (sol, cost, prec, ease, color) in enumerate(zip(solutions_cost, costs, precisions, ease_of_use, colors_map)):
    ax.scatter(cost, prec, s=ease, alpha=0.6, color=color, edgecolors='black', linewidth=2)
    ax.annotate(sol, (cost, prec), fontsize=11, fontweight='bold', 
                ha='center', va='center')

ax.set_xlabel('Coût mensuel (€ pour 1000 images)', fontsize=14, fontweight='bold')
ax.set_ylabel('Précision estimée (%)', fontsize=14, fontweight='bold')
ax.set_title('Rapport Coût / Précision des solutions', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.set_xlim(-2, 20)
ax.set_ylim(-5, 105)

# Zone optimale
ax.axhspan(80, 100, alpha=0.1, color='green', label='Zone haute précision')
ax.axvspan(0, 5, alpha=0.1, color='blue', label='Zone faible coût')

ax.legend(fontsize=10, loc='lower right')

plt.tight_layout()
plt.savefig(output_dir / 'cout_vs_precision.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 5 créé: cout_vs_precision.png")
plt.close()

# ============================================================================
# GRAPHIQUE 6: Tendance OpenCV vs ChatGPT
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Sous-graphique 1: OpenCV
ax1.plot(attendus, attendus, 'k--', label='Détection parfaite', linewidth=2)
ax1.scatter(attendus, opencv_results, color='#E63946', s=200, alpha=0.7, edgecolors='black', linewidth=2)
ax1.plot(attendus, opencv_results, color='#E63946', alpha=0.5, linewidth=2)

for i, (x, y) in enumerate(zip(attendus, opencv_results)):
    ax1.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(10,5), 
                ha='center', fontsize=10, fontweight='bold')

ax1.set_xlabel('Nombre attendu', fontsize=13, fontweight='bold')
ax1.set_ylabel('Nombre détecté', fontsize=13, fontweight='bold')
ax1.set_title('OpenCV - Détections vs Attendu', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Sous-graphique 2: ChatGPT
ax2.plot(attendus, attendus, 'k--', label='Détection parfaite', linewidth=2)
ax2.scatter(attendus, chatgpt_results, color='#457B9D', s=200, alpha=0.7, edgecolors='black', linewidth=2)
ax2.plot(attendus, chatgpt_results, color='#457B9D', alpha=0.5, linewidth=2)

for i, (x, y) in enumerate(zip(attendus, chatgpt_results)):
    ax2.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(10,5), 
                ha='center', fontsize=10, fontweight='bold')

ax2.set_xlabel('Nombre attendu', fontsize=13, fontweight='bold')
ax2.set_ylabel('Nombre détecté', fontsize=13, fontweight='bold')
ax2.set_title('ChatGPT - Détections vs Attendu', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'tendance_detections.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 6 créé: tendance_detections.png")
plt.close()

# ============================================================================
# GRAPHIQUE 7: Dashboard récapitulatif
# ============================================================================
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Titre principal
fig.suptitle('DASHBOARD - ÉVALUATION DES SOLUTIONS DE COMPTAGE DE COLIS', 
             fontsize=20, fontweight='bold', y=0.98)

# 1. Erreur moyenne (grand)
ax1 = fig.add_subplot(gs[0, :2])
solutions = ['OpenCV', 'ChatGPT']
erreurs = [np.mean(opencv_errors), np.mean(chatgpt_errors)]
bars = ax1.barh(solutions, erreurs, color=['#E63946', '#457B9D'], alpha=0.8)
ax1.set_xlabel('Erreur moyenne (colis)', fontsize=11, fontweight='bold')
ax1.set_title('Erreur moyenne par solution', fontsize=13, fontweight='bold')
for i, bar in enumerate(bars):
    ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2.,
            f'{erreurs[i]:.1f}', ha='left', va='center', fontsize=11, fontweight='bold')

# 2. Taux de réussite (petit)
ax2 = fig.add_subplot(gs[0, 2])
success_rate = [0, 17]  # % (seuil ±2 colis)
bars = ax2.bar(solutions, success_rate, color=['#E63946', '#457B9D'], alpha=0.8)
ax2.set_ylabel('Précision (%)', fontsize=11, fontweight='bold')
ax2.set_title('Taux de réussite\n(±2 colis)', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 100)
for i, bar in enumerate(bars):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
            f'{success_rate[i]}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 3. Erreurs par image (moyen)
ax3 = fig.add_subplot(gs[1, :])
x = np.arange(len(images))
width = 0.35
bars1 = ax3.bar(x - width/2, opencv_errors, width, label='OpenCV', color='#E63946', alpha=0.8)
bars2 = ax3.bar(x + width/2, chatgpt_errors, width, label='ChatGPT', color='#457B9D', alpha=0.8)
ax3.set_xlabel('Images', fontsize=11, fontweight='bold')
ax3.set_ylabel('Erreur absolue', fontsize=11, fontweight='bold')
ax3.set_title('Erreurs par image', fontsize=13, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(images, fontsize=9)
ax3.legend(fontsize=10)
ax3.grid(axis='y', alpha=0.3)

# 4. Coût mensuel
ax4 = fig.add_subplot(gs[2, 0])
costs_month = [0, 15, 0, 1000]
solutions_all = ['OpenCV', 'ChatGPT', 'YOLOv8', 'DETR']
colors_all = ['#E63946', '#457B9D', '#06A77D', '#F18F01']
bars = ax4.bar(range(len(solutions_all)), costs_month, color=colors_all, alpha=0.8)
ax4.set_ylabel('Coût (€/mois)', fontsize=10, fontweight='bold')
ax4.set_title('Coût mensuel\n(1000 images)', fontsize=11, fontweight='bold')
ax4.set_xticks(range(len(solutions_all)))
ax4.set_xticklabels(solutions_all, fontsize=9, rotation=15)
ax4.set_yscale('log')
ax4.set_ylim(0.1, 2000)

# 5. Vitesse de traitement
ax5 = fig.add_subplot(gs[2, 1])
speeds = [0.5, 3, 2, 4]  # secondes par image
bars = ax5.bar(range(len(solutions_all)), speeds, color=colors_all, alpha=0.8)
ax5.set_ylabel('Temps (sec/image)', fontsize=10, fontweight='bold')
ax5.set_title('Vitesse de traitement', fontsize=11, fontweight='bold')
ax5.set_xticks(range(len(solutions_all)))
ax5.set_xticklabels(solutions_all, fontsize=9, rotation=15)
for i, bar in enumerate(bars):
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
            f'{speeds[i]}s', ha='center', va='bottom', fontsize=9, fontweight='bold')

# 6. Recommandation
ax6 = fig.add_subplot(gs[2, 2])
ax6.axis('off')
recommendation_text = """
RECOMMANDATION:

🥇 Court terme:
   ChatGPT (58%)
   
⚠️ Avec validation
   humaine pour >30 colis

🥇 Moyen terme:
   YOLOv8 custom (95%+)
   
💰 Budget total:
   500-1000€ (setup)
   0€/mois (après)
"""
ax6.text(0.1, 0.5, recommendation_text, fontsize=10, verticalalignment='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.savefig(output_dir / 'dashboard_complet.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 7 créé: dashboard_complet.png")
plt.close()

# ============================================================================
# Résumé final
# ============================================================================
print("\n" + "=" * 80)
print("✅ GÉNÉRATION TERMINÉE")
print("=" * 80)
print(f"\n📁 Tous les graphiques ont été sauvegardés dans: {output_dir.absolute()}\n")
print("Fichiers créés:")
print("  1. comparaison_detections.png    - Comparaison des détections")
print("  2. erreurs_absolues.png          - Erreurs par image")
print("  3. erreur_moyenne.png            - Erreur moyenne globale")
print("  4. precision_par_taille.png      - Précision selon taille palette")
print("  5. cout_vs_precision.png         - Rapport coût/performance")
print("  6. tendance_detections.png       - Tendance des détections")
print("  7. dashboard_complet.png         - Dashboard récapitulatif complet")
print("\n" + "=" * 80)
