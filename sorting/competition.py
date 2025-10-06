import random
import time
import copy
import sys
import math

sys.setrecursionlimit(3000)

# --- Sorting Algorithm Definitions ---

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
    """
    NOTE: This is NOT a standard or practical sorting algorithm.
    It is a mathematical curiosity with significant limitations.
    """
    if any(x < 0 for x in a):
        print("Warning: Power sort cannot handle negative numbers.")
        return a
    powered_list = [x**2 for x in a]
    powered_list.sort() # Uses Python's built-in Timsort
    a[:] = [int(round(math.sqrt(x))) for x in powered_list]
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
    """
    Runs a head-to-head competition for a set number of runs.
    """
    win_counts = {}
    print(f"--- Competition: {labels[0].upper()} vs {labels[1].upper()} vs {labels[2].upper()} ({num_runs} Runs) ---")

    for n in Ns:
        t_l = init_l[:n]
        print(f"N = {n}: Running {num_runs} competitions...")

        # Initialize win counts for this N
        win_counts[n] = {label: 0 for label in labels}

        for _ in range(num_runs):
            # Time each algorithm on the same data
            time1 = run_single_test(sort_funcs[0], t_l)
            time2 = run_single_test(sort_funcs[1], t_l)
            time3 = run_single_test(sort_funcs[2], t_l)

            times = [time1, time2, time3]
            min_time = min(times)
            winner_index = times.index(min_time)

            # Award the win
            win_counts[n][labels[winner_index]] += 1

        print(f"  Completed. Wins -> {labels[0]}: {win_counts[n][labels[0]]}, "
              f"{labels[1]}: {win_counts[n][labels[1]]}, {labels[2]}: {win_counts[n][labels[2]]}")
        print("-" * 20)
    return win_counts

# --- Main Execution ---

if __name__ == "__main__":
    Ns = [10, 50, 100, 1000, 2000, 5000, 10000, 100000]
    NUM_RUNS = 100
    MAX_N = max(Ns)
    # Ensure all numbers are positive for power sort to work
    M = 1000
    init_l = [random.randint(1, M) for _ in range(MAX_N)]

    # --- 3-Way Sorting Competition ---

    sort_functions = [merge_sort, quick_sort, power_sort]
    sort_labels = ["merge sort", "quick sort", "power sort"]

    final_wins = run_competition(sort_functions, sort_labels, Ns, init_l, NUM_RUNS)

    print("\n\n--- Final Competition Results (Total Wins) ---")
    print("=" * 70)
    print(f"{'N':<8} | {'MERGE SORT WINS':<20} | {'QUICK SORT WINS':<20} | {'POWER SORT WINS':<20}")
    print("=" * 70)

    for n in Ns:
        results = final_wins.get(n, {})
        merge_wins = results.get("merge sort", 0)
        quick_wins = results.get("quick sort", 0)
        power_wins = results.get("power sort", 0)

        print(f"{n:<8} | {merge_wins:<20} | {quick_wins:<20} | {power_wins:<20}")

    print("=" * 70)