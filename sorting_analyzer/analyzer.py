# sorting_analyzer/analyzer.py

"""
Handles the execution of sorting experiments.

Generates arrays of different types and sizes, runs
each algorithm, and records time, comparisons, and swaps.
"""

import time
import random
import pandas as pd
from .algorithms import ALGORITHM_MAP

def generate_array(size: int, array_type: str) -> list:
    """Generates an array of a specific size and type."""
    arr = list(range(size))
    if array_type == "Random":
        random.shuffle(arr)
    elif array_type == "Sorted":
        pass # Already sorted
    elif array_type == "Reversed":
        arr.reverse()
    return arr

def run_analysis(algo_names: list[str], array_sizes: list[int], array_types: list[str]) -> pd.DataFrame:
    """
    Runs the full analysis and returns a DataFrame with results.
    
    Args:
        algo_names: List of algorithm names to test.
        array_sizes: List of array sizes to test.
        array_types: List of array types ('Random', 'Sorted', 'Reversed').
        
    Returns:
        A pandas DataFrame containing all experiment results.
    """
    results = []
    
    for name in algo_names:
        print(f"Testing Algorithm: {name}...")
        for size in array_sizes:
            for arr_type in array_types:
                
                arr_to_sort = generate_array(size, arr_type)
                
                # --- Special case for Timsort (built-in) ---
                if name == "Timsort (Python built-in)":
                    # We can only time it, not get internal ops
                    start_time = time.perf_counter()
                    sorted(arr_to_sort) # Run out-of-place sort
                    end_time = time.perf_counter()
                    
                    results.append({
                        "Algorithm": name,
                        "Size": size,
                        "Type": arr_type,
                        "Time (ms)": (end_time - start_time) * 1000,
                        "Comparisons": None, # Cannot be measured
                        "Swaps": None,       # Cannot be measured
                    })
                    continue

                # --- For all other algorithms ---
                func = ALGORITHM_MAP[name]
                
                # Run the sort, record time, and get op counts
                start_time = time.perf_counter()
                comparisons, swaps = func(arr_to_sort) # Sorts in-place
                end_time = time.perf_counter()
                
                elapsed_ms = (end_time - start_time) * 1000
                
                results.append({
                    "Algorithm": name,
                    "Size": size,
                    "Type": arr_type,
                    "Time (ms)": elapsed_ms,
                    "Comparisons": comparisons,
                    "Swaps": swaps
                })
        print(f"Finished {name}.")

    return pd.DataFrame(results)
