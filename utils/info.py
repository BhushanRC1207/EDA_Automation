
import numpy as np
import pandas as pd

class Information:
    def __init__(self, data):
        self.data = data

    def get_info(self):
        """Generate comprehensive dataset information"""
        data = pd.read_csv(self.data)
        
        info_dict = {
            "overview": self._get_overview(data),
            "missing_values": self._get_missing_values(data),
            "duplicates": self._get_duplicates(data),
            "statistics": self._get_statistics(data),
            "sample_data": self._get_sample_data(data)
        }
        
        return info_dict
    
    def _get_overview(self, data):
        """Get basic dataset overview"""
        return {
            "total_rows": int(data.shape[0]),
            "total_columns": int(data.shape[1]),
            "columns": list(data.columns),
            "memory_usage": f"{data.memory_usage(deep=True).sum() / 1024:.2f} KB",
            "numeric_columns": int(data.select_dtypes(include=['number']).shape[1]),
            "categorical_columns": int(data.select_dtypes(include=['object']).shape[1])
        }
    
    def _get_missing_values(self, data):
        """Calculate missing values with percentages"""
        missing_data = []
        for col in data.columns:
            missing_count = int(data[col].isnull().sum())
            missing_pct = round((missing_count / len(data)) * 100, 2)
            
            missing_data.append({
                "column": col,
                "missing_count": missing_count,
                "missing_percentage": missing_pct,
                "has_missing": missing_count > 0
            })
        
        total_missing = sum(item['missing_count'] for item in missing_data)
        
        return {
            "total_missing_values": total_missing,
            "columns_with_missing": sum(1 for item in missing_data if item['has_missing']),
            "details": missing_data
        }
    
    def _get_duplicates(self, data):
        """Get duplicate row information"""
        dup_count = int(data.duplicated().sum())
        return {
            "duplicate_rows": dup_count,
            "duplicate_percentage": round((dup_count / len(data)) * 100, 2),
            "has_duplicates": dup_count > 0
        }
    
    def _get_statistics(self, data):
        """Get descriptive statistics for numeric columns"""
        numeric_data = data.select_dtypes(include=['number'])
        
        if numeric_data.empty:
            return {"message": "No numeric columns found"}
        
        stats = numeric_data.describe().T
        
        stats_list = []
        for col in stats.index:
            stats_list.append({
                "column": col,
                "count": int(stats.loc[col, 'count']),
                "mean": round(stats.loc[col, 'mean'], 2),
                "std": round(stats.loc[col, 'std'], 2),
                "min": round(stats.loc[col, 'min'], 2),
                "25%": round(stats.loc[col, '25%'], 2),
                "50%": round(stats.loc[col, '50%'], 2),
                "75%": round(stats.loc[col, '75%'], 2),
                "max": round(stats.loc[col, 'max'], 2)
            })
        
        return {"numeric_columns": stats_list}
    
    def _get_sample_data(self, data):
        """Get first few rows as sample"""
        sample = data.head(5).to_dict(orient='records')
        return {
            "rows": sample,
            "note": "Showing first 5 rows"
        }