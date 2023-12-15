import tkinter as tk
from tkinter import simpledialog, messagebox
import gurobipy as gp
from gurobipy import Model, GRB

# Structure de la culture
class Culture:
    def __init__(self, nom, R, PU, MO, HM, E, SMO, FX):
        self.nom = nom
        self.R = R  # Rendement (Quantité / hectare)
        self.PU = PU  # Prix unité
        self.MO = MO  # Main d'oeuvre (/ hectare)
        self.HM = HM  # Heure machine (/ hectare)
        self.E = E  # Eau (mètre cube / hectare)
        self.SMO = SMO  # Salaire annuel (/ouvrier)
        self.FX = FX  # Frais fixes

# Interface utilisateur pour entrer les données des cultures
class CultureEntryUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Entrée des données des cultures")

        # Stocker les cultures dans une liste
        self.cultures = []

        # Demander les ressources disponibles
        self.main_oeuvre_dispo = simpledialog.askinteger("Ressources", "Entrez la main d'œuvre disponible (ouvriers):", initialvalue=3000)
        self.eau_dispo = simpledialog.askinteger("Ressources", "Entrez la quantité d'eau disponible (m3):", initialvalue=2500000)
        self.heures_machine_dispo = simpledialog.askinteger("Ressources", "Entrez le temps machine disponible (heures):", initialvalue=24000)
        self.surface_max = simpledialog.askinteger("Ressources", "Entrez la surface totale de la zone agricole (ha):", initialvalue=1000)

        # Demander les valeurs 30 et 0.1 à l'utilisateur
        self.heures_machine_cout = simpledialog.askfloat("Coût des heures machine", "Entrez le coût des heures machine (UM/H):", initialvalue=30.0)
        self.eau_cout = simpledialog.askfloat("Coût de l'eau", "Entrez le coût de l'eau (UM/m3):", initialvalue=0.1)

        # Demander le nombre de cultures
        self.nb_cultures = simpledialog.askinteger("Nombre de cultures", "Entrez le nombre de cultures:", minvalue=1, maxvalue=10)

        for i in range(self.nb_cultures):
            # Demander les informations pour chaque culture
            nom = simpledialog.askstring("Nom de la culture", f"Entrez le nom de la culture {i+1}:", initialvalue=f"Culture {i+1}")
            R = simpledialog.askfloat("Rendement", f"Entrez le rendement pour {nom} (Q/ha):")
            PU = simpledialog.askfloat("Prix de vente", f"Entrez le prix de vente pour {nom} (UM/Q):")
            MO = simpledialog.askfloat("Main d'oeuvre", f"Entrez la main d'oeuvre pour {nom} (Ouvriers/ha):")
            HM = simpledialog.askfloat("Temps machine", f"Entrez le temps machine pour {nom} (H/ha):")
            E = simpledialog.askfloat("Eau", f"Entrez l'eau nécessaire pour {nom} (m3/ha):")
            SMO = simpledialog.askfloat("Salaire annuel", f"Entrez le salaire annuel par ouvrier pour {nom}:")
            FX = simpledialog.askfloat("Frais fixe de gestion", f"Entrez les frais fixes de gestion pour {nom}:")

            # Créer et ajouter l'objet Culture
            self.cultures.append(Culture(nom, R, PU, MO, HM, E, SMO, FX))

        # Ajouter un bouton pour exécuter l'optimisation
        self.optimize_button = tk.Button(self.root, text="Optimiser", command=self.optimize)
        self.optimize_button.pack()

    def optimize(self):
        try:
            model = gp.Model("Optimisation agricole")

            # Variables de décision : nombre d'hectares pour chaque culture
            x = model.addVars([culture.nom for culture in self.cultures], name="x", vtype=GRB.INTEGER)

            # Fonction objectif : maximiser le bénéfice net total
            model.setObjective(
                gp.quicksum((culture.R * culture.PU - culture.MO * culture.SMO - culture.HM * self.heures_machine_cout - culture.E * self.eau_cout) * x[culture.nom] - culture.FX
                            for culture in self.cultures),
                GRB.MAXIMIZE)

            # Contraintes
            model.addConstr(gp.quicksum(culture.MO * x[culture.nom] for culture in self.cultures) <= self.main_oeuvre_dispo, "Main d'oeuvre")
            model.addConstr(gp.quicksum(culture.E * x[culture.nom] for culture in self.cultures) <= self.eau_dispo, "Eau d'irrigation")
            model.addConstr(gp.quicksum(culture.HM * x[culture.nom] for culture in self.cultures) <= self.heures_machine_dispo, "Heures machine")
            model.addConstr(gp.quicksum(x[culture.nom] for culture in self.cultures) <= self.surface_max, "Surface totale")

            # Exécuter le modèle
            model.optimize()

            # Afficher les résultats
            if model.status == GRB.OPTIMAL:
                result_window = tk.Toplevel(self.root)
                result_window.title("Résultats")
                result_window.geometry("+500+250")

                text_widget = tk.Text(result_window, wrap=tk.WORD, width=40, height=10)
                text_widget.pack(padx=10, pady=10)

                for culture in self.cultures:
                    text_widget.insert(tk.END, f"{culture.nom}: {x[culture.nom].X:.2f} hectares\n")
                text_widget.insert(tk.END, f"\nBénéfice total : {model.objVal:.2f} UM")

                text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
            else:
                messagebox.showinfo("Résultat", "Optimisation terminée sans solution optimale.")
        except gp.GurobiError as e:
            messagebox.showerror("Erreur Gurobi", f"Erreur Gurobi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CultureEntryUI(root)
    root.mainloop()