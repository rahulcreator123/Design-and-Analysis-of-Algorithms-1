import streamlit as st
import pandas as pd

st.set_page_config(page_title="Matrix Chain Multiplication", page_icon="🔗")

st.title("🔗 Matrix Chain Multiplication using Dynamic Programming")

# -----------------------------
# Matrix Chain Multiplication
# -----------------------------
def matrix_chain_order(dims):
    n = len(dims) - 1

    # Cost table
    m = [[0] * (n + 1) for _ in range(n + 1)]

    # Split table
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # Chain length
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')

            for k in range(i, j):
                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


# -----------------------------
# Print Parenthesization
# -----------------------------
def print_optimal_parens(s, i, j):
    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# -----------------------------
# User Input
# -----------------------------
st.subheader("Enter Matrix Dimensions")

dimension_input = st.text_input(
    "Dimensions (comma separated)",
    "10,30,5,60,10"
)

try:
    dims = [int(x.strip()) for x in dimension_input.split(",")]

    if len(dims) < 2:
        st.error("Enter at least two dimensions.")
        st.stop()

except:
    st.error("Please enter valid integers separated by commas.")
    st.stop()

n = len(dims) - 1

st.subheader("Matrices")

for i in range(n):
    st.write(f"**A{i+1} :** {dims[i]} × {dims[i+1]}")

# -----------------------------
# Solve
# -----------------------------
if st.button("Compute"):

    m, s = matrix_chain_order(dims)

    st.success(f"Minimum Scalar Multiplications: {m[1][n]}")

    st.success(
        f"Optimal Parenthesization: {print_optimal_parens(s,1,n)}"
    )

    # -------------------------
    # DP Table
    # -------------------------
    st.subheader("DP Cost Table")

    table = []

    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):

            if j < i:
                row.append("---")
            else:
                row.append(m[i][j])

        table.append(row)

    df = pd.DataFrame(
        table,
        index=[f"A{i}" for i in range(1, n + 1)],
        columns=[f"A{i}" for i in range(1, n + 1)]
    )

    st.dataframe(df, use_container_width=True)

# -----------------------------
# Theory
# -----------------------------
st.markdown("---")

st.markdown("""
### Algorithm

Matrix Chain Multiplication is solved using **Dynamic Programming**.

- Finds the optimal order of multiplying matrices.
- Minimizes the number of scalar multiplications.
- Uses a DP table to store intermediate results.

### Complexity

- **Time Complexity:** O(n³)
- **Space Complexity:** O(n²)

### Example

Input Dimensions:

`10,30,5,60,10`

Matrices:

- A1 = 10 × 30
- A2 = 30 × 5
- A3 = 5 × 60
- A4 = 60 × 10

Output:

- Minimum Cost = **5000**
- Optimal Parenthesization = **((A1 × A2) × (A3 × A4))**
""")