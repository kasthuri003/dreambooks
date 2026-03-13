from src.data_loader import CSVDataLoader
from src.analyzers import (
    PublicationTrendAnalyzer, 
    AuthorsAnalyzer, 
    LanguageAnalyzer, 
    PublisherAnalyzer, 
    MissingISBNAnalyzer,
    LanguageYearAnalyzer
)
from src.visualizers import MatplotlibVisualizer
from src.cli import DreamBookCLI

# DESIGN PATTERN: COMPOSITION ROOT
# The main() function acts as the Composition Root. 
# This is the unique location in the application where the graph of objects is wired together.

def main():
    # SOLID: DEPENDENCY INJECTION (MANUAL)
    # We instantiate the concrete implementations here and 'inject' them into the CLI.
    # This keeps the CLI decoupled from specific loader/analyzer implementations.
    
    loader = CSVDataLoader(limit=5000)
    
    analyzers = [
        PublicationTrendAnalyzer(),
        AuthorsAnalyzer(),
        LanguageAnalyzer(),
        PublisherAnalyzer(),
        MissingISBNAnalyzer(),
        LanguageYearAnalyzer()
    ]
    
    # Default to Matplotlib
    initial_visualizer = MatplotlibVisualizer()
    
    app = DreamBookCLI(loader, analyzers, initial_visualizer)
    app.run()

if __name__ == "__main__":
    main()
