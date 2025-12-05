<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hungarian Algorithm - Delivery Assignment</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .card-header {
            background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            padding: 15px 20px;
            font-weight: 600;
        }
        .matrix-input {
            width: 80px;
            text-align: center;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 8px;
            font-weight: 500;
            transition: all 0.3s;
        }
        .matrix-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            outline: none;
        }
        .btn-custom {
            background: linear-gradient(to right, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-custom:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            color: white;
        }
        .step-box {
            background: white;
            border-left: 5px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }
        .assignment-item {
            background: linear-gradient(to right, #d4fc79, #96e6a1);
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 8px;
            font-weight: 600;
        }
        .highlight {
            background-color: #fff3cd !important;
            font-weight: bold;
        }
        .starred-cell {
            background-color: #c3e6cb !important;
            color: #155724;
            font-weight: bold;
            position: relative;
        }
        .starred-cell::after {
            content: "★";
            position: absolute;
            top: 2px;
            right: 2px;
            font-size: 12px;
        }
        .primed-cell {
            background-color: #ffeeba !important;
            color: #856404;
            font-weight: bold;
        }
        .covered-row {
            background-color: #f8d7da !important;
            opacity: 0.8;
        }
        .covered-col {
            background-color: #d1ecf1 !important;
            opacity: 0.8;
        }
        .result-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border: 2px solid #667eea;
        }
        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }
        .spinner-custom {
            width: 3rem;
            height: 3rem;
            border-width: 3px;
        }
        .matrix-table {
            width: auto;
            margin: 0 auto;
            border-collapse: separate;
            border-spacing: 5px;
        }
        .matrix-table th {
            background-color: #f1f3f5;
            padding: 10px 15px;
            text-align: center;
            font-weight: 600;
        }
        .matrix-table td {
            padding: 12px;
            text-align: center;
            min-width: 80px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            background-color: white;
            transition: all 0.3s;
        }
        .cost-badge {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="display-5 mb-3">🚚 Hungarian Algorithm Solver</h1>
                    <p class="lead mb-0">Optimal Delivery Driver → Route Assignment System</p>
                    <p class="mb-0">Minimize total delivery cost using the Hungarian Algorithm</p>
                </div>
                <div class="col-md-4 text-end">
                    <div class="bg-white rounded-pill d-inline-block p-2">
                        <span class="text-primary fw-bold">Total Cost Minimization</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">
            <!-- Input Section -->
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">📝 Input Delivery Cost Matrix</h5>
                    </div>
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <label class="form-label fw-bold">Number of Delivery Drivers</label>
                                <input type="number" id="rows" class="form-control" min="1" max="10" value="4">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold">Number of Delivery Routes</label>
                                <input type="number" id="cols" class="form-control" min="1" max="10" value="4">
                            </div>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">Enter Delivery Costs (Rs.)</label>
                            <p class="text-muted small mb-2">Enter cost for each Driver → Route combination</p>
                            <div id="matrix-container" class="table-responsive"></div>
                        </div>
                        
                        <div class="d-flex flex-wrap gap-2 mb-3">
                            <button class="btn btn-custom" onclick="updateMatrix()">
                                <i class="fas fa-sync-alt me-2"></i>Create Matrix
                            </button>
                            <button class="btn btn-success" onclick="loadSample()">
                                <i class="fas fa-vial me-2"></i>Load Sample
                            </button>
                            <button class="btn btn-outline-danger" onclick="clearMatrix()">
                                <i class="fas fa-eraser me-2"></i>Clear All
                            </button>
                        </div>
                        
                        <div class="d-grid">
                            <button class="btn btn-custom btn-lg" onclick="calculate()">
                                <i class="fas fa-calculator me-2"></i>Calculate Optimal Assignment
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Sample Data Cards -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h6 class="mb-0">📊 Sample Data</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100 mb-2" onclick="loadSample1()">Sample 1</button>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100 mb-2" onclick="loadSample2()">Sample 2</button>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100 mb-2" onclick="loadSample3()">Sample 3</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Results Section -->
            <div class="col-lg-6">
                <div class="card result-card">
                    <div class="card-header">
                        <h5 class="mb-0">📈 Results & Assignment</h5>
                    </div>
                    <div class="card-body">
                        <!-- Loading Indicator -->
                        <div id="loading" class="loading" style="display: none;">
                            <div class="spinner-border spinner-custom text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-3 fw-bold">Calculating optimal assignment...</p>
                            <p class="text-muted small">Running Hungarian Algorithm step by step</p>
                        </div>
                        
                        <!-- Results Container -->
                        <div id="results" style="display: none;"></div>
                        
                        <!-- Error Message -->
                        <div id="error" class="alert alert-danger" style="display: none;"></div>
                        
                        <!-- Initial Placeholder -->
                        <div id="initial-placeholder">
                            <div class="text-center text-muted py-5">
                                <i class="fas fa-chart-line fa-3x mb-3" style="color: #ccc;"></i>
                                <h5>Results will appear here</h5>
                                <p class="mb-0">Enter your delivery cost matrix and click "Calculate"</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Steps Section -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h5 class="mb-0">🔍 Algorithm Steps</h5>
                    </div>
                    <div class="card-body">
                        <div id="steps-container">
                            <p class="text-muted text-center py-3">
                                Step-by-step solution will appear here after calculation
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center mt-5 mb-4">
            <p class="text-muted">
                Hungarian Algorithm Implementation | Delivery Optimization System
            </p>
        </div>
    </div>

    <!-- Font Awesome for Icons -->
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Initialize matrix on page load
        document.addEventListener('DOMContentLoaded', function() {
            updateMatrix();
        });

        function updateMatrix() {
            const rows = parseInt(document.getElementById('rows').value);
            const cols = parseInt(document.getElementById('cols').value);
            const container = document.getElementById('matrix-container');
            
            if (rows > 10 || cols > 10) {
                alert('Maximum size is 10x10 for better performance.');
                return;
            }
            
            let html = '<table class="matrix-table"><thead><tr><th></th>';
            
            // Column headers
            for (let j = 0; j < cols; j++) {
                html += `<th>Route ${j+1}</th>`;
            }
            html += '</tr></thead><tbody>';
            
            // Rows with inputs
            for (let i = 0; i < rows; i++) {
                html += `<tr><th class="bg-light">Driver ${i+1}</th>`;
                for (let j = 0; j < cols; j++) {
                    html += `<td>
                        <input type="number" class="matrix-input" 
                               id="cell-${i}-${j}" value="${Math.floor(Math.random() * 100) + 1}" 
                               min="0" step="0.01" placeholder="0.00">
                    </td>`;
                }
                html += '</tr>';
            }
            html += '</tbody></table>';
            
            container.innerHTML = html;
        }

        function clearMatrix() {
            const inputs = document.querySelectorAll('.matrix-input');
            inputs.forEach(input => {
                input.value = '';
            });
        }

        function loadSample1() {
            fetch('/api/sample')
                .then(response => response.json())
                .then(data => {
                    loadMatrixData(data.sample);
                });
        }

        function loadSample2() {
            fetch('/api/sample2')
                .then(response => response.json())
                .then(data => {
                    loadMatrixData(data.sample);
                });
        }

        function loadSample3() {
            fetch('/api/sample3')
                .then(response => response.json())
                .then(data => {
                    loadMatrixData(data.sample);
                });
        }

        function loadSample() {
            loadSample1(); // Default to sample 1
        }

        function loadMatrixData(sample) {
            const rows = sample.length;
            const cols = sample[0].length;
            
            document.getElementById('rows').value = rows;
            document.getElementById('cols').value = cols;
            updateMatrix();
            
            // Set sample values
            setTimeout(() => {
                for (let i = 0; i < rows; i++) {
                    for (let j = 0; j < cols; j++) {
                        const input = document.getElementById(`cell-${i}-${j}`);
                        if (input) {
                            input.value = sample[i][j];
                        }
                    }
                }
            }, 100);
        }

        function getMatrix() {
            const rows = parseInt(document.getElementById('rows').value);
            const cols = parseInt(document.getElementById('cols').value);
            const matrix = [];
            
            for (let i = 0; i < rows; i++) {
                const row = [];
                for (let j = 0; j < cols; j++) {
                    const input = document.getElementById(`cell-${i}-${j}`);
                    const value = parseFloat(input.value) || 0;
                    row.push(value);
                }
                matrix.push(row);
            }
            
            return matrix;
        }

        function calculate() {
            const matrix = getMatrix();
            
            // Validate matrix
            if (matrix.length === 0 || matrix[0].length === 0) {
                showError('Please enter a valid matrix');
                return;
            }
            
            // Show loading, hide other sections
            document.getElementById('loading').style.display = 'flex';
            document.getElementById('results').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('initial-placeholder').style.display = 'none';
            document.getElementById('steps-container').innerHTML = '<p class="text-muted text-center py-3">Calculating steps...</p>';
            
            // Send to server
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ matrix: matrix })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    displayResults(data);
                    displaySteps(data);
                } else {
                    showError(data.error);
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                showError('Network error: ' + error.message);
            });
        }

        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            
            // Show placeholder again
            document.getElementById('initial-placeholder').style.display = 'block';
        }

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            let html = '';
            
            // Show balanced matrix if it was balanced
            if (data.original_rows !== data.balanced_size || data.original_cols !== data.balanced_size) {
                html += `<div class="alert alert-info">
                    <strong>Note:</strong> Matrix balanced from ${data.original_rows}×${data.original_cols} to ${data.balanced_size}×${data.balanced_size}
                </div>`;
            }
            
            // Show reduction steps summary
            html += `<h5>Reduction Steps:</h5>`;
            html += `<div class="row mb-3">`;
            html += `<div class="col-md-6">`;
            html += `<h6>Row Reduction:</h6>`;
            data.row_reduction.forEach(step => {
                html += `<div class="step-box"><small>${step}</small></div>`;
            });
            html += `</div>`;
            html += `<div class="col-md-6">`;
            html += `<h6>Column Reduction:</h6>`;
            data.col_reduction.forEach(step => {
                html += `<div class="step-box"><small>${step}</small></div>`;
            });
            html += `</div>`;
            html += `</div>`;
            
            // Show final assignment
            html += `<div class="mt-4 p-3 bg-light rounded">`;
            html += `<h5 class="mb-3"><i class="fas fa-check-circle text-success me-2"></i>Optimal Assignment:</h5>`;
            
            if (data.assignment.length === 0) {
                html += `<p class="text-danger">No valid assignment found!</p>`;
            } else {
                data.assignment.forEach(assign => {
                    html += `<div class="assignment-item d-flex justify-content-between align-items-center">
                        <div>
                            <i class="fas fa-user-tie me-2"></i>Driver ${assign.driver} 
                            <i class="fas fa-arrow-right mx-3"></i>
                            <i class="fas fa-route me-2"></i>Route ${assign.route}
                        </div>
                        <span class="cost-badge">Rs. ${assign.cost.toFixed(2)}</span>
                    </div>`;
                });
                
                html += `<div class="mt-4 text-center">
                    <h4 class="text-primary">
                        Total Minimum Delivery Cost: 
                        <span class="cost-badge px-4 py-2">Rs. ${data.total_cost.toFixed(2)}</span>
                    </h4>
                </div>`;
            }
            html += `</div>`;
            
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
        }

        function displaySteps(data) {
            const container = document.getElementById('steps-container');
            
            if (data.steps.length === 0) {
                container.innerHTML = '<p class="text-muted text-center py-3">No steps to display</p>';
                return;
            }
            
            let html = '';
            
            // Create tabs for each step
            html += `<ul class="nav nav-pills mb-3" id="stepTabs" role="tablist">`;
            data.steps.forEach((step, index) => {
                const active = index === 0 ? 'active' : '';
                html += `<li class="nav-item" role="presentation">
                    <button class="nav-link ${active}" id="step-${step.iteration}-tab" data-bs-toggle="pill" 
                            data-bs-target="#step-${step.iteration}" type="button" role="tab">
                        Step ${step.iteration}
                    </button>
                </li>`;
            });
            html += `</ul>`;
            
            html += `<div class="tab-content" id="stepTabsContent">`;
            
            data.steps.forEach((step, index) => {
                const active = index === 0 ? 'show active' : '';
                html += `<div class="tab-pane fade ${active}" id="step-${step.iteration}" role="tabpanel">`;
                html += `<div class="step-box">`;
                
                if (step.message) {
                    html += `<div class="alert alert-success mb-3">${step.message}</div>`;
                }
                
                // Display matrix
                html += `<h6>Matrix:</h6>`;
                html += `<div class="table-responsive">`;
                html += `<table class="table table-bordered matrix-table">`;
                
                for (let i = 0; i < step.matrix.length; i++) {
                    html += '<tr>';
                    for (let j = 0; j < step.matrix[i].length; j++) {
                        let cellClass = '';
                        let cellContent = step.matrix[i][j].toFixed(2);
                        
                        if (step.starred[i][j]) cellClass = 'starred-cell';
                        if (step.row_cov[i]) cellClass += ' covered-row';
                        if (step.col_cov[j]) cellClass += ' covered-col';
                        
                        if (step.primed && step.primed[0] === i && step.primed[1] === j) {
                            cellClass = 'primed-cell';
                            cellContent = '0.00*';
                        }
                        
                        html += `<td class="${cellClass}">${cellContent}</td>`;
                    }
                    html += '</tr>';
                }
                html += `</table>`;
                html += `</div>`;
                
                if (step.path_labels && step.path_labels.length > 0) {
                    html += `<p class="mt-2"><strong>Augmenting Path:</strong> ${step.path_labels.join(' → ')}</p>`;
                }
                
                if (step.adjustment) {
                    html += `<div class="alert alert-warning mt-3">
                        <strong>Matrix Adjustment:</strong> Minimum uncovered value = ${step.adjustment.min_value}
                    </div>`;
                }
                
                html += `</div></div>`;
            });
            
            html += `</div>`;
            
            container.innerHTML = html;
        }
    </script>
</body>
</html>
