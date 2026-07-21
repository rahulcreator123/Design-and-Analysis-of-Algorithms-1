import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="String Matching Algorithms", page_icon="🔍")

st.title("🔍 String Matching Algorithms")
st.write("Compare **Naive**, **KMP**, and **Rabin-Karp** algorithms.")

# -------------------------------------------------
# Naive Search
# -------------------------------------------------
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)

    return matches, comparisons


# -------------------------------------------------
# Compute LPS for KMP
# -------------------------------------------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


# -------------------------------------------------
# KMP Search
# -------------------------------------------------
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


# -------------------------------------------------
# Rabin-Karp
# -------------------------------------------------
def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)

    d = 256
    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# -------------------------------------------------
# User Input
# -------------------------------------------------
st.subheader("Input")

text = st.text_area(
    "Enter Text",
    "ABABDABACDABABCABAB"
)

pattern = st.text_input(
    "Enter Pattern",
    "ABABCABAB"
)

# -------------------------------------------------
# Search Button
# -------------------------------------------------
if st.button("Search"):

    if pattern == "":
        st.error("Pattern cannot be empty.")
    else:

        m1, c1 = naive_search(text, pattern)
        m2, c2 = kmp_search(text, pattern)
        m3, c3 = rabin_karp(text, pattern)

        df = pd.DataFrame({
            "Algorithm": [
                "Naive",
                "KMP",
                "Rabin-Karp"
            ],
            "Matches": [
                str(m1),
                str(m2),
                str(m3)
            ],
            "Comparisons": [
                c1,
                c2,
                c3
            ]
        })

        st.subheader("Results")
        st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# Performance Analysis
# -------------------------------------------------
st.subheader("Performance Analysis")

if st.button("Run Performance Analysis"):

    text_large = "".join(random.choices("ABCD", k=10000))

    patterns = [
        "AB",
        "ABCD",
        "ABCDAB",
        "ABCDABCD"
    ]

    results = []

    for p in patterns:

        _, c1 = naive_search(text_large, p)
        _, c2 = kmp_search(text_large, p)
        _, c3 = rabin_karp(text_large, p)

        results.append({
            "Pattern": p,
            "Naive Comparisons": c1,
            "KMP Comparisons": c2,
            "Rabin-Karp Comparisons": c3
        })

    st.dataframe(pd.DataFrame(results), use_container_width=True)

# -------------------------------------------------
# Theory
# -------------------------------------------------
st.markdown("---")

st.markdown("""
## Theory

### 1. Naive String Matching
- Compares the pattern with every possible position in the text.
- Simple but inefficient for large texts.

**Time Complexity**
- Best: **O(n)**
- Average: **O(nm)**
- Worst: **O(nm)**

---

### 2. Knuth-Morris-Pratt (KMP)
- Uses an **LPS (Longest Prefix Suffix)** table.
- Avoids unnecessary comparisons after a mismatch.

**Time Complexity**
- Best: **O(n)**
- Average: **O(n + m)**
- Worst: **O(n + m)**

---

### 3. Rabin-Karp
- Uses **hash values** to compare substrings.
- Only performs character-by-character comparison when hash values match.

**Time Complexity**
- Best: **O(n + m)**
- Average: **O(n + m)**
- Worst: **O(nm)** (many hash collisions)

---

## Space Complexity

- Naive : **O(1)**
- KMP : **O(m)** (LPS table)
- Rabin-Karp : **O(1)**

### Observation

- **Naive** is easy to implement but performs many comparisons.
- **KMP** is generally the most efficient for repeated pattern searches.
- **Rabin-Karp** performs well for multiple pattern matching due to hashing.
""")
