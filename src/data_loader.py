import pandas as pd
import os
from .interfaces import IDataLoader

# SOLID: SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# This file is dedicated solely to data loading logic. 

# OOP: INHERITANCE
# CSVDataLoader 'is-a' IDataLoader. It inherits the structure and fulfills the contract
# defined by the interface.

class CSVDataLoader(IDataLoader):
    """Implementation of IDataLoader for CSV files."""
    
    def __init__(self, limit: int = 5000):
        """
        Initialize the loader.
        
        # CLEAN CODING: MEANINGFUL NAMES
        # 'limit' is a clear name for the maximum number of rows to load.
        
        # OOP: ENCAPSULATION
        # The 'limit' attribute is encapsulated within the object.
        """
        self.limit = limit
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        # CLEAN CODING: Error Handling
        # We validate the file path and use try-except blocks to fail gracefully.
        
        Loads data from a CSV file into a Pandas DataFrame.
        
        DATA STRUCTURE: PANDAS DATAFRAME
        A DataFrame is a 2D labeled data structure, like a table.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            # Basic cleaning
            df = pd.read_csv(file_path, nrows=self.limit)
            df.columns = df.columns.str.strip().str.lower()
            
            return df
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
