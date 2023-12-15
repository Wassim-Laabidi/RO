import tkinter as tk
from tkinter import ttk, messagebox
import gurobipy as gp
from gurobipy import GRB

class Application:
    def __init__(self):
        self.result_window = None

    def relancer_optimisation(self):
        if self.result_window:
            self.result_window.destroy()
        self.interface_utilisateur()

    def optimisation_agences_serveurs_budget(self, a_percentage, b_percentage, c_percentage, n_regions, matrice_voisinage,
                                             populations, budget, cost_agence, cost_dab):
        model = gp.Model("Optimisation_Agences_Serveurs_Budget")

        X = model.addVars(n_regions, vtype=GRB.BINARY, name="X")
        Y = model.addVars(n_regions, vtype=GRB.BINARY, name="Y")

        obj_expr = gp.LinExpr()
        for i in range(n_regions):
            obj_expr += (a_percentage * X[i] + c_percentage * Y[i]) * populations[f'R{i + 1}']
            for j in range(n_regions):
                if j != i:
                    obj_expr += b_percentage * matrice_voisinage[i][j] * X[i] * populations[f'R{j + 1}']

        model.setObjective(obj_expr, GRB.MAXIMIZE)

        # Add budget constraint
        budget_expr = gp.LinExpr()
        for i in range(n_regions):
            budget_expr += (cost_agence * X[i] + cost_dab * Y[i])

        model.addConstr(budget_expr <= budget, "Budget")

        for i in range(n_regions):
            for j in range(n_regions):
                if j != i:
                    model.addConstr(X[i] * matrice_voisinage[i][j] + X[j] * matrice_voisinage[i][j] <= 1)

        for i in range(n_regions):
            model.addConstr(gp.quicksum(matrice_voisinage[i][j] * X[j] for j in range(n_regions)) + Y[i] >= 1)

        model.optimize()

        if model.status == GRB.OPTIMAL:
            if budget_expr.getValue() <= budget:
                # Afficher les résultats
                self.afficher_resultats(model, n_regions, X, Y)
            else:
                # Contrainte de budget non respectée
                self.afficher_erreur_budget()
        else:
            # Aucune solution optimale trouvée
            self.afficher_erreur_optimisation()

    def afficher_resultats(self, model, n_regions, X, Y):
        self.result_window = tk.Tk()
        self.result_window.title("Résultats")

        ttk.Label(self.result_window, text="Résultats de l'optimisation :").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(self.result_window, text="Optimal Solution:").grid(row=1, column=0, columnspan=2, pady=5)
        for i in range(n_regions):
            ttk.Label(self.result_window, text=f"Region {i + 1}: Agence={X[i].x}, Serveur DAB={Y[i].x}").grid(row=i + 2,column=0,columnspan=2,pady=2)

        ttk.Label(self.result_window, text=f"Total Number of Clients (millions): {int(model.objVal)}").grid(row=n_regions + 2, column=0,columnspan=2, pady=5)

        ttk.Button(self.result_window, text="Fermer", command=self.result_window.destroy).grid(row=n_regions + 3, column=0, columnspan=2, pady=10)

        self.result_window.mainloop()

    def afficher_erreur_budget(self):
        messagebox.showerror("Erreur", "Contrainte de budget non respectée. Veuillez ajuster les paramètres.")
        self.relancer_optimisation()

    def afficher_erreur_optimisation(self):
        messagebox.showerror("Erreur", "Aucune solution optimale trouvée. Veuillez ajuster les paramètres.")
        self.relancer_optimisation()

    def entrer_populations_par_region(self, n_regions):
        populations_par_region = {}

        fenetre = tk.Tk()
        fenetre.title("Saisie des Populations par Région")

        for i in range(n_regions):
            ttk.Label(fenetre, text=f"Entrez la population (millions) pour la région R{i + 1}:").grid(row=i, column=0, padx=5, pady=5)
            population_var = tk.IntVar()
            ttk.Entry(fenetre, textvariable=population_var).grid(row=i, column=1, padx=5, pady=5)
            populations_par_region[f'R{i + 1}'] = population_var

        bouton_valider = ttk.Button(fenetre, text="Valider", command=fenetre.destroy)
        bouton_valider.grid(row=n_regions, columnspan=2, pady=10)

        fenetre.mainloop()

        populations_par_region = {key: var.get() for key, var in populations_par_region.items()}
        return populations_par_region

    def sauvegarder_voisinage(self, n_regions, cases):
        matrice_voisinage = [[0 for _ in range(n_regions)] for _ in range(n_regions)]

        for i in range(n_regions):
            for j in range(n_regions):
                if i != j:
                    valeur = cases[i][j].get()
                    matrice_voisinage[i][j] = int(valeur)

        print("\nMatrice de voisinage :")
        noms_colonnes = [""] + [f"R{i}" for i in range(1, n_regions + 1)]
        print("   " + " ".join(noms_colonnes))
        for i in range(n_regions):
            ligne = [f"R{i + 1}"]
            for j in range(n_regions):
                ligne.append(str(matrice_voisinage[i][j]))
            print(" ".join(ligne))

        return matrice_voisinage

    def interface_voisinage(self, n_regions):
        global cases

        matrice_voisinage = [[0 for _ in range(n_regions)] for _ in range(n_regions)]

        fenetre = tk.Tk()
        fenetre.title("Interface de Voisinage")

        cases = [[tk.IntVar() for _ in range(n_regions)] for _ in range(n_regions)]

        for i in range(n_regions):
            ttk.Label(fenetre, text=f"R{i + 1}").grid(row=0, column=i + 1, padx=5, pady=5)
            ttk.Label(fenetre, text=f"R{i + 1}").grid(row=i + 1, column=0, padx=5, pady=5)

        for i in range(n_regions):
            for j in range(n_regions):
                if i != j:
                    case = ttk.Checkbutton(fenetre, variable=cases[i][j])
                    case.grid(row=i + 1, column=j + 1, padx=5, pady=5)

        bouton_sauvegarder = ttk.Button(fenetre, text="Sauvegarder", command=lambda: self.sauvegarder_voisinage(n_regions, cases))
        bouton_sauvegarder.grid(row=n_regions + 1, columnspan=n_regions, pady=10)

        fenetre.mainloop()

        for i in range(n_regions):
            for j in range(n_regions):
                if i != j:
                    matrice_voisinage[i][j] = int(cases[i][j].get())

        return matrice_voisinage

    def interface_utilisateur(self):
        fenetre = tk.Tk()
        fenetre.title("Interface Utilisateur")

        ttk.Label(fenetre, text="Pourcentage de la population de la région Ri pour une agence:").grid(row=0, column=0, padx=5, pady=5)
        a_percentage = tk.DoubleVar()
        ttk.Entry(fenetre, textvariable=a_percentage).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(fenetre, text="Pourcentage de la population des régions voisines pour une agence:").grid(row=1, column=0, padx=5, pady=5)
        b_percentage = tk.DoubleVar()
        ttk.Entry(fenetre, textvariable=b_percentage).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(fenetre, text="Pourcentage de la population de la région Ri pour un serveur DAB:").grid(row=2, column=0, padx=5, pady=5)
        c_percentage = tk.DoubleVar()
        ttk.Entry(fenetre, textvariable=c_percentage).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(fenetre, text="Entrez le nombre de régions:").grid(row=3, column=0, padx=5, pady=5)
        n_regions = tk.IntVar()
        ttk.Entry(fenetre, textvariable=n_regions).grid(row=3, column=1, padx=5, pady=5)

        bouton_valider = ttk.Button(fenetre, text="Valider", command=fenetre.destroy)
        bouton_valider.grid(row=4, columnspan=2, pady=10)

        fenetre.mainloop()

        return a_percentage.get(), b_percentage.get(), c_percentage.get(), n_regions.get()

if __name__ == "__main__":
    app = Application()
    a_percentage, b_percentage, c_percentage, n_regions =app.interface_utilisateur()
    populations =app.entrer_populations_par_region(n_regions)
    matrice_voisinage = app.interface_voisinage(n_regions)

    # Get the budget and costs from the user
    budget_window = tk.Tk()
    budget_window.title("Budget")
    ttk.Label(budget_window, text="Entrez le budget (en milliers de dinars):").grid(row=0, column=0, padx=5, pady=5)
    budget_var = tk.DoubleVar()
    ttk.Entry(budget_window, textvariable=budget_var).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(budget_window, text="Coût d'une agence (en milliers de dinars):").grid(row=1, column=0, padx=5, pady=5)
    cost_agence_var = tk.DoubleVar()
    ttk.Entry(budget_window, textvariable=cost_agence_var).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(budget_window, text="Coût d'un serveur DAB (en milliers de dinars):").grid(row=2, column=0, padx=5,
                                                                                         pady=5)
    cost_dab_var = tk.DoubleVar()
    ttk.Entry(budget_window, textvariable=cost_dab_var).grid(row=2, column=1, padx=5, pady=5)

    bouton_valider_budget = ttk.Button(budget_window, text="Valider", command=budget_window.destroy)
    bouton_valider_budget.grid(row=3, columnspan=2, pady=10)
    budget_window.mainloop()

    budget = budget_var.get()
    cost_agence = cost_agence_var.get()
    cost_dab = cost_dab_var.get()

    app.optimisation_agences_serveurs_budget(a_percentage, b_percentage, c_percentage, n_regions, matrice_voisinage,
                                         populations, budget, cost_agence, cost_dab)