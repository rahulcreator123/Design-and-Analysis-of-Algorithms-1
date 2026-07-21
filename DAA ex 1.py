import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="Interpolation Search", page_icon="🔍")

st.title("🔍 Interpolation Search")

# ---------------------------------
# Interpolation Search
# ---------------------------------
def interpolation_search(arr, target):

    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:

        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        if arr[high] == arr[low]:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos, comparisons

        elif arr[pos] < target:
            low = pos + 1

        else:
            high = pos - 1

    return -1, comparisons


# ---------------------------------
# Binary Search
# ---------------------------------
def binary_search(arr, target):

    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:

        comparisons += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons

        elif arr[mid] < target:
            low = mid + 1

        else:
            high = mid - 1

    return -1, comparisons


# ---------------------------------
# User Input
# ---------------------------------
st.subheader("Enter Sorted Array")

array_input = st.text_input(
    "Array Elements (comma separated)",
    "5,12,18,24,31,45,52,60,71,89"
)

try:
    arr = [int(x.strip()) for x in array_input.split(",")]
    arr.sort()

except:
    st.error("Please enter valid integers.")
    st.stop()

target = st.number_input("Enter Target", value=31)

# ---------------------------------
# Search
# ---------------------------------
if st.button("Search"):

    idx, comps = interpolation_search(arr, target)

    st.subheader("Result")

    st.write("**Sorted Array:**", arr)

    if idx != -1:
        st.success(f"Element Found at Index : {idx}")
    else:
        st.error("Element Not Found")

    st.info(f"Comparisons : {comps}")

# ---------------------------------
# Performance Analysis
# ---------------------------------
st.subheader("Performance Analysis")

if st.button("Run Performance Analysis"):

    sizes = [1000, 5000, 10000, 50000, 100000]

    results = []

    for size in sizes:

        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        # Interpolation Search
        start = time.perf_counter()

        for _ in range(100):
            _, comp_is = interpolation_search(arr, target)

        is_time = ((time.perf_counter() - start) / 100) * 1000

        # Binary Search
        start = time.perf_counter()

        for _ in range(100):
            _, comp_bs = binary_search(arr, target)

        bs_time = ((time.perf_counter() - start) / 100) * 1000

        results.append({
            "Size": size,
            "IS Time (ms)": round(is_time, 4),
            "BS Time (ms)": round(bs_time, 4),
            "IS Comparisons": comp_is,
            "BS Comparisons": comp_bs
        })

    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)

# ---------------------------------
# Theory
# ---------------------------------
st.markdown("---")

st.markdown("""
## Theory

### Interpolation Search

Interpolation Search improves Binary Search by estimating the probable position
of the target using the values in the array.

It works best when the data is **uniformly distributed**.

### Formula
