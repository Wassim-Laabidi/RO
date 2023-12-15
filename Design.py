import tkinter as tk
from gurobipy import Model, GRB

# Configuration de l'interface graphique
root = tk.Tk()
root.title("Programme linéaire 3")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 100  # Adjust the value based on the taskbar size
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Style personnalisé pour les entrées et les étiquettes
entry_font = ("Arial", 14)
label_font = ("Arial", 14, "bold")

# Couleurs personnalisées
background_color = "#FFF"
button_color = "#050A30"
text_color = "#FFF"
result_color = "white"

# Texte additionnel
additional_text = "text"
# Titre du tableau
title_label = tk.Label(root, text="PL 1 : Gestion optimale d’une zone agricole", font=("Arial", 24, "bold"), bg=button_color, fg=text_color)
title_label.pack(fill="x")

# Texte additionnel compact
additional_label = tk.Label(root, text=additional_text, font=("Arial", 12), bg=background_color, wraplength=800)
additional_label.pack(fill="x", padx=10, pady=5)

# Label for additional warning
warning_label = tk.Label(root, text="Veuillez donner des valeurs positives.", font=("Arial", 12, "bold"), fg="red", bg=background_color)
warning_label.pack(fill="x", padx=10, pady=0)  # Reduce pady to lower the distance

# Cadre pour les entrées de données
data_frame = tk.Frame(root, bg=background_color)
data_frame.pack(padx=10, pady=0, anchor='center')  # Reduce pady to lower the distance

#make your changes here

# Bouton pour exécuter l'optimisation
submit_button = tk.Button(root, text="Optimiser", command="optimize", font=label_font, bg=button_color, fg=text_color)
submit_button.pack(side="bottom", fill="x", padx=10, pady=10)

# Étiquette pour afficher le résultat
result_label = tk.Label(root, text="", font=("Arial", 16), bg=result_color)
result_label.pack(side="bottom", fill="x", padx=10, pady=10)

# Démarrage de l'interface graphique
root.mainloop()
