import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Delivery Route Optimizer",
    page_icon="🚚",
    layout="wide"
)

def munkres_verbose(cost, verbose=True, log_func=print):
    """Munkres (Hungarian) algorithm with detailed logging"""
    matrix = cost.copy().astype(float)
    n = matrix.shape[0]
    
    logs = []
    
    def log(msg):
        logs.append(msg)
        if verbose:
            log_func(msg)
    
    log("\n===== INITIAL MATRIX (DELIVERY COST MATRIX) =====")
    log(f"\n{matrix}")
    
    # Step 1: Row reduction
    log("\n===== ROW REDUCTION =====")
    for i in range(n):
        mv = matrix[i].min()
        log(f"Row {i} min = {mv}")
        matrix[i] -= mv
    log("\nMatrix after row reduction:")
    log(f"\n{matrix}")
    
    # Step 2: Column reduction
    log("\n===== COLUMN REDUCTION =====")
    for j in range(n):
        mv = matrix[:, j].min()
        log(f"Col {j} min = {mv}")
        matrix[:, j] -= mv
    log("\nMatrix after column reduction:")
    log(f"\n{matrix}")
    
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
    
    log("\nInitial starred zeros (1 = starred):")
    log(f"\n{starred.astype(int)}")
    
    # Cover columns that have a starred zero
    for j in range(n):
        if starred[:, j].any():
            col_cov[j] = True
    log(f"Initially covered columns: {np.where(col_cov)[0].tolist()}")
    
    iteration = 1
    while True:
        log(f"\n===== ITERATION {iteration} =====")
        
        if col_cov.sum() == n:
            log("All columns covered — Optimal Driver → Route assignment found.")
            break
        
        def find_uncovered_zero():
            for i in range(n):
                if not row_cov[i]:
                    for j in range(n):
                        if not col_cov[j] and matrix[i, j] == 0:
                            return (i, j)
            return None
        
        z = find_uncovered_zero()
        
        while z is not None:
            i, j = z
            primed[i, j] = True
            log(f"Primed zero at ({i},{j})")
            
            star_col = np.where(starred[i])[0]
            
            if star_col.size == 0:
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
                
                log(f"Augmenting path: {path}")
                
                for r, c in path:
                    starred[r, c] = not starred[r, c]
                
                primed[:, :] = False
                row_cov[:] = False
                col_cov[:] = False
                
                for col in range(n):
                    if starred[:, col].any():
                        col_cov[col] = True
                
                log("Starred matrix now:")
                log(f"\n{starred.astype(int)}")
                break
            
            else:
                sc = int(star_col[0])
                row_cov[i] = True
                col_cov[sc] = False
                log(f"Row {i} covered; Column {sc} uncovered")
                z = find_uncovered_zero()
        
        if find_uncovered_zero() is None:
            min_uncovered = float('inf')
            for ii in range(n):
                if not row_cov[ii]:
                    for jj in range(n):
                        if not col_cov[jj] and matrix[ii, jj] < min_uncovered:
                            min_uncovered = matrix[ii, jj]
            
            if min_uncovered == float('inf'):
                min_uncovered = 0
            
            log(f"Minimum uncovered value: {min_uncovered}")
            
            for ii in range(n):
                for jj in range(n):
                    if not row_cov[ii] and not col_cov[jj]:
                        matrix[ii, jj] -= min_uncovered
                    elif row_cov[ii] and col_cov[jj]:
                        matrix[ii, jj] += min_uncovered
            
            log("Matrix after adjustment:")
            log(f"\n{matrix}")
        
        iteration += 1
    
    assignment = []
    for i in range(n):
        j_idx = np.where(starred[i])[0]
        if j_idx.size > 0:
            assignment.append((i, int(j_idx[0])))
    
    return assignment, logs

def main():
    st.title("🚚 Delivery Route Optimizer")
    st.markdown("""
    This app uses the **Munkres (Hungarian) Algorithm** to find the optimal assignment of 
    delivery drivers to routes, minimizing total delivery cost.
    """)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📊 Input Parameters")
        
        st.subheader("Method 1: Manual Matrix Input")
        rows = st.number_input("Number of Delivery Drivers", min_value=1, max_value=10, value=3, step=1)
        cols = st.number_input("Number of Delivery Routes", min_value=1, max_value=10, value=3, step=1)
        
        st.markdown("---")
        st.subheader("Method 2: Example Matrices")
        example_choice = st.selectbox(
            "Choose an example matrix",
            ["Select an example", "Small (3x3)", "Medium (4x4)", "Large (5x5)", "Unbalanced (3x4)"]
        )
        
        st.markdown("---")
        st.subheader("Algorithm Settings")
        show_steps = st.checkbox("Show Detailed Steps", value=True)
    
    # Initialize session state for matrix
    if 'cost_matrix' not in st.session_state:
        st.session_state.cost_matrix = np.zeros((rows, cols))
    
    # Example matrices
    example_matrices = {
        "Small (3x3)": np.array([
            [250, 400, 350],
            [400, 600, 350],
            [200, 400, 250]
        ]),
        "Medium (4x4)": np.array([
            [82, 83, 69, 92],
            [77, 37, 49, 92],
            [11, 69, 5, 86],
            [8, 9, 98, 23]
        ]),
        "Large (5x5)": np.array([
            [10, 5, 13, 15, 16],
            [3, 9, 18, 13, 6],
            [10, 7, 2, 2, 2],
            [7, 11, 9, 7, 12],
            [7, 9, 10, 4, 12]
        ]),
        "Unbalanced (3x4)": np.array([
            [250, 400, 350, 300],
            [400, 600, 350, 200],
            [200, 400, 250, 500]
        ])
    }
    
    # Matrix input
    st.header("📝 Delivery Cost Matrix")
    
    # Handle example selection
    if example_choice != "Select an example":
        example_matrix = example_matrices[example_choice]
        rows, cols = example_matrix.shape
        st.session_state.cost_matrix = example_matrix
        st.info(f"Loaded {example_choice} example matrix")
    
    # Create editable matrix
    st.write("Enter delivery costs (in Rupees):")
    
    # Create input grid
    input_data = []
    for i in range(rows):
        cols_list = []
        cols_container = st.columns(cols)
        for j in range(cols):
            with cols_container[j]:
                if example_choice != "Select an example" and i < example_matrix.shape[0] and j < example_matrix.shape[1]:
                    default_val = float(example_matrix[i, j])
                else:
                    default_val = float(st.session_state.cost_matrix[i, j]) if i < st.session_state.cost_matrix.shape[0] and j < st.session_state.cost_matrix.shape[1] else 0.0
                
                val = cols_container[j].number_input(
                    f"D{i+1}R{j+1}",
                    min_value=0.0,
                    max_value=10000.0,
                    value=default_val,
                    step=50.0,
                    key=f"cell_{i}_{j}"
                )
                cols_list.append(val)
        input_data.append(cols_list)
    
    # Update session state
    st.session_state.cost_matrix = np.array(input_data)
    
    # Display the matrix
    st.subheader("Current Delivery Cost Matrix")
    df = pd.DataFrame(
        st.session_state.cost_matrix,
        index=[f"Driver {i+1}" for i in range(rows)],
        columns=[f"Route {j+1}" for j in range(cols)]
    )
    st.dataframe(df.style.format("{:.2f}"), use_container_width=True)
    
    # Add a visual representation
    st.subheader("Visual Representation")
    fig_data = pd.DataFrame(
        st.session_state.cost_matrix,
        index=[f"D{i+1}" for i in range(rows)],
        columns=[f"R{j+1}" for j in range(cols)]
    )
    st.bar_chart(fig_data.T if rows >= cols else fig_data)
    
    # Run algorithm button
    if st.button("🚀 Find Optimal Assignment", type="primary", use_container_width=True):
        st.markdown("---")
        
        # Balance the matrix if needed
        original_rows, original_cols = st.session_state.cost_matrix.shape
        n = max(original_rows, original_cols)
        
        if original_rows != original_cols:
            st.info(f"⚠️ Matrix is unbalanced ({original_rows}x{original_cols}). Adding dummy {'drivers' if original_rows < original_cols else 'routes'} with zero cost.")
        
        balanced_matrix = np.zeros((n, n))
        balanced_matrix[:original_rows, :original_cols] = st.session_state.cost_matrix
        
        st.subheader("🧮 Algorithm Execution")
        
        # Create tabs for output
        tab1, tab2, tab3 = st.tabs(["📊 Results", "🔍 Detailed Steps", "📈 Visualization"])
        
        with tab1:
            # Run the algorithm
            assignment, logs = munkres_verbose(balanced_matrix, verbose=False)
            
            # Display results
            st.success("✅ Optimal Assignment Found!")
            
            # Calculate total cost
            total_cost = 0
            results = []
            
            for r, c in assignment:
                if r < original_rows and c < original_cols:
                    cost = st.session_state.cost_matrix[r, c]
                    total_cost += cost
                    results.append({
                        "Driver": f"D{r+1}",
                        "Route": f"R{c+1}",
                        "Cost (Rs.)": f"{cost:.2f}"
                    })
            
            # Display assignment as a table
            results_df = pd.DataFrame(results)
            st.table(results_df)
            
            # Display total cost
            st.metric("💰 Total Minimum Delivery Cost", f"Rs. {total_cost:.2f}")
            
            # Show assignment matrix
            st.subheader("Assignment Matrix")
            assign_matrix = np.zeros((original_rows, original_cols))
            for r, c in assignment:
                if r < original_rows and c < original_cols:
                    assign_matrix[r, c] = 1
            
            assign_df = pd.DataFrame(
                assign_matrix,
                index=[f"Driver {i+1}" for i in range(original_rows)],
                columns=[f"Route {j+1}" for j in range(original_cols)]
            )
            st.dataframe(assign_df.style.format("{:.0f}"), use_container_width=True)
        
        with tab2:
            if show_steps:
                # Display the algorithm steps
                st.subheader("Algorithm Steps")
                
                # Create an expandable container for each major step
                current_section = ""
                section_content = []
                
                for log_entry in logs:
                    if "=====" in log_entry:
                        # Save previous section
                        if current_section and section_content:
                            with st.expander(current_section, expanded=True):
                                for content in section_content:
                                    if content.strip():
                                        if "Matrix after" in content or "Starred matrix" in content or content.strip().startswith("[[") or content.strip().startswith("["):
                                            # Try to parse as numpy array
                                            try:
                                                lines = content.strip().split('\n')
                                                if len(lines) > 1:
                                                    for line in lines:
                                                        if line.strip():
                                                            st.code(line)
                                                else:
                                                    st.code(content)
                                            except:
                                                st.text(content)
                                        else:
                                            st.text(content)
                        
                        # Start new section
                        current_section = log_entry.replace("=", "").strip()
                        section_content = []
                    else:
                        section_content.append(log_entry)
                
                # Display the last section
                if current_section and section_content:
                    with st.expander(current_section, expanded=True):
                        for content in section_content:
                            if content.strip():
                                if "Matrix after" in content or "Starred matrix" in content or content.strip().startswith("[[") or content.strip().startswith("["):
                                    st.code(content)
                                else:
                                    st.text(content)
            else:
                st.info("Enable 'Show Detailed Steps' in the sidebar to see the algorithm steps.")
        
        with tab3:
            st.subheader("Assignment Visualization")
            
            # Create a simple visualization
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Create nodes
            driver_nodes = [f"D{i+1}" for i in range(original_rows)]
            route_nodes = [f"R{j+1}" for j in range(original_cols)]
            
            # Plot nodes
            for i, driver in enumerate(driver_nodes):
                ax.scatter(0, i, s=500, c='blue', alpha=0.7, edgecolors='black')
                ax.text(0, i, driver, ha='center', va='center', fontsize=12, color='white', fontweight='bold')
            
            for j, route in enumerate(route_nodes):
                ax.scatter(1, j, s=500, c='green', alpha=0.7, edgecolors='black')
                ax.text(1, j, route, ha='center', va='center', fontsize=12, color='white', fontweight='bold')
            
            # Plot assignments
            assigned_pairs = []
            for r, c in assignment:
                if r < original_rows and c < original_cols:
                    cost = st.session_state.cost_matrix[r, c]
                    assigned_pairs.append((r, c, cost))
                    
                    # Draw line
                    ax.plot([0, 1], [r, c], 'r-', linewidth=2, alpha=0.7)
                    
                    # Add cost label
                    mid_x, mid_y = 0.5, (r + c) / 2
                    ax.text(mid_x, mid_y, f"Rs.{cost:.0f}", 
                           ha='center', va='center', 
                           backgroundcolor='white',
                           fontsize=10,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
            
            ax.set_xlim(-0.5, 1.5)
            ax.set_ylim(-0.5, max(original_rows, original_cols) - 0.5)
            ax.set_xticks([0, 1])
            ax.set_xticklabels(['Drivers', 'Routes'])
            ax.set_yticks([])
            ax.set_title('Optimal Driver-Route Assignment', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 📖 How it works:
    1. **Row Reduction**: Subtract the minimum value of each row from all elements in that row
    2. **Column Reduction**: Subtract the minimum value of each column from all elements in that column
    3. **Zero Assignment**: Find optimal assignment using zeros in the matrix
    4. **Cost Calculation**: Sum the original costs of assigned pairs
    
    ### ⚠️ Note:
    - Costs should be in Rupees (Rs.)
    - The algorithm automatically balances the matrix if drivers ≠ routes
    - Dummy drivers/routes are assigned zero cost
    """)

if __name__ == "__main__":
    main()
