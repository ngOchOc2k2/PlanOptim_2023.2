from ortools.linear_solver import pywraplp

def solve_reviewer_assignment_problem(N, M, L, b):
    # Create a solver instance using SCIP
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Define binary decision variables x[i, j]
    x = {}
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    # Define the objective function: Minimize the maximum load z
    z = solver.IntVar(0, solver.infinity(), 'z')
    solver.Minimize(z)

    # Constraints: Each paper must be assigned to exactly 'b' reviewers
    for i in range(1, N + 1):
        solver.Add(solver.Sum(x[i, j] for j in range(1, M + 1) if j in L[i]) == b)

    # Constraints: The load on each reviewer must be less than or equal to z
    for j in range(1, M + 1):
        solver.Add(solver.Sum(x[i, j] for i in range(1, N + 1)) <= z)

    # Solve the ILP problem
    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        return -1, []

    # Get the minimum load from the solution
    min_load = int(z.solution_value())

    # Extract the assignment of reviewers to papers
    assignments = []
    for i in range(1, N + 1):
        reviewers = []
        for j in range(1, M + 1):
            if x[i, j].solution_value() == 1:
                reviewers.append(j)
        assignments.append(reviewers)

    return min_load, assignments



# Read input from standard input or a file
N, M, b = map(int, input().split())
L = {}
for i in range(1, N + 1):
    data = list(map(int, input().split()))
    L[i] = data[1:]

# Solve the reviewer assignment problem and print the result
min_load, assignments = solve_reviewer_assignment_problem(N, M, L, b)

print(N)
for i in range(N):
    print(b, ' '.join(map(str, assignments[i])))
    