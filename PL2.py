import gurobipy as gp
from gurobipy import GRB
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, Toplevel

def optimize_model(numMonths, Z, Sal, R, L, Hsup, Hmax, h1, C, Cs, NOinit, S0init, l):
    numTasks = 24
    m = gp.Model("Example")

    objCoeffs = []
    for i in range(numMonths):
        objCoeffs.append(Cs[i])
    for i in range(numMonths):
        objCoeffs.append(Sal)
    for i in range(numMonths):
        objCoeffs.append(Hsup)
    for i in range(numMonths):
        objCoeffs.append(R)
    for i in range(numMonths):
        objCoeffs.append(L)
    for i in range(numMonths):
        objCoeffs.append(C[i])

    x = m.addVars(numTasks, obj=objCoeffs, vtype=gp.GRB.CONTINUOUS)
    m.setObjective(x.prod(objCoeffs), gp.GRB.MINIMIZE)

    S = []
    NO = []
    NHS = []
    NOR = []
    NOL = []
    NCH = []

    for i in range(numMonths):
        S.append(x[i])
        NO.append(x[i + numMonths])
        NHS.append(x[i + 2 * numMonths])
        NOR.append(x[i + 3 * numMonths])
        NOL.append(x[i + 4 * numMonths])
        NCH.append(x[i + 5 * numMonths])

    S[0] = S0init
    Sfinal = 0

    for i in range(len(NHS)):
        m.addConstr(NHS[i] <= Hmax * NO[i])

    for i in range(len(S)):
        m.addConstr(S[i] + NCH[i] >= l[i])

    for i in range(len(NCH)):
        m.addConstr(NCH[i] <= (1 / h1) * (NHS[i] + NO[i] * Z))

    m.addConstr(NO[0] == NOinit + NOR[0] - NOL[0])

    i = 1
    while (i < len(S)):
        m.addConstr(NO[i] == NO[i - 1] + NOR[i] - NOL[i])
        i = i + 1

    for j in range(len(S) - 1):
        m.addConstr(S[j + 1] == S[j] + NCH[j] - l[j])

    m.addConstr(Sfinal == S[len(S) - 1] + NCH[len(S) - 1] - l[len(S) - 1])

    for i in range(len(S)):
        m.addConstr(S[i] >= 0)
        m.addConstr(Sfinal >= 0)
        m.addConstr(NOinit >= 0)
        m.addConstr(NO[i] >= 0)
        m.addConstr(NOR[i] >= 0)
        m.addConstr(NOL[i] >= 0)
        m.addConstr(NHS[i] >= 0)

    m.optimize()

    # Display the results in a new window
    result_window = tk.Toplevel(root)
    result_window.title("Optimization Results")

    result_label = Label(result_window, text="Optimization Results:")
    result_label.pack()

    result_text = "Objective Value: {}\n".format(m.objVal)
    result_text += "Decision Variables:\n"
    for i, var in enumerate(m.getVars()):
        result_text += "{}: {}\n".format(var.varName, var.x)
    result_display = Label(result_window, text=result_text)
    result_display.pack()

    # Allow the user to close the result window
    close_button = Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack()

# Fonction pour obtenir les données de l'utilisateur et exécuter le modèle d'optimisation
def get_user_input():
    numMonths = int(months_entry.get())
    Z = int(volume_entry.get())
    Sal = int(salary_entry.get())
    R = int(recruitment_entry.get())
    L = int(licensing_entry.get())
    Hsup = int(hourly_sup_cost_entry.get())
    Hmax = int(max_hourly_sup_entry.get())
    h1 = int(hours_per_pair_entry.get())

    C = []
    Cs = []
    l = []

    for i in range(numMonths):
        production_cost = int(production_cost_entries[i].get())
        C.append(production_cost)

        storage_cost = int(storage_cost_entries[i].get())
        Cs.append(storage_cost)

        demand = int(demand_entries[i].get())
        l.append(demand)

    NOinit = int(initial_workers_entry.get())
    S0init = int(initial_stock_entry.get())

    optimize_model(numMonths, Z, Sal, R, L, Hsup, Hmax, h1, C, Cs, NOinit, S0init, l)

# Fonction pour créer la fenêtre de dialogue pour spécifier le nombre de mois
def get_num_months():
    num_months_window = Toplevel(root)
    num_months_window.title("Specify Number of Months")

    num_months_label = Label(num_months_window, text="Enter the number of months:")
    num_months_label.pack()

    num_months_entry = Entry(num_months_window)
    num_months_entry.pack()

    confirm_button = Button(num_months_window, text="Confirm", command=lambda: create_input_fields(num_months_entry.get(), num_months_window))
    confirm_button.pack()

# Fonction pour créer dynamiquement les champs d'entrée en fonction du nombre de mois spécifié
def create_input_fields(num_months, window):
    try:
        num_months = int(num_months)
        window.destroy()

        for i in range(num_months):
            Label(root, text=f"Month {i + 1} Production Cost:").grid(row=10 + i, column=0)
            production_cost_entry = Entry(root)
            production_cost_entry.grid(row=10 + i, column=1)
            production_cost_entries.append(production_cost_entry)

            Label(root, text=f"Month {i + 1} Storage Cost:").grid(row=22 + i, column=0)
            storage_cost_entry = Entry(root)
            storage_cost_entry.grid(row=22 + i, column=1)
            storage_cost_entries.append(storage_cost_entry)

            Label(root, text=f"Month {i + 1} Demand:").grid(row=34 + i, column=0)
            demand_entry = Entry(root)
            demand_entry.grid(row=34 + i, column=1)
            demand_entries.append(demand_entry)

        optimize_button = Button(root, text="Optimize", command=get_user_input)
        optimize_button.grid(row=46, column=0, columnspan=2)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of months.")

# Créer la fenêtre principale Tkinter
root = tk.Tk()
root.title("Optimization Model")

# Créer et placer les étiquettes et les widgets d'entrée pour les données utilisateur
Label(root, text="Number of Months:").grid(row=0, column=0)
months_entry = Entry(root)
months_entry.grid(row=0, column=1)

Label(root, text="Volume Hourly Work:").grid(row=1, column=0)
volume_entry = Entry(root)
volume_entry.grid(row=1, column=1)

Label(root, text="Salary per Worker:").grid(row=2, column=0)
salary_entry = Entry(root)
salary_entry.grid(row=2, column=1)

Label(root, text="Recruitment Cost:").grid(row=3, column=0)
recruitment_entry = Entry(root)
recruitment_entry.grid(row=3, column=1)

Label(root, text="Licensing Cost:").grid(row=4, column=0)
licensing_entry = Entry(root)
licensing_entry.grid(row=4, column=1)

Label(root, text="Hourly Sup. Cost:").grid(row=5, column=0)
hourly_sup_cost_entry = Entry(root)
hourly_sup_cost_entry.grid(row=5, column=1)

Label(root, text="Max Hourly Sup. Hours:").grid(row=6, column=0)
max_hourly_sup_entry = Entry(root)
max_hourly_sup_entry.grid(row=6, column=1)

Label(root, text="Hours per Pair:").grid(row=7, column=0)
hours_per_pair_entry = Entry(root)
hours_per_pair_entry.grid(row=7, column=1)

Label(root, text="Initial Workers:").grid(row=8, column=0)
initial_workers_entry = Entry(root)
initial_workers_entry.grid(row=8, column=1)

Label(root, text="Initial Stock:").grid(row=9, column=0)
initial_stock_entry = Entry(root)
initial_stock_entry.grid(row=9, column=1)

# Bouton pour déclencher le modèle d'optimisation
num_months_button = Button(root, text="Specify Number of Months", command=get_num_months)
num_months_button.grid(row=10, column=0, columnspan=2)

# Listes pour stocker les champs d'entrée dynamiques
production_cost_entries = []
storage_cost_entries = []
demand_entries = []

# Exécuter la boucle principale Tkinter
root.mainloop()
