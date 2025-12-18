import numpy as np
import pandas as pd

class Information:
    def __init__(self, data):
        self.data = data

    def get_info(self):
        """
        Return a tuple representing the dimensionality of the DataFrame.
        """
        data = pd.read_csv(self.data)
        print(f"Dataset Shape: {data.shape}")

        print(data.head())
        print(data.tail())
        print(data.sample(5))
        print(data.info())

        total_missing = data.isnull().sum()
        percentage_missing = np.round((total_missing * 100) / len(data), 2)

        missing_value_df = pd.DataFrame([total_missing, percentage_missing], index=["Total_Missing", "%_Missing"]).T
        print(missing_value_df)

        print(data.describe(include="number").T)
        print(data.describe(include="O").T)
        print(data.duplicated().sum())