import random
import time
import copy
import sys
import math

# ==============================================================================
# === USER CONFIGURATION ===
# ==============================================================================
# array sizes
Ns = [10, 50, 100, 1000, 5000, 10000]

#  maximum value for random 
M = 1000

# number of competitions
NUM_RUNS = 100
# === SORTING METHOD SELECTION ===
# 1: Bubble Sort        5: Quick Sort
# 2: Insertion Sort     6: Power Sort
# 3: Selection Sort     7: Counting Sort
# 4: Merge Sort
choices = [4, 5, 6]
# ==============================================================================
# ==============================================================================


sys.setrecursionlimit(3000)

# --- Sorting Algorithm Definitions ---

def bubble_sort(a):
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def selection_sort(a):
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def merge_sort(a):
    if len(a) > 1:
        mid = len(a) // 2
        L, R = a[:mid], a[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: a[k] = L[i]; i += 1
            else: a[k] = R[j]; j += 1
            k += 1
        while i < len(L): a[k] = L[i]; i += 1; k += 1
        while j < len(R): a[k] = R[j]; j += 1; k += 1
    return a

def quick_sort(a):
    if not a: return a
    quick_sort_helper(a, 0, len(a) - 1)
    return a

def quick_sort_helper(a, low, high):
    if low < high:
        pi = partition(a, low, high)
        quick_sort_helper(a, low, pi - 1)
        quick_sort_helper(a, pi + 1, high)

def partition(a, low, high):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1

def power_sort(a):
    """Mathematical curiosity sort. Fast because it uses Timsort internally."""
    if any(x < 0 for x in a): return a
    a.sort()
    return a

def counting_sort(a):
    """Efficient for integers in a known, small range."""
    if not a: return a
    if any(x < 0 for x in a): return a # Does not support negative numbers

    max_val = max(a)
    count = [0] * (max_val + 1)
    for x in a:
        count[x] += 1

    i = 0
    for val in range(max_val + 1):
        for _ in range(count[val]):
            a[i] = val
            i += 1
    return a

# --- Test and Timing Functions ---

def run_single_test(sort_f, l):
    """Times a single run of a sorting function."""
    l_to_sort = copy.deepcopy(l)
    start = time.perf_counter()
    sort_f(l_to_sort)
    end = time.perf_counter()
    return end - start

def run_competition(sort_funcs, labels, Ns, init_l, num_runs):
    """Runs a head-to-head competition for the selected algorithms."""
    win_counts = {}
    slow_algorithms = {"Bubble Sort", "Insertion Sort", "Selection Sort"}

    # Generate header for the competition title
    title_header = " vs ".join([label.upper() for label in labels])
    print(f"\n--- Competition: {title_header} ({num_runs} Runs) ---")

    for n in Ns:
        print(f"N = {n}: Running {num_runs} competitions...")
        win_counts[n] = {label: 0 for label in labels}

        # Skip slow algorithms for large N to save time
        active_indices = [i for i, label in enumerate(labels) if not (n > 5000 and label in slow_algorithms)]
        if len(active_indices) < len(labels):
            skipped_labels = [l for l in labels if l in slow_algorithms]
            print(f"  (Skipping {', '.join(skipped_labels)} for N > 5000)")

        # If all selected algorithms are slow and skipped, continue to next N
        if not active_indices:
            continue

        for _ in range(num_runs):
            t_l = init_l[:n]
            times = []
            # Only time the active algorithms
            for i in active_indices:
                times.append(run_single_test(sort_funcs[i], t_l))

            if not times: continue

            min_time = min(times)
            # Find the original index of the winner
            winner_original_index = active_indices[times.index(min_time)]

            # Award the win
            win_counts[n][labels[winner_original_index]] += 1

        # Print intermediate results for the current N
        result_line = ", ".join([f"{label}: {win_counts[n][label]}" for label in labels])
        print(f"  Completed. Wins -> {result_line}")
        print("-" * 20)

    return win_counts

# --- Main Execution ---
if __name__ == "__main__":
    SORTING_ALGORITHMS = {
        '1': ("Bubble Sort", bubble_sort),
        '2': ("Insertion Sort", insertion_sort),
        '3': ("Selection Sort", selection_sort),
        '4': ("Merge Sort", merge_sort),
        '5': ("Quick Sort", quick_sort),
        '6': ("Power Sort", power_sort),
        '7': ("Counting Sort", counting_sort)
    }

    # --- User Selection ---
    print("=== Sorting Algorithm Competition ===")

    chosen_funcs, chosen_labels = [], []
    while True:
        try:
            choices = [str(i) for i in choices]
            chosen_funcs = [SORTING_ALGORITHMS[key][1] for key in choices]
            chosen_labels = [SORTING_ALGORITHMS[key][0] for key in choices]
            break
        except KeyError as e:
            print(f"Invalid selection: {e}. Please choose numbers from the list.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # --- Setup and Run ---
    MAX_N = max(Ns)
    # Ensure all numbers are positive for Power Sort and Counting Sort
    init_l = [random.randint(1, M) for _ in range(MAX_N)]

    final_wins = run_competition(chosen_funcs, chosen_labels, Ns, init_l, NUM_RUNS)

    # --- Final Results Table ---
    print("\n\n--- Final Competition Results (Total Wins) ---")

    # Dynamic header
    header = f"{'N':<8} | " + " | ".join([f"{label.upper()+' WINS':<20}" for label in chosen_labels])
    print("=" * len(header))
    print(header)
    print("=" * len(header))

    # Dynamic rows
    for n in Ns:
        results = final_wins.get(n, {})
        row_data = [f"{results.get(label, 0):<20}" for label in chosen_labels]
        print(f"{n:<8} | " + " | ".join(row_data))

    print("=" * len(header))
