# sorting_analyzer/algorithms.py

"""
Contains all the sorting algorithm implementations.

Each function takes a list of numbers, sorts it *in-place*,
and returns a tuple: (comparison_count, swap_count).
"""

def insertion_sort(arr: list) -> tuple[int, int]:
    """Sorts a list in-place using Insertion Sort."""
    comparisons = 0
    swaps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # We count this as the first comparison for the loop
        comparisons += 1
        while j >= 0 and key < arr[j]:
            comparisons += 1 # Count each comparison in the loop
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        arr[j + 1] = key
        # The placement of 'key' is not a swap, it's an insertion
    return comparisons, swaps

def bubble_sort(arr: list) -> tuple[int, int]:
    """Sorts a list in-place using Bubble Sort."""
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break # Optimized: stop if no swaps in a pass
    return comparisons, swaps

def merge_sort(arr: list) -> tuple[int, int]:
    """
    Wrapper for the recursive merge sort.
    Returns (comparisons, data_movements).
    Note: Swaps are not a natural metric for merge sort,
    so we count data_movements (writes to the list).
    """
    comparisons = 0
    movements = 0
    
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        # Recursive calls
        comps_l, moves_l = merge_sort(L)
        comps_r, moves_r = merge_sort(R)
        comparisons += comps_l + comps_r
        movements += moves_l + moves_r

        i = j = k = 0
        
        # Merge logic
        while i < len(L) and j < len(R):
            comparisons += 1
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            movements += 1
            k += 1

        # Copy remaining elements
        while i < len(L):
            arr[k] = L[i]
            movements += 1
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            movements += 1
            j += 1
            k += 1
            
    return comparisons, movements

def quicksort(arr: list) -> tuple[int, int]:
    """Wrapper for the recursive quicksort."""
    
    def _partition(arr, low, high) -> tuple[int, int, int]:
        """
        Partitions the array using the last element as pivot.
        Returns (pivot_index, comparisons, swaps).
        """
        pivot = arr[high]
        i = low - 1
        comps = 0
        swaps = 0
        
        for j in range(low, high):
            comps += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                
        # Place pivot
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        return i + 1, comps, swaps

    def _quicksort_recursive(arr, low, high) -> tuple[int, int]:
        """Recursive helper for quicksort."""
        total_comps = 0
        total_swaps = 0
        if low < high:
            pi, comps, swaps = _partition(arr, low, high)
            total_comps += comps
            total_swaps += swaps
            
            # Recursive calls
            comps_l, swaps_l = _quicksort_recursive(arr, low, pi - 1)
            comps_r, swaps_r = _quicksort_recursive(arr, pi + 1, high)
            
            total_comps += comps_l + comps_r
            total_swaps += swaps_l + swaps_r
            
        return total_comps, total_swaps

    return _quicksort_recursive(arr, 0, len(arr) - 1)

# A map to easily access functions by name
ALGORITHM_MAP = {
    "Insertion Sort": insertion_sort,
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quicksort": quicksort,
}
