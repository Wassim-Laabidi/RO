import tkinter as tk
from tkinter import simpledialog, messagebox
from gurobipy import Model, GRB

# Fonction d'optimisation qui sera appelée lorsque l'utilisateur cliquera sur le bouton "Optimiser"
def optimize():
    try:
        # Extraction des coefficients des contraintes de l'interface
        constraint_values = [float(constraint_entry.get()) if constraint_entry.get() else 0.0 for constraint_entry in constraint_entries]

        if any(value < 0 for value in constraint_values):
            raise ValueError("Les valeurs des contraintes doivent être positives.")

        # Création du modèle Gurobi
        m = Model("Example")
        x = m.addVars(numTasks, obj=[1, 1, 1, 1, 1, 1, 1], vtype=GRB.CONTINUOUS)

        # Ajout des contraintes avec les coefficients entrés
        m.addConstr(x[0] + x[3] + x[4] + x[5] + x[6] >= constraint_values[0])
        m.addConstr(x[0] + x[1] + x[4] + x[5] + x[6] >= constraint_values[1])
        m.addConstr(x[0] + x[1] + x[2] + x[5] + x[6] >= constraint_values[2])
        m.addConstr(x[0] + x[1] + x[2] + x[3] + x[6] >= constraint_values[3])
        m.addConstr(x[0] + x[1] + x[2] + x[4] + x[5] >= constraint_values[4])
        m.addConstr(x[1] + x[2] + x[3] + x[4] + x[5] >= constraint_values[5])
        m.addConstr(x[2] + x[3] + x[4] + x[5] + x[6] >= constraint_values[6])

        for i in range(numTasks):
            m.addConstr(x[i] >= 0)

        # Optimisation
        m.optimize()

        # Affichage de la valeur de la fonction objectif
        if m.status == GRB.OPTIMAL:
            result_text = f'Valeur de la fonction objectif: {m.objVal:.2f}'
        else:
            result_text = "Aucune solution optimale trouvée ou problème non réalisable."

    except ValueError as e:
        result_text = str(e)

    result_label.config(text=result_text)

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
additional_text = "Un bureau de poste a des besoins en personnel pour les sept jours de la semaine, comme indiqué dans le tableau suivant. Déterminez la planification permettant de satisfaire les besoins du bureau en recourant au minimum d'employés, en tenant compte du fait que chaque employé doit travailler pendant cinq jours consécutifs avant de prendre deux jours de congé."
# Titre du tableau
title_label = tk.Label(root, text="PL 3 : Planification des besoins en ressources humaines", font=("Arial", 24, "bold"), bg=button_color, fg=text_color)
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

# Entêtes de colonnes
columns = ["Jour", "Nombre employé minimum requis"]
for i, column in enumerate(columns):
    label = tk.Label(data_frame, text=column, font=label_font, bg=button_color, fg=text_color)
    label.grid(row=0, column=i, sticky="nsew", padx=10, pady=10)

# Données du tableau et entrées pour les coefficients
days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
numTasks = len(days)
constraint_entries = []

preset_values = [17, 13, 15, 19, 14, 16, 11]

for i in range(numTasks):
    # Jour
    label = tk.Label(data_frame, text=days[i], font=entry_font, bg=button_color, fg=text_color)
    label.grid(row=i+1, column=0, sticky="nsew", padx=10, pady=10)

    # Entrée pour le coefficient avec les valeurs prédéfinies
    entry = tk.Entry(data_frame, font=entry_font, bg="light grey")
    entry.insert(0, preset_values[i])  # Insert preset value
    entry.grid(row=i+1, column=1, sticky="nsew", padx=10, pady=10)
    constraint_entries.append(entry)

# Bouton pour exécuter l'optimisation
submit_button = tk.Button(root, text="Optimiser", command=optimize, font=label_font, bg=button_color, fg=text_color)
submit_button.pack(side="bottom", fill="x", padx=10, pady=10)

# Étiquette pour afficher le résultat
result_label = tk.Label(root, text="", font=("Arial", 16), bg=result_color)
result_label.pack(side="bottom", fill="x", padx=10, pady=10)

# Démarrage de l'interface graphique
root.mainloop()
