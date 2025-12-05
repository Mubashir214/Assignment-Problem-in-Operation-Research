from flask import Flask, render_template, request, jsonify
import numpy as np
import json

app = Flask(__name__)

def munkres_algorithm(cost):
    """Hungarian Algorithm implementation for assignment problem"""
    matrix = cost.copy().astype(float)
    n = matrix.shape[0]
    
    # Step 1: Row reduction
    row_reduction = []
    for i in range(n):
        mv = matrix[i].min()
        row_reduction.append(f"Row {i} min = {mv}")
        matrix[i] -= mv
    
    # Step 2: Column reduction
    col_reduction = []
    for j in range(n):
        mv = matrix[:, j].min()
        col_reduction.append(f"Col {j} min = {mv}")
        matrix[:, j] -= mv
    
    # Prepare structures
    starred = np.zeros((n, n), dtype=bool)
    primed = np.zeros((n, n), dtype=bool)
    row_cov = np.zeros(n, dtype=bool)
    col_cov = np.zeros(n, dtype=bool)
    
    # Step: Star initial zeros
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 0 and not row_cov[i] and not col_cov[j]:
                starred[i, j] = True
                row_cov[i] = True
                col_cov[j] = True
    row_cov[:] = False
    col_cov[:] = False
    
    # Cover columns that have a starred zero
    for j in range(n):
        if starred[:, j].any():
            col_cov[j] = True
    
    iteration = 1
    steps = []
    
    while True:
        step_info = {
            'iteration': iteration,
            'matrix': matrix.copy(),
            'starred': starred.copy(),
            'row_cov': row_cov.copy(),
            'col_cov': col_cov.copy()
        }
        
        if col_cov.sum() == n:
            step_info['message'] = "All columns covered — Optimal assignment found!"
            steps.append(step_info)
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
        
        if z is not None:
            i, j = z
            primed[i, j] = True
            step_info['primed'] = (i, j)
            
            star_col = np.where(starred[i])[0]
            
            if star_col.size == 0:
                # Augmenting path found
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
                
                step_info['path'] = path
                
                for r, c in path:
                    starred[r, c] = not starred[r, c]
                
                primed[:, :] = False
                row_cov[:] = False
                col_cov[:] = False
                
                for col in range(n):
                    if starred[:, col].any():
                        col_cov[col] = True
            else:
                sc = int(star_col[0])
                row_cov[i] = True
                col_cov[sc] = False
                step_info['message'] = f"Cover row {i}, uncover column {sc}"
        
        steps.append(step_info)
        
        if z is None:
            # Adjust matrix
            min_uncovered = float('inf')
            for ii in range(n):
                if not row_cov[ii]:
                    for jj in range(n):
                        if not col_cov[jj] and matrix[ii, jj] < min_uncovered:
                            min_uncovered = matrix[ii, jj]
            
            if min_uncovered == float('inf'):
                min_uncovered = 0
            
            adjustment_info = []
            for ii in range(n):
                for jj in range(n):
                    if not row_cov[ii] and not col_cov[jj]:
                        matrix[ii, jj] -= min_uncovered
                        adjustment_info.append(f"Subtract {min_uncovered} at ({ii},{jj})")
                    elif row_cov[ii] and col_cov[jj]:
                        matrix[ii, jj] += min_uncovered
                        adjustment_info.append(f"Add {min_uncovered} at ({ii},{jj})")
            
            steps[-1]['adjustment'] = {
                'min_value': min_uncovered,
                'details': adjustment_info
            }
        
        iteration += 1
    
    # Get final assignment
    assignment = []
    for i in range(n):
        j_idx = np.where(starred[i])[0]
        if j_idx.size > 0:
            assignment.append((i, int(j_idx[0])))
    
    return assignment, steps, row_reduction, col_reduction

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # Get matrix from request
        matrix_data = data['matrix']
        n_rows = len(matrix_data)
        n_cols = len(matrix_data[0]) if n_rows > 0 else 0
        
        # Convert to numpy array
        user_matrix = np.array(matrix_data, dtype=float)
        
        # Balance matrix if not square
        n = max(n_rows, n_cols)
        balanced = np.zeros((n, n))
        balanced[:n_rows, :n_cols] = user_matrix
        
        # Run Hungarian algorithm
        assignment, steps, row_reduction, col_reduction = munkres_algorithm(balanced)
        
        # Calculate total cost
        total_cost = 0
        final_assignment = []
        for r, c in assignment:
            if r < n_rows and c < n_cols:
                cost = user_matrix[r, c]
                total_cost += cost
                final_assignment.append({
                    'driver': r + 1,
                    'route': c + 1,
                    'cost': float(cost)
                })
        
        # Prepare response
        response = {
            'success': True,
            'balanced_matrix': balanced.tolist(),
            'row_reduction': row_reduction,
            'col_reduction': col_reduction,
            'steps': [],
            'assignment': final_assignment,
            'total_cost': float(total_cost)
        }
        
        # Convert numpy arrays to lists for JSON serialization
        for step in steps:
            step_data = {
                'iteration': step['iteration'],
                'matrix': step['matrix'].tolist(),
                'starred': step['starred'].tolist(),
                'row_cov': step['row_cov'].tolist(),
                'col_cov': step['col_cov'].tolist(),
                'message': step.get('message', '')
            }
            
            if 'primed' in step:
                step_data['primed'] = step['primed']
            
            if 'path' in step:
                step_data['path'] = step['path']
            
            if 'adjustment' in step:
                step_data['adjustment'] = step['adjustment']
            
            response['steps'].append(step_data)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/sample')
def sample_data():
    """Return sample data for testing"""
    sample_matrix = [
        [82, 83, 69, 92],
        [77, 37, 49, 92],
        [11, 69, 5, 86],
        [8, 9, 98, 23]
    ]
    
    return jsonify({
        'sample': sample_matrix,
        'description': 'Sample 4x4 Delivery Cost Matrix'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
