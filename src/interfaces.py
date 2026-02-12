from abc import ABC, abstractmethod
from typing import Any, Dict
import pandas as pd

# OOP: ABSTRACTION
# The following classes use ABC (Abstract Base Class) to define contracts.
# This is a core OOP concept where we define 'what' an object does without specifying 'how'.

# SOLID: SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# Each interface has one clear responsibility: loading, analyzing, or visualizing.

# CLEAN CODING: MEANINGFUL NAMES
# Interface names start with 'I' (e.g., IDataLoader) to clearly distinguish 
# them from concrete implementations.

class IDataLoader(ABC):
    """Interface for loading data from various sources."""
    
    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from a file.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            DataFrame containing the loaded data
        """
        pass

# SOLID: INTERFACE SEGREGATION PRINCIPLE (ISP)
# We split IAnalyzer and IVisualizer instead of having one 'IBookApp' interface.
# This ensures that a class implementing an analyzer doesn't have to worry about visualization.

class IAnalyzer(ABC):
    """Interface for data analysis strategies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the human-readable name of the analysis."""
        pass
    
    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> Any:
        """
        Analyze the provided data.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            Analysis results
        """
        pass

class IVisualizer(ABC):
    """Interface for visualizing analysis results."""
    
    @abstractmethod
    def visualize(self, data: Any, title: str, chart_type: str = 'bar', xlabel: str = None, ylabel: str = None, log_scale: bool = False) -> None:
        """
        Visualize the provided data.
        
        Args:
            data: Data to visualize
            title: Title of the visualization
            chart_type: Type of chart ('bar', 'line', 'pie', etc.)
        """
        pass
