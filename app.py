import numpy as np
import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="Hospital Surgery Scheduler",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        color: #1E3A8A;
        padding-bottom: 1rem;
    }
    .step-box {
        background-color: #F0F9FF;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3B82F6;
    }
    .result-box {
        background-color: #F0FDF4;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #10B981;
    }
    .iteration-box {
        background-color: #FEF3C7;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 5px solid #F59E0B;
    }
    .matrix-box {
        background-color: #F5F5F5;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: monospace;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def munkres_verbose(cost, verbose_container=None):
    """Munkres algorithm with detailed steps for Streamlit display"""
    matrix = cost.copy().astype(float)
    n = matrix.shape[0]
    
    if verbose_container:
        verbose_container.markdown("#### 📊 Initial Surgery Time Matrix")
        verbose_container.dataframe(matrix, use_container_width=True)
        verbose_container.markdown("---")
    
    steps_log = []
    
    # Step 1: Row reduction
    steps_log.append("### ⚙️ Step 1: Row Reduction")
    row_minima = []
    for i in range(n):
        mv = matrix[i].min()
        row_minima.append(mv)
        matrix[i] -= mv
    
    steps_log.append(f"Row minima: {row_minima}")
    steps_log.append("Matrix after row reduction:")
    steps_log.append(str(matrix))
    
    # Step 2: Column reduction
    steps_log.append("### ⚙️ Step 2: Column Reduction")
    col_minima = []
    for j in range(n):
        mv = matrix[:, j].min()
        col_minima.append(mv)
        matrix[:, j] -= mv
    
    steps_log.append(f"Column minima: {col_minima}")
    steps_log.append("Matrix after column reduction:")
    steps_log.append(str(matrix))
    
    # Prepare structures
    starred = np.zeros((n, n), dtype=bool)
    primed = np.zeros((n, n), dtype=bool)
    row_cov = np.zeros(n, dtype=bool)
    col_cov = np.zeros(n, dtype=bool)
    
    # Initial star zeros
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 0 and not row_cov[i] and not col_cov[j]:
                starred[i, j] = True
                row_cov[i] = True
                col_cov[j] = True
    
    row_cov[:] = False
    col_cov[:] = False
    
    # Cover columns with starred zeros
    for j in range(n):
        if starred[:, j].any():
            col_cov[j] = True
    
    steps_log.append("### 📍 Initial Assignment")
    steps_log.append("Starred zeros (initial assignment):")
    steps_log.append(str(starred.astype(int)))
    steps_log.append(f"Covered columns: {np.where(col_cov)[0].tolist()}")
    
    iteration = 1
    while True:
        iteration_log = []
        iteration_log.append(f"#### 🔄 Iteration {iteration}")
        
        if col_cov.sum() == n:
            iteration_log.append("✅ All columns covered by starred zeros — optimal matching found!")
            steps_log.extend(iteration_log)
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
            iteration_log.append(f"🔹 Primed zero at position ({i},{j})")
            
            star_col = np.where(starred[i])[0]
            
            if star_col.size == 0:
                # Found augmenting path
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
                
                iteration_log.append(f"🔄 Augmenting path: {path}")
                
                # Flip stars along the path
                for r, c in path:
                    starred[r, c] = not starred[r, c]
                
                # Reset covers and primes
                primed[:, :] = False
                row_cov[:] = False
                col_cov[:] = False
                
                # Cover columns with starred zeros
                for col in range(n):
                    if starred[:, col].any():
                        col_cov[col] = True
                
                iteration_log.append("Updated starred matrix:")
                iteration_log.append(str(starred.astype(int)))
                break
            else:
                sc = int(star_col[0])
                row_cov[i] = True
                col_cov[sc] = False
                iteration_log.append(f"📌 Covered row {i}, uncovered column {sc}")
                z = find_uncovered_zero()
        
        if find_uncovered_zero() is None:
            # Find minimum uncovered value
            min_uncovered = float('inf')
            for ii in range(n):
                if not row_cov[ii]:
                    for jj in range(n):
                        if not col_cov[jj] and matrix[ii, jj] < min_uncovered:
                            min_uncovered = matrix[ii, jj]
            
            if min_uncovered == float('inf'):
                min_uncovered = 0
            
            iteration_log.append(f"🔍 Minimum uncovered value: {min_uncovered}")
            
            # Adjust matrix
            for ii in range(n):
                for jj in range(n):
                    if not row_cov[ii] and not col_cov[jj]:
                        matrix[ii, jj] -= min_uncovered
                    elif row_cov[ii] and col_cov[jj]:
                        matrix[ii, jj] += min_uncovered
            
            iteration_log.append("Adjusted matrix:")
            iteration_log.append(str(matrix))
        
        steps_log.extend(iteration_log)
        iteration += 1
    
    # Extract final assignment
    assignment = []
    for i in range(n):
        j_idx = np.where(starred[i])[0]
        if j_idx.size > 0:
            assignment.append((i, int(j_idx[0])))
    
    return assignment, steps_log

def main():
    # Header
    st.title("🏥 Hospital Surgery Scheduling System")
    st.markdown("""
    <div class='main-header'>
    Use the Hungarian (Munkres) Algorithm to optimally assign doctors to operation rooms
    minimizing total surgery time.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for input options
    with st.sidebar:
        st.header("⚙️ Input Options")
        input_method = st.radio(
            "Choose input method:",
            ["Manual Entry", "CSV Upload", "Example Data"]
        )
        
        if input_method == "Example Data":
            example_choice = st.selectbox(
                "Select example:",
                ["Small Hospital (3x3)", "Medium Hospital (4x4)", "Large Hospital (5x5)"]
            )
            
            if example_choice == "Small Hospital (3x3)":
                example_matrix = np.array([
                    [45, 50, 60],
                    [55, 40, 50],
                    [50, 55, 45]
                ])
                rows, cols = 3, 3
            elif example_choice == "Medium Hospital (4x4)":
                example_matrix = np.array([
                    [30, 25, 40, 35],
                    [35, 40, 30, 45],
                    [40, 35, 45, 30],
                    [25, 30, 35, 40]
                ])
                rows, cols = 4, 4
            else:  # Large Hospital (5x5)
                example_matrix = np.array([
                    [60, 75, 80, 65, 70],
                    [70, 65, 75, 80, 60],
                    [80, 70, 60, 75, 65],
                    [65, 80, 70, 60, 75],
                    [75, 60, 65, 70, 80]
                ])
                rows, cols = 5, 5
            
            st.write(f"Example: {rows} doctors × {cols} rooms")
            st.dataframe(example_matrix)
            
        st.markdown("---")
        st.info("""
        **Instructions:**
        1. Enter surgery times in minutes
        2. If doctors ≠ rooms, dummy rows/cols will be added
        3. Algorithm finds optimal assignment
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    # Initialize variables
    user_matrix = None
    rows, cols = 0, 0
    
    with col1:
        st.header("📝 Input Surgery Times")
        
        if input_method == "Manual Entry":
            rows_input = st.number_input("Number of Doctors", min_value=1, max_value=10, value=3, step=1, key="rows_input")
            cols_input = st.number_input("Number of Operation Rooms", min_value=1, max_value=10, value=3, step=1, key="cols_input")
            
            # Convert to integers
            rows = int(rows_input)
            cols = int(cols_input)
            
            st.subheader("Enter Surgery Time Matrix (in minutes)")
            
            # Create input matrix
            input_data = []
            for i in range(rows):
                cols_list = st.columns(cols)
                row_data = []
                for j in range(cols):
                    with cols_list[j]:
                        value = st.number_input(
                            f"D{i+1}→R{j+1}",
                            min_value=0.0,
                            max_value=300.0,
                            value=float(30 + (i+j)*5),
                            key=f"input_{i}_{j}"
                        )
                        row_data.append(value)
                input_data.append(row_data)
            
            user_matrix = np.array(input_data)
            
        elif input_method == "CSV Upload":
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                try:
                    # Read CSV
                    df = pd.read_csv(uploaded_file, header=None)
                    user_matrix = df.to_numpy()
                    rows, cols = user_matrix.shape
                    st.success(f"Successfully loaded {rows}×{cols} matrix")
                    st.dataframe(user_matrix)
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
                    return
            else:
                st.info("Please upload a CSV file")
                return
        else:  # Example Data
            user_matrix = example_matrix
            # rows, cols are already set above
        
        # Display input matrix if it exists
        if user_matrix is not None:
            # Display input matrix
            st.subheader("📊 Input Surgery Time Matrix")
            st.dataframe(
                pd.DataFrame(
                    user_matrix,
                    index=[f"Doctor {i+1}" for i in range(rows)],
                    columns=[f"Room {j+1}" for j in range(cols)]
                ),
                use_container_width=True
            )
            
            # Calculate statistics
            st.subheader("📈 Matrix Statistics")
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Minimum Time", f"{user_matrix.min():.1f} min")
            with col_stat2:
                st.metric("Maximum Time", f"{user_matrix.max():.1f} min")
            with col_stat3:
                st.metric("Average Time", f"{user_matrix.mean():.1f} min")
    
    with col2:
        st.header("⚡ Run Optimization")
        
        if user_matrix is not None:
            if st.button("🚀 Find Optimal Assignment", type="primary", use_container_width=True):
                with st.spinner("Running Munkres algorithm..."):
                    # Balance the matrix if not square
                    n = max(rows, cols)
                    balanced = np.zeros((n, n))
                    balanced[:rows, :cols] = user_matrix
                    
                    if rows != cols:
                        st.warning(f"⚠️ Matrix balanced to {n}×{n} by adding dummy rows/columns with zero time")
                    
                    # Run algorithm
                    assignment, steps_log = munkres_verbose(balanced)
                    
                    # Display results
                    st.success("✅ Optimal Assignment Found!")
                    
                    # Create results container
                    result_container = st.container()
                    
                    with result_container:
                        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                        st.subheader("🎯 Optimal Assignment")
                        
                        total_time = 0
                        results_data = []
                        
                        for r, c in assignment:
                            if r < rows and c < cols:
                                time_val = user_matrix[r, c]
                                total_time += time_val
                                results_data.append({
                                    "Doctor": f"D{r+1}",
                                    "Room": f"R{c+1}",
                                    "Surgery Time (min)": time_val
                                })
                        
                        # Display as table
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True, hide_index=True)
                        
                        # Display total time
                        st.metric("Total Surgery Time", f"{total_time:.1f} minutes")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Display algorithm steps
                        st.subheader("🔍 Algorithm Steps")
                        
                        with st.expander("View Detailed Steps", expanded=False):
                            steps_text = "\n".join(steps_log)
                            st.markdown(steps_text)
                        
                        # Visual representation
                        st.subheader("👥 Assignment Visualization")
                        
                        # Create a simple visualization
                        if results_data:
                            viz_cols = st.columns(min(5, len(results_data)))
                            for idx, (col, result) in enumerate(zip(viz_cols, results_data)):
                                with col:
                                    st.markdown(f"""
                                    <div style='text-align: center; padding: 10px; border: 2px solid #3B82F6; border-radius: 10px; background-color: #f0f9ff;'>
                                        <h4>👨‍⚕️ {result['Doctor']}</h4>
                                        <p style='font-size: 20px; margin: 5px;'>→</p>
                                        <h4>🏥 {result['Room']}</h4>
                                        <p style='font-size: 18px; font-weight: bold; margin-top: 10px;'>{result['Surgery Time (min)']} min</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Download results
                        if not results_df.empty:
                            st.download_button(
                                label="📥 Download Results as CSV",
                                data=results_df.to_csv(index=False),
                                file_name="surgery_assignment.csv",
                                mime="text/csv"
                            )
        else:
            st.info("Please enter data in the left column first.")
        
        # Information section
        st.markdown("---")
        st.markdown("<div class='step-box'>", unsafe_allow_html=True)
        st.subheader("ℹ️ How It Works")
        st.markdown("""
        1. **Row Reduction**: Subtract minimum of each row
        2. **Column Reduction**: Subtract minimum of each column
        3. **Initial Assignment**: Star independent zeros
        4. **Iterative Improvement**: Cover zeros, find augmenting paths
        5. **Optimal Assignment**: Minimum total surgery time
        """)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
