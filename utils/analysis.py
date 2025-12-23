import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

class Analysis:
    def __init__(self, data_path):
        self.data_path = data_path

    def get_viz(self):
        """Generate visualizations and return as base64-encoded images"""
        data = pd.read_csv(self.data_path)
        
        numeric_cols = data.select_dtypes(include="number").columns
        categorical_cols = data.select_dtypes(include="O").columns
        
        results = {
            "numeric_columns": list(numeric_cols),
            "categorical_columns": list(categorical_cols),
            "visualizations": []
        }
        
        for col in numeric_cols:
            viz_data = self.num_univariate(data, col)
            results["visualizations"].append(viz_data)
        
        return results

    def num_univariate(self, data, col):
        """Generate univariate analysis for numeric column"""
        # Calculate statistics
        skewness = np.round(data[col].skew(), 2)
        mean_val = np.round(data[col].mean(), 2)
        median_val = np.round(data[col].median(), 2)
        std_val = np.round(data[col].std(), 2)
        
        # Create figure
        fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Histogram with KDE
        sns.histplot(data[col], kde=True, ax=ax[0])
        ax[0].set_title(f"Distribution of {col}")
        ax[0].set_xlabel("")
        
        # Boxplot
        sns.boxplot(x=data[col], ax=ax[1], orient="h")
        ax[1].set_xlabel(col)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close(fig)
        
        return {
            "column": col,
            "statistics": {
                "skewness": skewness,
                "mean": mean_val,
                "median": median_val,
                "std": std_val
            },
            "image": img_base64
        }