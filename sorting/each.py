import random
import time
import copy
import sys
import math # Added for power sort

sys.setrecursionlimit(3000)

# --- Sorting Algorithm Definitions ---

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
    L = a[:mid]
    R = a[mid:]

    merge_sort(L)
    merge_sort(R)

    i = j = k = 0

    while i < len(L) and j < len(R):
      if L[i] <= R[j]:
        a[k] = L[i]
        i += 1
      else:
        a[k] = R[j]
        j += 1
      k += 1

    while i < len(L):
      a[k] = L[i]
      i += 1
      k += 1

    while j < len(R):
      a[k] = R[j]
      j += 1
      k += 1
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

def bubble_sort(a):
  n = len(a)
  for i in range(n):
    for j in range(0, n - i - 1):
      if a[j] > a[j + 1]:
        a[j], a[j + 1] = a[j + 1], a[j]
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
      i = i + 1
      a[i], a[j] = a[j], a[i]
  a[i + 1], a[high] = a[high], a[i + 1]
  return i + 1

def quick_sort(a):
  quick_sort_helper(a, 0, len(a) - 1)
  return a

# --- New Algorithm: Power Sort ---
def power_sort(a):
  """
  NOTE: This is NOT a standard or practical sorting algorithm.
  It is a mathematical curiosity with significant limitations:
  1. It only works correctly for lists of NON-NEGATIVE numbers.
  2. It can suffer from floating-point precision errors for large numbers or
     non-integer values, which might lead to incorrect sorting.
  """
  # Check if any numbers are negative, as the logic fails for them.
  if any(x < 0 for x in a):
      print("Warning: Power sort cannot handle negative numbers.")
      # This implementation will not sort lists with negative numbers.
      return a

  # 1. Raise each number to a power (e.g., 2)
  powered_list = [x**2 for x in a]
  # 2. Sort the list of powered numbers
  powered_list.sort()
  # 3. Take the square root of each number to revert to the original scale
  #    and update the original list in-place.
  a[:] = [int(round(math.sqrt(x))) for x in powered_list]
  return a


# --- Test and Timing Function ---

def test_sort(sort_f, label, Ns, init_l, results_d):
  print(f"{label}:")
  for n in Ns:
    # Stop testing inefficient algorithms on large lists
    if n > 5000 and label in ["selection sort", "insertion sort", "bubble sort"]:
        print(f"({n}) Skipped (too slow)")
        continue

    t_l = init_l[:n]
    l_to_sort = copy.deepcopy(t_l)

    start = time.perf_counter()
    sort_f(l_to_sort)
    end = time.perf_counter()
    time_taken = end - start

    print(f"({n}) {time_taken:.6f}")

    # Store result for winner board
    if n not in results_d:
      results_d[n] = []
    results_d[n].append((label, time_taken))

# --- Main Execution ---

if __name__ == "__main__":
  Ns = [10, 50, 100, 1000, 2000, 5000, 10000, 100000]

  MAX_N = max(Ns)
  # Ensure all numbers are positive for power sort to work
  M = 1000
  init_l = [random.randint(1, M) for _ in range(MAX_N)]

  # Dictionary to store all results: {N: [(name, time), (name, time), ...]}
  all_results = {}

  print("--- Sorting Algorithm Timing Comparison ---")

  #test_sort(selection_sort, "selection sort", Ns, init_l, all_results)
  print("-" * 20)

  test_sort(merge_sort, "merge sort", Ns, init_l, all_results)
  print("-" * 20)

  #test_sort(insertion_sort, "insertion sort", Ns, init_l, all_results)
  print("-" * 20)

  #test_sort(bubble_sort, "bubble sort", Ns, init_l, all_results)
  print("-" * 20)

  test_sort(quick_sort, "quick sort", Ns, init_l, all_results)
  print("-" * 20)

  test_sort(power_sort, "power sort", Ns, init_l, all_results)
  print("-" * 20)


  print("\n\n--- Winner Board ---")
  print("=" * 45)

  for n in Ns:
    results = all_results.get(n, [])

    if results:
      fastest = min(results, key=lambda x: x[1])
      winner_name = fastest[0].upper()
      winner_time = fastest[1]
      print(f"N = {n:<6}: {winner_name:<20} (Time: {winner_time:.6f}s)")
    else:
      print(f"N = {n:<6}: No data available")

  print("=" * 45)