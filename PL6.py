import tkinter as tk
from tkinter import simpledialog, messagebox
import gurobipy as gp

class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PL1: Problème de réseau")

        # Style for the title
        title_style = {'font': ('Arial', 18, 'bold'), 'bg': '#050A30', 'fg': 'white'}

        # Title label
        self.title_label = tk.Label(root, text="PL6: Problème de réseau", **title_style)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Style for other labels and buttons
        label_style = {'font': ('Arial', 12)}
        button_style = {'font': ('Arial', 12, 'bold'), 'bg': '#050A30', 'fg': 'white'}

        self.nbNoeuds_label = tk.Label(root, text="Nombre de nœuds:", **label_style)
        self.nbNoeuds_label.grid(row=1, column=0, padx=10, pady=5)
        self.nbNoeuds_entry = tk.Entry(root, font=('Arial', 12))
        self.nbNoeuds_entry.grid(row=1, column=1, padx=10, pady=5)

        self.nbLiens_label = tk.Label(root, text="Nombre de liens:", **label_style)
        self.nbLiens_label.grid(row=2, column=0, padx=10, pady=5)
        self.nbLiens_entry = tk.Entry(root, font=('Arial', 12))
        self.nbLiens_entry.grid(row=2, column=1, padx=10, pady=5)

        self.solve_button = tk.Button(root, text="Résoudre", command=self.solve, **button_style)
        self.solve_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Labels for displaying results
        self.result_label = tk.Label(root, text="", **label_style)
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def solve(self):
        nbNoeuds_input = self.nbNoeuds_entry.get().strip()
        nbLiens_input = self.nbLiens_entry.get().strip()

        if not nbNoeuds_input or not nbLiens_input:
            messagebox.showerror("Erreur de saisie", "Veuillez saisir des valeurs pour le nombre de nœuds et de liens.")
            return

        try:
            nbNoeuds = int(nbNoeuds_input)
            nbLiens = int(nbLiens_input)
        except ValueError:
            messagebox.showerror("Erreur de saisie", "Veuillez saisir des valeurs entières pour le nombre de nœuds et de liens.")
            return

        if nbNoeuds <= 0 or nbLiens <= 0:
            messagebox.showerror("Erreur de saisie", "Veuillez saisir des valeurs positives pour le nombre de nœuds et de liens.")
            return

        m = gp.Model("Example")
        numTasks = nbLiens
        listeLiens = []
        listeNoeuds = []

        for i in range(nbNoeuds):
            ch = simpledialog.askstring("Input", f"Saisir le nom du noeud numero {i + 1}")
            if not ch:
                messagebox.showerror("Erreur de saisie", "Veuillez saisir un nom de noeud.")
                return
            listeNoeuds.append(ch)

        l1 = []
        cout = 0
        objCoeffs = []

        for i in range(nbLiens):
            l1 = []
            ch1 = simpledialog.askstring("Input", f"saisir le noeud du départ du lien numero {i + 1}")
            ch2 = simpledialog.askstring("Input", f"Saisir le noeud de destination du lien numero {i + 1}")
            cout_str = simpledialog.askstring("Input", f"saisir le cout du lien numero {i + 1}")
            if not ch1 or not ch2 or not cout_str:
                messagebox.showerror("Erreur de saisie", "Veuillez saisir des valeurs valides pour le lien.")
                return
            cout = int(cout_str)
            l1.append(ch1)
            l1.append(ch2)
            listeLiens.append(l1)
            objCoeffs.append(cout)

        x = m.addVars(numTasks, obj=objCoeffs, vtype=gp.GRB.BINARY)
        m.setObjective(x.prod(objCoeffs), gp.GRB.MINIMIZE)

        num1 = 0
        num2 = 0
        lindices1 = []
        lindices2 = []
        sum_var = 0

        for i in range(nbNoeuds):
            num1 = 0
            num2 = 0
            sum_var = 0
            lindices1 = []
            lindices2 = []

            for j in range(nbLiens):
                if listeLiens[j][0] == listeNoeuds[i]:
                    lindices1.append(j)
                    num1 += 1
                if listeLiens[j][1] == listeNoeuds[i]:
                    lindices2.append(j)
                    num2 += 1

            if num1 == 0:
                if num2 != 0:
                    # Point d'arrivée seulement
                    for k in lindices2:
                        sum_var += x[k]
                    m.addConstr(sum_var == 1)
            elif num2 == 0:
                if num1 != 0:
                    # Point de départ seulement
                    for k in lindices1:
                        sum_var += x[k]
                    m.addConstr(sum_var == 1)
            else:
                for k in lindices1:
                    sum_var += x[k]
                for k in lindices2:
                    sum_var -= x[k]
                m.addConstr(sum_var == 0)

        m.optimize()

        if m.status == gp.GRB.OPTIMAL:
            result_str = self.get_solution_str(m, listeLiens)
            self.result_label.config(text=result_str)
        elif m.status == gp.GRB.INFEASIBLE:
            messagebox.showinfo("Résultat", "Le modèle est infaisable.")
        elif m.status == gp.GRB.INF_OR_UNBD:
            messagebox.showinfo("Résultat", "Le modèle a une solution optimale infinie ou est non borné.")

    def get_solution_str(self, solution, listeLiens):
        result_str = "Solution optimale trouvée. Valeur de la fonction objectif : {}".format(solution.objVal)

        link_names = []
        for i in range(len(solution.getAttr('X'))):
            if solution.getAttr('X')[i] > 0.5:
                link_names.append(tuple(listeLiens[i]))

        link_str = "\n".join([f"({link[0]} -> {link[1]})" for link in link_names])

        result_str += "\n\nLiens de la solution : \n{}".format(link_str)

        return result_str


if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()
