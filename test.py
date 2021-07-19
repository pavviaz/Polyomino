from ortools.sat.python import cp_model

cells = {(x, y) for x in range(4) for y in range(4) if x > 1 or y > 0}
sizes = [4, 2, 5, 2, 1]
num_polyominos = len(sizes)
model = cp_model.CpModel()

# Each cell is a member of one polyomino
member = {
    (cell, p): model.NewBoolVar(f"member{cell, p}")
    for cell in cells
    for p in range(num_polyominos)
}
for cell in cells:
    model.Add(sum(member[cell, p] for p in range(num_polyominos)) < 2)

# Each polyomino contains the given number of cells
for p, size in enumerate(sizes):
    model.Add(sum(member[cell, p] for cell in cells) == size)

# Find the border of each polyomino
vertices = {
    v: i
    for i, v in enumerate(
        {(x + i, y + j) for x, y in cells for i in [0, 1] for j in [0, 1]}
    )
}
edges = [
    edge
    for x, y in cells
    for edge in [
        ((x, y), (x + 1, y)),
        ((x + 1, y), (x + 1, y + 1)),
        ((x + 1, y + 1), (x, y + 1)),
        ((x, y + 1), (x, y)),
    ]
]
border = {
    (edge, p): model.NewBoolVar(f"border{edge, p}")
    for edge in edges
    for p in range(num_polyominos)
}
for (((x0, y0), (x1, y1)), p), border_var in border.items():
    left_cell = ((x0 + x1 + y0 - y1) // 2, (y0 + y1 - x0 + x1) // 2)
    right_cell = ((x0 + x1 - y0 + y1) // 2, (y0 + y1 + x0 - x1) // 2)
    left_var = member[left_cell, p]
    model.AddBoolOr([border_var.Not(), left_var])
    if (right_cell, p) in member:
        right_var = member[right_cell, p]
        model.AddBoolOr([border_var.Not(), right_var.Not()])
        model.AddBoolOr([border_var, left_var.Not(), right_var])
    else:
        model.AddBoolOr([border_var, left_var.Not()])

# Each border is a circuit
for p in range(num_polyominos):
    model.AddCircuit(
        [(vertices[v0], vertices[v1], border[(v0, v1), p]) for v0, v1 in edges]
        + [(i, i, model.NewBoolVar(f"vertex_loop{v, p}")) for v, i in vertices.items()]
    )

# Print all solutions
x_range = range(min(x for x, y in cells), max(x for x, y in cells) + 1)
y_range = range(min(y for x, y in cells), max(y for x, y in cells) + 1)
solutions = 0


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
	def OnSolutionCallback(self):
		global solutions
		solutions += 1
		for y in y_range:
			print(
				*(
					next(
						p
						for p in range(num_polyominos)
						if self.Value(member[(x, y), p])
					)
					if (x, y) in cells
					else "-"
					for x in x_range
				)
			)
		print()
		if (solutions >= 1):
			self.StopSearch()

solver = cp_model.CpSolver()
solver.SearchForAllSolutions(model, SolutionPrinter())