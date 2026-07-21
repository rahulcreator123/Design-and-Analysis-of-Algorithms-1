import streamlit as st
import random
import time
import pandas as pd

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(page_title="Interpolation Search", page_icon="🔍")

st.title("🔍 Interpolation Search")
st.write("Compare **Interpolation Search** with **Binary Search**.")

# ---------------------------------
# Interpolation Search
# ---------------------------------
def interpolation_search(arr, target):

    low = 0
    high = len(arr) - 1
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

    low = 0
    high = len(arr) - 1
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
st.subheader("Input Array")

array_input = st.text_input(
    "Enter Array Elements (comma separated)",
    "5,12,18,24,31,45,52,60,71,89"
)

try:
    arr = [int(x.strip()) for x in array_input.split(",")]

    if len(arr) == 0:
        st.error("Array cannot be empty.")
        st.stop()

    arr.sort()

except:
    st.error("Please enter valid integers separated by commas.")
    st.stop()

target = st.number_input(
    "Enter Target Element",
    value=31,
    step=1
)

# ---------------------------------
# Search Button
# ---------------------------------
if st.button("Search"):

    idx, comps = interpolation_search(arr, target)

    st.subheader("Search Result")

    st.write("**Sorted Array:**")
    st.write(arr)

    if idx != -1:
        st.success(f"✅ Element found at index {idx}")
    else:
        st.error("❌ Element not found")

    st.info(f"Interpolation Search Comparisons: {comps}")


# ---------------------------------
# Performance Analysis
# ---------------------------------
st.subheader("Performance Analysis")

if st.button("Run Performance Analysis"):

    sizes = [1000, 5000, 10000, 50000, 100000]

    results = []

    for size in sizes:

        arr = sorted(random.sample(range(size * 10), size))
        target = random.choice(arr)

        # Interpolation Search Timing
        start = time.perf_counter()

        for _ in range(100):
            _, comp_is = interpolation_search(arr, target)

        is_time = ((time.perf_counter() - start) / 100) * 1000

        # Binary Search Timing
        start = time.perf_counter()

        for _ in range(100):
            _, comp_bs = binary_search(arr, target)

        bs_time = ((time.perf_counter() - start) / 100) * 1000

        results.append({
            "Array Size": size,
            "Interpolation Time (ms)": round(is_time, 5),
            "Binary Time (ms)": round(bs_time, 5),
            "Interpolation Comparisons": comp_is,
            "Binary Comparisons": comp_bs
        })

    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)


# ---------------------------------
# Theory
# ---------------------------------
st.markdown("---")

st.header("Theory")

st.markdown("""
### Interpolation Search

Interpolation Search is an improved version of Binary Search for **uniformly distributed sorted arrays**.

Instead of checking the middle element, it estimates the probable position of the target.

### Formula
