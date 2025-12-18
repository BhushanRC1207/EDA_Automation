import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

class Analysis:
    def __init__(self, data):
        self.data = data

    def get_viz(self):
        data = pd.read_csv(self.data)

        numeric_cols = data.select_dtypes(include="number").columns
        categorical_cols = data.select_dtypes(include="O").columns

        for col in numeric_cols:
            self.num_univariate(data, col)

    def num_univariate(self, data, col):
        print("-"*50)
        print(f"Feature name: {col}")

        print(f"Skewness: {np.round(data[col].skew(), 2)}")

        fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

       
        sns.histplot(data[col], kde=True, ax=ax[0])
        ax[0].set_title(f"Distribution of {col}")
        ax[0].set_xlabel("")  


        sns.boxplot(x=data[col], ax=ax[1], orient="h")


        plt.tight_layout()
        plt.show()