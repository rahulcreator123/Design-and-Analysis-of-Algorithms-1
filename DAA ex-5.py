import streamlit as st
import random

st.set_page_config(page_title="Min-Max using Divide & Conquer", page_icon="📊")

st.title("📊 Minimum and Maximum using Divide & Conquer")

comparison_count = 0


# Divide and Conquer Function
def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2

    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Combine
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


# Naive Method
def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    comps = 0

    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


# Sidebar
st.sidebar.header("Input Options")

choice = st.sidebar.radio(
    "Choose Input Method",
    ("Enter Custom Array", "Generate Random Array")
)

if choice == "Enter Custom Array":
    arr_input = st.text_input(
        "Enter numbers separated by commas",
        "3,1,7,4,9,2,8,5,6,0"
    )

    try:
        arr = [int(x.strip()) for x in arr_input.split(",")]
    except:
        st.error("Please enter valid integers separated by commas.")
        st.stop()

else:
    size = st.sidebar.slider("Array Size", 2, 100, 10)
    arr = [random.randint(1, 100) for _ in range(size)]

st.subheader("Input Array")
st.write(arr)

# Run Algorithm
if st.button("Find Min & Max"):

    comparison_count = 0

    mn, mx = min_max_dc(arr, 0, len(arr) - 1)
    dc_comps = comparison_count

    _, _, naive_comps = min_max_naive(arr)

    st.success(f"Minimum Element: **{mn}**")
    st.success(f"Maximum Element: **{mx}**")

    st.subheader("Comparison Count")

    st.table({
        "Method": ["Divide & Conquer", "Naive"],
        "Comparisons": [dc_comps, naive_comps]
    })

# Performance Analysis
st.subheader("Performance Analysis")

if st.button("Run Performance Analysis"):

    sizes = [10, 100, 1000, 10000]

    results = []

    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]

        comparison_count = 0

        mn, mx = min_max_dc(arr, 0, len(arr) - 1)
        dc = comparison_count

        _, _, naive = min_max_naive(arr)

        formula = 3 * size // 2 - 2

        results.append({
            "Size": size,
            "DC Comparisons": dc,
            "Naive Comparisons": naive,
            "Formula (3n/2 - 2)": formula
        })

    st.table(results)

st.markdown("---")
st.markdown(
    """
    **Theory**

    - **Divide & Conquer**
      - Divides the array into two halves.
      - Finds minimum and maximum recursively.
      - Combines results using only **2 comparisons**.
      - Time Complexity: **O(n)**
      - Space Complexity: **O(log n)** (recursion stack)

    - **Naive Method**
      - Scans the array once.
      - Uses **2(n−1)** comparisons.
      - Time Complexity: **O(n)**
      - Space Complexity: **O(1)**
    """
)