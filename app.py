import numpy as np

def get_user_input():
    """Get matrix input from user via terminal"""
    print("=" * 60)
    print("HUNGARIAN ALGORITHM - OPTIMAL DELIVERY ASSIGNMENT")
    print("=" * 60)
    
    try:
        rows = int(input("\nEnter number of Delivery Drivers: "))
        cols = int(input("Enter number of Delivery Routes: "))
        
        print(f"\nEnter delivery cost matrix row by row ({rows} x {cols}):")
        print("(Enter costs separated by space)")
        print("-" * 40)
        
        user_matrix = []
        for i in range(rows):
            while True:
                try:
                    row_input = input(f"Driver {i+1} costs: ").strip()
                    row = list(map(float, row_input.split()))
                    
                    if len(row) != cols:
                        print(f"Error: Expected {cols} costs, got {len(row)}. Please enter again.")
                        continue
                    
                    if any(cost < 0 for cost in row):
                        print("Error: Costs cannot be negative. Please enter again.")
                        continue
                    
                    user_matrix.append(row)
                    break
                except ValueError:
                    print("Error: Please enter valid numbers separated by spaces.")
        
        return np.array(user_matrix), rows, cols
        
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()

def munkres_verbose(cost, original_rows, original_cols):
    """Hungarian Algorithm implementation with detailed output"""
    matrix = cost.copy().astype(float)
    n = matrix.shape[0]

    print("\n" + "="*60)
    print("STEP 1: INITIAL DELIVERY COST MATRIX")
    print("="*60)
    print_matrix(matrix, original_rows, original_cols)

    # Step 1: Row reduction
    print("\n" + "="*60)
    print("STEP 2: ROW REDUCTION")
    print("="*60)
    print("Subtract minimum value from each row:")
    row_mins = []
    for i in range(n):
        mv = matrix[i].min()
        row_mins.append(mv)
        print(f"  Row {i+1} min = {mv}")
        matrix[i] -= mv
    
    print("\nMatrix after row reduction:")
    print_matrix(matrix, original_rows, original_cols)

    # Step 2: Column reduction
    print("\n" + "="*60)
    print("STEP 3: COLUMN REDUCTION")
    print("="*60)
    print("Subtract minimum value from each column:")
    col_mins = []
    for j in range(n):
        mv = matrix[:, j].min()
        col_mins.append(mv)
        print(f"  Column {j+1} min = {mv}")
        matrix[:, j] -= mv
    
    print("\nMatrix after column reduction:")
    print_matrix(matrix, original_rows, original_cols)

    # Prepare structures
    starred = np.zeros((n, n), dtype=bool)
    primed = np.zeros((n, n), dtype=bool)
    row_cov = np.zeros(n, dtype=bool)
    col_cov = np.zeros(n, dtype=bool)

    # Step: Star initial zeros
    print("\n" + "="*60)
    print("STEP 4: INITIAL ZERO ASSIGNMENT (STARRING)")
    print("="*60)
    print("Star independent zeros (one per row and column):")
    
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 0 and not row_cov[i] and not col_cov[j]:
                starred[i, j] = True
                row_cov[i] = True
                col_cov[j] = True
                print(f"  Starred zero at (Driver {i+1}, Route {j+1})")
    
    row_cov[:] = False
    col_cov[:] = False

    print("\nInitial starred zeros matrix:")
    print_starred_matrix(starred, original_rows, original_cols)

    # Cover columns that have a starred zero
    for j in range(n):
        if starred[:, j].any():
            col_cov[j] = True
    
    print("\nCovered columns (with starred zeros):", 
          [f"Route {j+1}" for j in range(n) if col_cov[j]])

    iteration = 1
    while True:
        print(f"\n" + "="*60)
        print(f"ITERATION {iteration}")
        print("="*60)

        if col_cov.sum() == n:
            print("✓ All columns covered — Optimal assignment found!")
            break

        # Find uncovered zero
        z = None
        for i in range(n):
            if not row_cov[i]:
                for j in range(n):
                    if not col_cov[j] and matrix[i, j] == 0:
                        z = (i, j)
                        break
            if z:
                break

        while z is not None:
            i, j = z
            primed[i, j] = True
            print(f"  Primed zero at (Driver {i+1}, Route {j+1})")

            star_col = np.where(starred[i])[0]

            if star_col.size == 0:
                # Augmenting path found
                print(f"  No starred zero in row {i+1} → Found augmenting path")
                path = [(i, j)]
                
                while True:
                    starred_row = np.where(starred[:, path[-1][1]])[0]
                    if starred_row.size == 0:
                        break
                    starred_row = int(starred_row[0])
                    path.append((starred_row, path[-1][1]))

                    prime_col = np.where(primed[path[-1][0]])[0]
                    prime_col = int(prime_col[0])
                    path.append((path[-1][0], prime_col))

                print("  Augmenting path:", 
                      " → ".join([f"(D{r+1},R{c+1})" for r, c in path]))

                # Toggle stars along path
                for r, c in path:
                    starred[r, c] = not starred[r, c]

                primed[:, :] = False
                row_cov[:] = False
                col_cov[:] = False

                # Update column covers
                for col in range(n):
                    if starred[:, col].any():
                        col_cov[col] = True

                print("  Updated starred zeros:")
                print_starred_matrix(starred, original_rows, original_cols)
                break

            else:
                sc = int(star_col[0])
                print(f"  Found starred zero at (Driver {i+1}, Route {sc+1})")
                print(f"  → Cover row {i+1}, uncover column {sc+1}")
                row_cov[i] = True
                col_cov[sc] = False
                
                # Find next uncovered zero
                z = None
                for ii in range(n):
                    if not row_cov[ii]:
                        for jj in range(n):
                            if not col_cov[jj] and matrix[ii, jj] == 0:
                                z = (ii, jj)
                                break
                    if z:
                        break

        if z is None:
            # Adjust matrix
            print("  No uncovered zeros found → Adjusting matrix")
            
            min_uncovered = float('inf')
            for ii in range(n):
                if not row_cov[ii]:
                    for jj in range(n):
                        if not col_cov[jj] and matrix[ii, jj] < min_uncovered:
                            min_uncovered = matrix[ii, jj]

            if min_uncovered == float('inf'):
                min_uncovered = 0

            print(f"  Minimum uncovered value: {min_uncovered}")
            print("  Adjusting matrix:")
            print(f"    - Subtract {min_uncovered} from uncovered cells")
            print(f"    - Add {min_uncovered} to twice-covered cells")

            for ii in range(n):
                for jj in range(n):
                    if not row_cov[ii] and not col_cov[jj]:
                        matrix[ii, jj] -= min_uncovered
                    elif row_cov[ii] and col_cov[jj]:
                        matrix[ii, jj] += min_uncovered

            print("\n  Matrix after adjustment:")
            print_matrix(matrix, original_rows, original_cols)
            
            # Reset covers for next iteration
            row_cov[:] = False
            for j in range(n):
                col_cov[j] = starred[:, j].any()

        iteration += 1

    # Get final assignment
    assignment = []
    for i in range(n):
        j_idx = np.where(starred[i])[0]
        if j_idx.size > 0:
            j = int(j_idx[0])
            if i < original_rows and j < original_cols:
                assignment.append((i, j))

    return assignment

def print_matrix(matrix, rows, cols, title=None):
    """Print matrix with formatting"""
    if title:
        print(title)
    
    n = matrix.shape[0]
    for i in range(n):
        row_str = ""
        for j in range(n):
            if i < rows and j < cols:
                value = matrix[i, j]
                if value == 0:
                    row_str += f" [{value:5.1f}]"
                else:
                    row_str += f"  {value:5.1f} "
            else:
                row_str += "      "
        print(row_str)

def print_starred_matrix(starred, rows, cols):
    """Print matrix showing starred zeros"""
    n = starred.shape[0]
    for i in range(n):
        row_str = ""
        for j in range(n):
            if i < rows and j < cols:
                if starred[i, j]:
                    row_str += "  [★]  "
                else:
                    row_str += "   .   "
            else:
                row_str += "       "
        print(row_str)

def main():
    """Main function"""
    print("\n" + "★" * 60)
    print("WELCOME TO HUNGARIAN ALGORITHM SOLVER")
    print("Optimal Delivery Driver-Route Assignment System")
    print("★" * 60)
    
    # Get user input
    user_matrix, original_rows, original_cols = get_user_input()
    
    print("\n" + "="*60)
    print("PROCESSING OPTIMAL ASSIGNMENT...")
    print("="*60)
    
    # Balance matrix if needed
    n = max(original_rows, original_cols)
    if original_rows != original_cols:
        print(f"\nNote: Matrix is {original_rows}x{original_cols}")
        print(f"Balancing to {n}x{n} by adding dummy rows/columns with zero cost")
    
    balanced = np.zeros((n, n))
    balanced[:original_rows, :original_cols] = user_matrix
    
    print(f"\nBalanced {n}x{n} matrix:")
    print_matrix(balanced, original_rows, original_cols)
    
    # Run Hungarian algorithm
    assignment = munkres_verbose(balanced, original_rows, original_cols)
    
    # Display final results
    print("\n" + "="*60)
    print("FINAL OPTIMAL ASSIGNMENT")
    print("="*60)
    
    total_cost = 0
    for r, c in assignment:
        cost = user_matrix[r, c]
        total_cost += cost
        print(f"✓ Driver {r+1} → Route {c+1}  | Cost = Rs. {cost:.2f}")
    
    print("\n" + "-"*40)
    print(f"TOTAL MINIMUM DELIVERY COST = Rs. {total_cost:.2f}")
    print("="*60)
    
    # Ask if user wants to run again
    while True:
        try:
            again = input("\nRun another assignment? (y/n): ").strip().lower()
            if again in ['y', 'yes']:
                print("\n" + "="*60)
                main()
                break
            elif again in ['n', 'no']:
                print("\nThank you for using Hungarian Algorithm Solver!")
                print("Goodbye!")
                break
        except KeyboardInterrupt:
            print("\n\nProgram terminated.")
            exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\nError: {e}")
