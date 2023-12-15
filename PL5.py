import gurobipy as gp
import tkinter as tk
from tkinter import ttk

class MatrixInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Input")

        self.num_zones = tk.IntVar()
        self.num_antennes = tk.IntVar()
        self.checkboxes = []
        self.zone_antenna_entries = []

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Number of Zones:").grid(row=0, column=0)
        ttk.Entry(self.root, textvariable=self.num_zones).grid(row=0, column=1)

        ttk.Label(self.root, text="Number of Antennas:").grid(row=1, column=0)
        ttk.Entry(self.root, textvariable=self.num_antennes).grid(row=1, column=1)

        ttk.Button(self.root, text="Create neighborhood matrix ", command=self.create_matrix).grid(row=2, column=0, columnspan=2)

    def create_matrix(self):
        num_zones = self.num_zones.get()
        num_antennes = self.num_antennes.get()

        matrix_window = tk.Toplevel(self.root)
        matrix_window.title("Matrix Input")

        # Add column labels
        ttk.Label(matrix_window, text="Contraintes").grid(row=0, column= num_antennes+1, padx=10)
        for j in range(num_antennes):
            ttk.Label(matrix_window, text=f"Antenna {j + 1}").grid(row=0, column=j + 1, padx=10)

        # Add row labels, checkboxes, and a single entry for the number of antennas in each zone
        for i in range(num_zones):
            ttk.Label(matrix_window, text=f"Zone {i + 1}").grid(row=i + 1, column=0, padx=10)
            row_checkboxes = []
            for j in range(num_antennes):
                var = tk.IntVar()
                checkbox = ttk.Checkbutton(matrix_window, variable=var)
                checkbox.grid(row=i + 1, column=j + 1)
                row_checkboxes.append(var)
            self.checkboxes.append(row_checkboxes)

            entry_var = tk.StringVar()
            entry = ttk.Entry(matrix_window, textvariable=entry_var)
            entry.grid(row=i + 1, column=num_antennes + 1)
            self.zone_antenna_entries.append(entry_var)

        # Add Constraints box
        constraints_frame = ttk.LabelFrame(matrix_window, text="Constraints")
        constraints_frame.grid(row=num_zones + 2, column=0, columnspan=num_antennes + 2, pady=10)

        ttk.Button(matrix_window, text="Optimize", command=lambda: self.optimize_matrix(num_antennes)).grid(row=num_zones + 3, column=0, columnspan=num_antennes + 2)

    def optimize_matrix(self, num_antennes):
        num_zones = len(self.checkboxes)

        antenne_matrix = [[self.checkboxes[i][j].get() for j in range(num_antennes)] for i in range(num_zones)]
        num_antennas_per_zone = [int(entry.get()) for entry in self.zone_antenna_entries]

        m = gp.Model("Example")
        obj_coeffs = [1] * num_antennes

        x = m.addVars(num_antennes, obj=obj_coeffs, vtype=gp.GRB.BINARY)
        m.setObjective(x.prod(obj_coeffs), gp.GRB.MINIMIZE)

        # Constraint: Each zone must have at least the specified number of antennas
        for i in range(num_zones):
            sum_var = gp.quicksum(x[j] * antenne_matrix[i][j] for j in range(num_antennes))
            m.addConstr(sum_var >= num_antennas_per_zone[i], name=f"AtLeastAntennasInZone{i + 1}")

        m.optimize()

        result_window = tk.Toplevel(self.root)
        result_window.title("Optimization Result")

        if m.status == gp.GRB.OPTIMAL:
            result_label = ttk.Label(result_window, text=f"Optimal Solution found. Objective function value: {m.objVal}")
            result_label.grid(row=0, column=0, columnspan=2)

            for j in range(num_antennes):
                ttk.Label(result_window, text=f"Antenna {j + 1}").grid(row=1, column=j + 1)

            for j in range(num_antennes):
                ttk.Label(result_window, text=f"AtLeastAntennasInZone{j + 1}").grid(row=2, column=j + 1)

            for j in range(num_antennes):
                ttk.Label(result_window, text=f"{x[j].X}").grid(row=3, column=j + 1)

        elif m.status == gp.GRB.INFEASIBLE:
            result_label = ttk.Label(result_window, text="The model is infeasible.")
            result_label.grid(row=0, column=0, columnspan=2)

        elif m.status == gp.GRB.INF_OR_UNBD:
            result_label = ttk.Label(result_window, text="The model has an infinite or unbounded optimal solution.")
            result_label.grid(row=0, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixInputApp(root)
    root.mainloop()