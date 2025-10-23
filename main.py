# main.py

"""
Sorting Algorithm Analyzer - CLI

Main entry point to run the sorting analysis.
This script coordinates the analysis and plotting modules.
"""

import argparse
import numpy as np
from sorting_analyzer.analyzer import run_analysis
from sorting_analyzer.plotter import generate_plots

def main():
    """Parses CLI arguments and runs the analysis."""
    
    parser = argparse.ArgumentParser(
        description="Run a comparative analysis of sorting algorithms."
    )
    parser.add_argument(
        '--max-size',
        type=int,
        default=2000,
        help="Maximum array size to test (default: 2000)"
    )
    parser.add_argument(
        '--steps',
        type=int,
        default=10,
        help="Number of different array sizes to test (default: 10)"
    )
    parser.add_argument(
        '--csv',
        type=str,
        default="sorting_results.csv",
        help="Filename to save the raw CSV data (default: sorting_results.csv)"
    )
    parser.add_argument(
        '--plots-dir',
        type=str,
        default="plots",
        help="Directory to save the output plots (default: plots)"
    )
    args = parser.parse_args()
    
    # 1. Setup the experiment parameters
    # We use linspace to get evenly spaced steps up to max_size
    # We start from at least 10 to avoid 0-size arrays
    array_sizes = np.linspace(start=10, stop=args.max_size, num=args.steps, dtype=int).tolist()
    
    algo_names = [
        "Insertion Sort",
        "Bubble Sort",
        "Merge Sort",
        "Quicksort",
        "Timsort (Python built-in)"
    ]
    
    array_types = ["Random", "Sorted", "Reversed"]
    
    print("--- Starting Sorting Analysis ---")
    print(f"Algorithms: {', '.join(algo_names)}")
    print(f"Array Sizes: {array_sizes}")
    print(f"Array Types: {', '.join(array_types)}")
    
    # 2. Run the analysis
    df = run_analysis(algo_names, array_sizes, array_types)
    
    # 3. Save the raw data
    df.to_csv(args.csv, index=False)
    print(f"\nRaw results saved to '{args.csv}'")
    
    # 4. Generate plots
    generate_plots(df, args.plots_dir)
    
    print("--- Analysis Complete ---")

if __name__ == "__main__":
    main()
