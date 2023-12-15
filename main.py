import tkinter as tk
import subprocess

def execute_script(script_name):
    try:
        subprocess.run(["python", script_name])
    except Exception as e:
        print(f"Erreur lors de l'exécution du script {script_name} : {e}")

class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Projet de recherche opérationnelle")

        # Configuration des couleurs
        couleur_fond = "#f5f5dc"  # Beige
        couleur_bouton = "#050A30"  # Bleu

        # Définition de la taille de la fenêtre
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 40  # Adjust the value based on the taskbar size
        root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Arrière-plan de la fenêtre
        root.configure(bg=couleur_fond)

        # Titre stylisé
        label_titre = tk.Label(root, text="Solveur de Programme Linéaire", font=("Helvetica", 32, "bold"),
                               bg=couleur_fond, pady=30, padx=10)
        label_titre.pack(fill=tk.X)

        # Espace entre le titre et les boutons
        espace = tk.Frame(root, height=20, bg=couleur_fond)
        espace.pack()

        # Création d'un cadre pour les boutons
        cadre_boutons = tk.Frame(root, bg=couleur_fond)
        cadre_boutons.pack()

        # Création des neuf boutons avec des titres en bleu
        noms_boutons = [
            "PL1: Gestion optimal d'une zone agricole",
            "PL2: Gestion de la production",
            "PL3: Planification des besoins en ressources humaines",
            "PL4: Choix d'implémentation d'agence bancaire",
            "PL5: Probléme de positionnement",
            "PL6: Probléme de réseau"
        ]
        boutons = []

        for nom in noms_boutons:
            script_name = f"{nom.split(':')[0].strip()}.py"
            bouton = tk.Button(cadre_boutons, text=nom, width=50, height=2,
                              command=lambda script=script_name: execute_script(script), anchor="w")
            bouton.config(bg=couleur_bouton, fg="white", font=("Helvetica", 16, "bold"))
            boutons.append(bouton)

        # Affichage des boutons dans une grille avec une colonne
        for bouton in boutons:
            bouton.pack(pady=10, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()
