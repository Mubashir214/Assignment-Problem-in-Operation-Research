# Hungarian Algorithm / Munkres Algorithm for Delivery Route Optimization

## 📌 Project Overview

This project implements the **Hungarian Algorithm (Munkres Algorithm)** in Python using **NumPy** to solve the **Assignment Problem**.

The program is designed for a **FreshDrinks delivery system**, where:

* Delivery drivers must be assigned to delivery routes
* Each assignment has a delivery cost
* The goal is to minimize the total delivery cost

The implementation provides:

* Step-by-step verbose output
* Row reduction and column reduction visualization
* Starred and primed zero tracking
* Matrix balancing for non-square matrices
* Final optimal assignment with minimum total cost

---

## 🎯 Objective

To find the **minimum-cost assignment** between:

* Drivers
* Delivery Routes

using the Hungarian Optimization Technique.

---

## 🛠 Technologies Used

* Python 3
* NumPy

---

## 📂 Features

✅ User input for dynamic cost matrices
✅ Supports rectangular matrices
✅ Automatically balances non-square matrices
✅ Verbose explanation of every algorithm step
✅ Displays:

* Row reduction
* Column reduction
* Starred zeros
* Primed zeros
* Matrix adjustments
* Final optimal assignments

✅ Calculates minimum total delivery cost

---

## 📌 Hungarian Algorithm Steps Implemented

### 1. Row Reduction

Subtract the minimum value from each row.

### 2. Column Reduction

Subtract the minimum value from each column.

### 3. Star Initial Zeros

Select independent zeros and mark them as starred.

### 4. Cover Columns

Cover columns containing starred zeros.

### 5. Prime Uncovered Zeros

Find uncovered zeros and prime them.

### 6. Augment Path

Create augmenting paths and update starred zeros.

### 7. Matrix Adjustment

Adjust uncovered values until an optimal assignment is found.

---

## 📥 Input Format

The user enters:

1. Number of delivery drivers
2. Number of delivery routes
3. Cost matrix row by row

Example:

```text
Enter number of Delivery Drivers: 3
Enter number of Delivery Routes: 3

Enter delivery cost matrix row by row (3 x 3):

Driver 1: 4 1 3
Driver 2: 2 0 5
Driver 3: 3 2 2
```

---

## 📤 Example Output

```text
===== FINAL ASSIGNMENT (DRIVER → ROUTE) =====

Driver 1 -> Route 2 | Cost = Rs. 1
Driver 2 -> Route 1 | Cost = Rs. 2
Driver 3 -> Route 3 | Cost = Rs. 2

✅ Total Minimum Delivery Cost = Rs. 5
```

---

## ▶️ How to Run

### Step 1: Install NumPy

```bash
pip install numpy
```

### Step 2: Run the Program

```bash
python munkres_delivery.py
```

---

## 📖 Code Explanation

### `munkres_verbose(cost)`

Main function implementing the Hungarian Algorithm.

#### Responsibilities:

* Performs row and column reduction
* Tracks starred and primed zeros
* Handles covering/uncovering rows and columns
* Finds augmenting paths
* Produces optimal assignments

---

## 📌 Matrix Balancing

If the number of drivers and routes are unequal:

* The program automatically creates a square matrix
* Dummy rows/columns are filled with zeros

Example:

```python
n = max(rows, cols)
balanced = np.zeros((n, n))
```

---

## 📊 Time Complexity

The Hungarian Algorithm has:

[
O(n^3)
]

time complexity, making it efficient for assignment optimization problems.

O(n^3)

---

## 📌 Applications

This algorithm can be used in:

* Delivery route optimization
* Employee-task assignment
* Job scheduling
* Resource allocation
* Logistics management
* Transportation systems

---

## 📁 Project Structure

```text
project/
│
├── munkres_delivery.py
├── README.md
```

---

## ✅ Advantages

* Guarantees optimal solution
* Efficient for medium and large datasets
* Easy to understand due to verbose output
* Supports real-world logistics problems

---

## 👨‍💻 Author

Developed for learning and implementing:

* Operations Research
* Optimization Techniques
* Assignment Problems
* Logistics Optimization using Python
