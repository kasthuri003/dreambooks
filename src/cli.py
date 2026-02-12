from typing import List, Dict
import pandas as pd
from .interfaces import IDataLoader, IAnalyzer, IVisualizer
from .visualizers import MatplotlibVisualizer, PlotlyVisualizer, ThemeManager

class DreamBookCLI:
    # SOLID: DEPENDENCY INJECTION (DI)
    # Instead of creating loader, analyzers, or visualizers inside the class,
    # we 'inject' them through the constructor. This makes the class more testable.

    # SOLID: DEPENDENCY INVERSION PRINCIPLE (DIP)
    # DreamBookCLI depends on high-level abstractions (IDataLoader, IAnalyzer)
    # rather than low-level concrete implementations (CSVDataLoader).

    # OOP: COMPOSITION
    # DreamBookCLI 'has-a' loader, list of analyzers, and a visualizer.
    # This is often preferred over deep inheritance hierarchies.

    def __init__(self, loader: IDataLoader, analyzers: List[IAnalyzer], initial_visualizer: IVisualizer):
        self.loader = loader
        self.analyzers = analyzers
        self.visualizer = initial_visualizer
        self.data = None
        self.file_path = "C:\\Users\\LENOVO\\Documents\\Dreambooks\\Dataset Books.csv"
        self.vis_mode = 'matplotlib' # default

    # SOLID: SINGLE RESPONSIBILITY PRINCIPLE (SRP)
    # The load_data method is only responsible for the data loading flow.
    def load_data(self):
        print("Loading data...")
        try:
            self.data = self.loader.load_data(self.file_path)
            print(f"Data loaded successfully: {len(self.data)} rows.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def toggle_visualizer(self):
        if self.vis_mode == 'matplotlib':
            self.vis_mode = 'plotly'
            self.visualizer = PlotlyVisualizer()
            print("Switched to Plotly (Interactive Browser)")
        else:
            self.vis_mode = 'matplotlib'
            self.visualizer = MatplotlibVisualizer()
            print("Switched to Matplotlib (Popup Window)")

    def switch_theme(self):
        print("\nAvailable Themes:")
        from .visualizers import ThemeManager
        themes = list(ThemeManager.THEMES.keys())
        for i, t in enumerate(themes):
            print(f"{i+1}. {t}")
        
        choice = input("Select a theme: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(themes):
                 selected = themes[idx]
                 ThemeManager.set_theme(selected)
                 print(f"Theme set to: {selected}")
                 if self.vis_mode == 'matplotlib':
                     pass
            else:
                 print("Invalid theme.")
        else:
             print("Invalid selection.")

    # SOLID: OPEN/CLOSED PRINCIPLE (OCP)
    # The run_analysis method is open for extension; it can handle any analyzer
    # that implements IAnalyzer without needing modifications.
    def run_analysis(self, analyzer_index: int):
        if self.data is None:
            print("No data loaded. Please load data first.")
            return

        analyzer = self.analyzers[analyzer_index]
        print(f"\nPerforming: {analyzer.name}...")
        
        # OOP: POLYMORPHISM IN ACTION:
        # We call analyze() on the interface type. The specific implementation
        # (e.g. PublicationTrendAnalyzer) is executed at runtime.
        results = analyzer.analyze(self.data)
        
        self.display_textual_summary(results)
        
        chart_type = 'bar'
        xlabel = 'Category'
        ylabel = 'Count'
        log_scale = False

        if "Trend" in analyzer.name or "Year" in analyzer.name:
            chart_type = 'line'
            xlabel = 'Year'
        elif "Language" in analyzer.name:
            chart_type = 'bar'
            xlabel = 'Language'
            ylabel = 'No. of Books'
            log_scale = True
        elif "Distribution" in analyzer.name or "ISBN" in analyzer.name:
            chart_type = 'pie'
            
        if isinstance(results, dict) and 'missing' in results and 'percentage' in results:
             pie_data = pd.Series([results['missing'], results['total'] - results['missing']], index=['Missing', 'Present'])
             self.visualizer.visualize(pie_data, analyzer.name, 'pie')
        else:
             viz_data = results
             if isinstance(results, dict) and 'counts' in results:
                 viz_data = results['counts']
                 
             self.visualizer.visualize(viz_data, analyzer.name, chart_type, xlabel=xlabel, ylabel=ylabel, log_scale=log_scale)

    def display_textual_summary(self, results):
        print("\n--- Textual Summary ---")
        if isinstance(results, pd.Series) or isinstance(results, pd.DataFrame):
            print(results.to_string())
        elif isinstance(results, dict):
            if 'counts' in results and 'others_details' in results:
                 print(results['counts'])
                 
                 others_slice = results['others_details']
                 others_total_books = others_slice.sum()
                 others_unique_publishers = len(others_slice)
                 
                 print("\n--- Details of 'Others' ---")
                 print(f"Total Books in 'Others': {others_total_books}")
                 print(f"Number of Publishers in 'Others': {others_unique_publishers}")
                 print("-" * 30)
                 print(others_slice.to_string())
                 return

            for k, v in results.items():
                if k != 'counts' and k != 'trend_line':
                     print(f"{k}: {v}")
            
            if "trend_line" in results and results["trend_line"]:
                 print(results["trend_line"]["description"])
                 print("top 5 years:")
                 print(results["counts"].head(5))

    def run(self):
        self.load_data()
        
        while True:
            print("\n--- Dream Book Shop Data Analysis ---")
            print(f"Visualizer: {self.vis_mode} (Press 'v' to toggle)")
            print(f"Current Theme: {ThemeManager.current_theme_name}") 
            for i, analyzer in enumerate(self.analyzers):
                print(f"{i + 1}. {analyzer.name}")
            print("t. Switch Theme")
            print("q. Quit")
            
            choice = input("Select an option: ")
            
            if choice.lower() == 'q':
                break
            elif choice.lower() == 'v':
                self.toggle_visualizer()
            elif choice.lower() == 't':
                self.switch_theme()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.analyzers):
                    self.run_analysis(idx)
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
