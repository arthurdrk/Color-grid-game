# class SolverGeneral(Solver):
#     def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
#         """
#         Runs the general solver to find pairs of cells using the Hungarian algorithm, allowing some cells to remain unpaired.

#         Returns:
#         --------
#         list[tuple[tuple[int, int], tuple[int, int]]]
#             A list of pairs of cells representing the optimal matching.
#         """
#         pairs = self.grid.all_pairs()
#         even_cells = []
#         odd_cells = []
#         for cell1, cell2 in pairs:
#             # Determine even and odd based on sum of coordinates
#             if (cell1[0] + cell1[1]) % 2 == 0:
#                 even, odd = cell1, cell2
#             else:
#                 even, odd = cell2, cell1
#             even_cells.append(even)
#             odd_cells.append(odd)
#         even_cells = list(set(even_cells))
#         odd_cells = list(set(odd_cells))
#         E = len(even_cells)
#         O = len(odd_cells)
#         large_value = np.inf
        
#         # Create mappings from cell to index
#         even_to_index = {cell: i for i, cell in enumerate(even_cells)}
#         odd_to_index = {cell: i for i, cell in enumerate(odd_cells)}
        

#         # Initialize cost matrix with large_value
#         cost_matrix = np.full((E+1, O+1), large_value)
        
#         # Fill real pairs
#         for u, v in pairs:
#             if (u[0] + u[1]) % 2 == 0:
#                 even, odd = u, v
#             else:
#                 even, odd = v, u
#             if even in even_to_index and odd in odd_to_index:
#                 i = even_to_index[even]
#                 j = odd_to_index[odd]
#                 cost = self.grid.cost((u, v)) - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
#                 cost_matrix[i][j] = cost

#         for u in even_cells:
#             cost_matrix[even_to_index[u]][-1] = self.grid.value[u[0]][u[1]]
#         for v in odd_cells:
#             cost_matrix[-1][odd_to_index[v]] = self.grid.value[v[0]][v[1]]
        
#         # Apply Hungarian algorithm
#         row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
#         # Collect matched pairs
#         matched_pairs = []
#         for i, j in zip(row_ind, col_ind):
#             if i < E and j < O:
#                 u = even_cells[i]
#                 v = odd_cells[j]
#                 # Check if the pair (u, v) or (v, u) is allowed
#                 if (u, v) in pairs or (v, u) in pairs:
#                     matched_pairs.append((u, v))
        
#         self.pairs = matched_pairs
#         return matched_pairs
    






# class SolverGeneral(Solver):
#     def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
#         """
#         Runs the general solver using the Hungarian algorithm to find optimal pairs, allowing unpaired cells.
#         """
#         pairs = self.grid.all_pairs()
#         # Include all non-forbidden cells in 'taken'
#         taken = []
#         for i in range(self.grid.n):
#             for j in range(self.grid.m):
#                 if not self.grid.is_forbidden(i, j):
#                     taken.append((i, j))
#         taken=list(set(taken))
#         l = len(taken)
#         if l == 0:
#             self.pairs = []
#             return []
#         cell_to_idx = {cell: idx for idx, cell in enumerate(taken)}
        
#         # Build adjacency list from allowed pairs
#         d = defaultdict(list)
#         for u, v in pairs:
#             d[u].append(v)
#             d[v].append(u)
        
#         # Initialize cost matrix with infinity and set diagonal to 0
#         large_value = np.inf
#         cost_matrix = np.full((l, l), large_value)
#         for i in range(l):
#             u = taken[i]
#             for v in d.get(u, []):
#                 j = cell_to_idx[v]
#                 cost = self.grid.cost((u, v)) - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
#                 cost_matrix[i][j] = cost

#             cost_matrix[i][i] = self.grid.value[u[0]][u[1]] 
#         for i in range(l):
#             for j in range(i-1):
#                 cost_matrix[i][j]=large_value
#         print(cost_matrix)
#         # Apply Hungarian algorithm
#         row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
#         # Collect mutual pairs
#         matched_pairs = []
#         seen = set()
#         for i, j in zip(row_ind, col_ind):
#             if i in seen or j in seen:
#                 continue
#             if i == j:
#                 seen.add(i)  # Unpaired
#             else:
#                 if col_ind[j] == i:  # Check mutual assignment
#                     u, v = taken[i], taken[j]
#                     if (u, v) in pairs or (v, u) in pairs:
#                         matched_pairs.append((u, v))
#                         seen.update([i, j])
        
#         self.pairs = matched_pairs
#         return matched_pairs
    

# class SolverGeneral(Solver):
#     """
#     Un solveur qui utilise l'algorithme hongrois pour trouver un appariement optimal.
#     """

#     def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
#         """
#         Exécute l'algorithme hongrois pour trouver les paires optimales.
#         """
#         pairs = self.grid.all_pairs()
#         even_cells = []
#         odd_cells = []

#         # Séparer les cellules paires et impaires
#         for cell1, cell2 in pairs:
#             if (cell1[0] + cell1[1]) % 2 == 0:
#                 even, odd = cell1, cell2
#             else:
#                 even, odd = cell2, cell1
#             even_cells.append(even)
#             odd_cells.append(odd)
#         even_cells = list(set(even_cells))
#         odd_cells = list(set(odd_cells))
#         E = len(even_cells)
#         O = len(odd_cells)
#         large_value = np.inf

#         # Créer des mappings pour les indices
#         even_to_idx = {cell: i for i, cell in enumerate(even_cells)}
#         odd_to_idx = {cell: i for i, cell in enumerate(odd_cells)}

#         # Initialiser la matrice de coût
#         cost_matrix = np.full((E + O, E + O), large_value)

#         # Remplir les coûts pour les paires valides
#         for u, v in pairs:
#             if (u[0] + u[1]) % 2 == 0:
#                 even, odd = u, v
#             else:
#                 even, odd = v, u
#             if even in even_to_idx and odd in odd_to_idx:
#                 i = even_to_idx[even]
#                 j = odd_to_idx[odd]
#                 cost = self.grid.cost((u, v)) - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
#                 cost_matrix[i][j] = cost

#         # Coût pour laisser une cellule non appariée
#         for i, cell in enumerate(even_cells):
#             cost_matrix[i][O + i] = self.grid.value[cell[0]][cell[1]]
#         for j, cell in enumerate(odd_cells):
#             cost_matrix[E + j][j] = self.grid.value[cell[0]][cell[1]]
#         print(cost_matrix)
#         # Appliquer l'algorithme hongrois
#         row_ind, col_ind = linear_sum_assignment(cost_matrix)

#         # Extraire les paires
#         matched_pairs = []
#         for i, j in zip(row_ind, col_ind):
#             if i < E and j < O:
#                 u = even_cells[i]
#                 v = odd_cells[j]
#                 if ((u, v) in pairs) or ((v, u) in pairs):
#                     matched_pairs.append((u, v))

#         self.pairs = matched_pairs
#         return matched_pairs
    
