import pandas as pd
import numpy as np
from scipy import stats
from typing import Any, Dict, List, Tuple
from .interfaces import IAnalyzer

# DESIGN PATTERN: STRATEGY PATTERN
# Each analyzer class below is a 'Strategy' for performing a specific type of data analysis.
# They all implement the IAnalyzer interface, allowing them to be swapped interchangeably
# depending on user choice.

# SOLID: OPEN/CLOSED PRINCIPLE (OCP)
# The system is OPEN for extension (we can add new analyzers by creating new classes)
# but CLOSED for modification (we don't need to change the existing CLI to add new logic).

# SOLID: LISKOV SUBSTITUTION PRINCIPLE (LSP)
# Any subclass of IAnalyzer can be used wherever IAnalyzer is expected (e.g., in the
# CLI's analyzer list) without breaking the system.

# SOLID: SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# PublicationTrendAnalyzer only calculates the trend and counts over years.

class PublicationTrendAnalyzer(IAnalyzer):
    """
    Analyzes how publication volume changes over time.
    """
    @property
    def name(self) -> str:
        return "Publication Trends Over Time"
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        # DATA STRUCTURE: DICTIONARY
        # We return a dictionary to bundle multiple related results (counts and trend line).
        
        if 'publication date' not in data.columns:
             return {"error": "Column 'publication date' not found"}

        years_series = pd.to_numeric(data['publication date'], errors='coerce')
        years = years_series.dropna().astype(int)
        
        # CLEAN CODING: NO MAGIC NUMBERS
        # We use explicit bounds (1800, 2026) to filter relevant data years.
        years = years[(years > 1800) & (years <= 2026)]
        
        # DATA STRUCTURE: PANDAS SERIES
        # value_counts() returns a Series where indices are years and values are counts.
        trends = years.value_counts().sort_index()
        
        trend_line_data = None
        if not trends.empty and len(trends) > 1:
            x = trends.index.to_numpy()
            y = trends.values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            trend_line_data = {
                "slope": slope,
                "intercept": intercept,
                "r_value": r_value,
                "description": f"Linear Trend: y = {slope:.2f}x + {intercept:.2f} (R2={r_value**2:.2f})"
            }
            
        return {"counts": trends, "trend_line": trend_line_data}

# SOLID: SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# AuthorsAnalyzer only focuses on finding the most frequent authors.

class AuthorsAnalyzer(IAnalyzer):
    """
    Identifies the top authors in the dataset.
    """
    @property
    def name(self) -> str:
        return "Top 5 Most Prolific Authors"
    
    def analyze(self, data: pd.DataFrame) -> pd.Series:
        if 'author' not in data.columns:
            return pd.Series(dtype=object)
            
        return data['author'].value_counts().head(5)

class LanguageAnalyzer(IAnalyzer):
    """
    Analyzes the distribution of books across languages.
    """
    @property
    def name(self) -> str:
        return "Language Distribution"
    
    def analyze(self, data: pd.DataFrame) -> pd.Series:
        if 'language' not in data.columns:
            return pd.Series(dtype=object)
            
        return data['language'].value_counts()

# OOP: POLYMORPHISM
# Every analyzer implements its own version of the analyze() method.
# The CLI calls this method without needing to know the specific class type.

class PublisherAnalyzer(IAnalyzer):
    """
    Analyzes the number of books per publisher, grouping tail publishers under 'Others'.
    """
    @property
    def name(self) -> str:
        return "Books per Publisher"
    
    def analyze(self, data: pd.DataFrame) -> pd.Series:
        if 'book publisher' not in data.columns:
             if 'publisher' in data.columns:
                 col = 'publisher'
             else:
                 return pd.Series(dtype=object)
        else:
            col = 'book publisher'

        counts = data[col].value_counts()
        
        top_n = 20
        if len(counts) > top_n:
            top_counts = counts.head(top_n)
            others_slice = counts.iloc[top_n:]
            others_count = others_slice.sum()
            top_counts['Others'] = others_count
            
            return {
                "counts": top_counts,
                "others_details": others_slice
            }
        
        return counts

class MissingISBNAnalyzer(IAnalyzer):
    """
    Identifies records missing ISBN data.
    """
    @property
    def name(self) -> str:
        return "Missing ISBN Analysis"
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        total_records = len(data)
        if 'isbn' not in data.columns:
             return {"total": total_records, "missing": total_records, "percentage": 100.0}
        
        missing_count = data['isbn'].isna().sum()
        
        percentage = (missing_count / total_records) * 100 if total_records > 0 else 0
        
        return {
            "total": total_records,
            "missing": int(missing_count),
            "percentage": round(percentage, 2)
        }

class LanguageYearAnalyzer(IAnalyzer):
    """
    Analyzes book counts grouped by both year and language.
    """
    @property
    def name(self) -> str:
         return "Books per Year by Language"

    def analyze(self, data: pd.DataFrame) -> pd.DataFrame:
        required_cols = ['publication date', 'language']
        if not all(col in data.columns for col in required_cols):
             return pd.DataFrame()

        df_clean = data.copy()
        df_clean['year'] = pd.to_numeric(df_clean['publication date'], errors='coerce')
        df_clean = df_clean.dropna(subset=['year'])
        df_clean['year'] = df_clean['year'].astype(int)
        # CLEAN CODING: NO MAGIC NUMBERS
        df_clean = df_clean[(df_clean['year'] > 1800) & (df_clean['year'] <= 2026)]

        # DATA STRUCTURE: PANDAS DATAFRAME (PIVOT TABLE)
        # unstack() creates a DataFrame where columns represent languages.
        pivot = df_clean.groupby(['year', 'language']).size().unstack(fill_value=0)
        return pivot
