import itertools

def branch_and_bound(n, m, b, L):
    def calculate_max_load(assignments):
        load = [0] * (m + 1)
        for paper_reviewers in assignments:
            for reviewer in paper_reviewers:
                load[reviewer] += 1
        return max(load)
    
    def is_valid(assignments):
        for paper_reviewers in assignments:
            if len(paper_reviewers) != b:
                return False
        return True
    
    def recursive_assign(i, current_assignments):
        nonlocal min_max_load, best_assignment
        
        if i > n:
            if is_valid(current_assignments):
                current_load = calculate_max_load(current_assignments)
                if current_load < min_max_load:
                    min_max_load = current_load
                    best_assignment = [list(assignment) for assignment in current_assignments]
            return
        
        for combination in itertools.combinations(L[i], b):
            current_assignments[i - 1] = combination
            recursive_assign(i + 1, current_assignments)
            current_assignments[i - 1] = []
    
    min_max_load = float('inf')
    best_assignment = []
    
    recursive_assign(1, [[] for _ in range(n)])
    
    return best_assignment, min_max_load

n, m, b = map(int, input().split())
L = {}
for i in range(1, n + 1):
    data = list(map(int, input().split()))
    L[i] = data[1:]

assignment, min_load = branch_and_bound(n, m, b, L)

print(n)
for reviewers in assignment:
    print(b, ' '.join(map(str, reviewers)))