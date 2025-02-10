import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Exemple de grille de paires (valeur, indice de couleur)
grille = [
    [(1, 0), (2, 1), (3, 2)],
    [(4, 3), (5, 4), (6, 5)],
    [(7, 6), (8, 7), (9, 8)]
]

# Dimensions de la grille
rows = len(grille)
cols = len(grille[0])

# Créer une liste des couleurs à utiliser (ici des couleurs de matplotlib, mais tu peux personnaliser)
colormap = plt.cm.viridis
num_colors = len(colormap.colors)
color_indices = np.linspace(0, 1, num_colors)

# Extraire les valeurs à afficher et les indices de couleur
values = np.array([[item[0] for item in row] for row in grille])
color_indices_grid = np.array([[item[1] for item in row] for row in grille])

# Création de la figure
plt.figure(figsize=(6, 6))

# Afficher la grille avec les couleurs correspondant aux indices
plt.imshow(color_indices_grid, cmap='viridis', interpolation='nearest')

# Afficher les numéros sur chaque case
for i in range(rows):
    for j in range(cols):
        plt.text(j, i, str(values[i, j]), ha='center', va='center', color='white', fontsize=12)
plt.axis('off')
# Optionnel : ajouter une barre de couleur
plt.colorbar()

# Suppression des axes
plt.axis('off')

# Affichage
plt.show()
