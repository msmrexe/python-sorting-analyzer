# sorting_analyzer/plotter.py

"""
Handles the generation of all performance plots using Seaborn.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def generate_plots(df: pd.DataFrame, output_dir: str):
    """
    Generates and saves line plots for all metrics.
    
    Args:
        df: The DataFrame containing the analysis results.
        output_dir: The directory to save plot images to.
    """
    print(f"Generating plots in '{output_dir}'...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Use a beautiful seaborn theme
    sns.set_theme(style="darkgrid")
    
    metrics = ["Time (ms)", "Comparisons", "Swaps"]
    array_types = df["Type"].unique()

    for arr_type in array_types:
        df_subset = df[df["Type"] == arr_type]
        
        for metric in metrics:
            # Skip plotting if metric is all None (e.g., Timsort ops)
            if df_subset[metric].isnull().all():
                continue
            
            plt.figure(figsize=(12, 7))
            
            # Create a line plot
            sns.lineplot(
                data=df_subset,
                x="Size",
                y=metric,
                hue="Algorithm",
                style="Algorithm", # Different line styles
                markers=True,      # Add markers
                dashes=True
            )
            
            title = f"{metric} vs. Array Size (Array Type: {arr_type})"
            plt.title(title, fontsize=16)
            plt.xlabel("Array Size", fontsize=12)
            plt.ylabel(metric, fontsize=12)
            plt.legend(title="Algorithm")
            
            # Save the file
            filename = f"{metric.lower().replace(' ', '_')}_{arr_type.lower()}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath)
            plt.close() # Close the figure to free memory

    print("All plots generated successfully.")
