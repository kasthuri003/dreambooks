import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Any, Dict, List
from .interfaces import IVisualizer

# DESIGN PATTERN: SIMPLE FACTORY (CONCEPTUAL)
# ThemeManager encapsulates the creation and management of theme configurations.
# It acts like a factory by providing theme products based on requested names.

# OOP: ENCAPSULATION
# Themes and current state are bundled inside ThemeManager, hidden from outside direct access.

class ThemeManager:
    # OOP: ENCAPSULATION
    # Themes are stored as a private/internal dictionary within the class.
    THEMES = {
        'default': {
            'bg': 'white', 'text': 'black', 'accent1': 'blue', 'accent2': 'orange', 'grid': 'gray'
        },
        'cyberpunk': {
            'bg': '#1a1a1a', 'text': '#00ffff', 'accent1': '#ff00ff', 'accent2': '#00ff00', 'grid': '#333333'
        },
        'vintage': {
            'bg': '#f4e4bc', 'text': '#4a3c31', 'accent1': '#8b4513', 'accent2': '#2f4f4f', 'grid': '#d3c6a6'
        },
        'oceanic': {
            'bg': '#001f3f', 'text': '#ffffff', 'accent1': '#39cccc', 'accent2': '#0074d9', 'grid': '#003366'
        }
    }
    
    current_theme_name = 'default'
    
    @classmethod
    def set_theme(cls, theme_name: str):
        if theme_name in cls.THEMES:
            cls.current_theme_name = theme_name
        else:
            print(f"Theme '{theme_name}' not found. Using current.")

    @classmethod
    def get_current(cls):
        return cls.THEMES[cls.current_theme_name]

# OOP: POLYMORPHISM
# Both MatplotlibVisualizer and PlotlyVisualizer implement the visualize() method.
# The CLI doesn't need to know the specific library used; it just calls visualize().
# This makes it easy to add more visualizers (e.g., Bokeh, Seaborn).

class MatplotlibVisualizer(IVisualizer):
    """
    Renders static plots using the Matplotlib library.
    """
    def visualize(self, data: Any, title: str, chart_type: str = 'bar', xlabel: str = None, ylabel: str = None, log_scale: bool = False) -> None:
        theme = ThemeManager.get_current()
        
        plt.rcParams['figure.facecolor'] = theme['bg']
        plt.rcParams['axes.facecolor'] = theme['bg']
        plt.rcParams['axes.edgecolor'] = theme['text']
        plt.rcParams['axes.labelcolor'] = theme['text']
        plt.rcParams['xtick.color'] = theme['text']
        plt.rcParams['ytick.color'] = theme['text']
        plt.rcParams['text.color'] = theme['text']
        plt.rcParams['grid.color'] = theme['grid']
        
        if isinstance(data, dict) and "counts" in data and "trend_line" in data:
            self._visualize_trend(data, title, theme)
            return

        plt.figure(figsize=(10, 6))
        
        if chart_type == 'bar':
             if isinstance(data, pd.Series):
                 ax = data.plot(kind='bar', color=theme['accent1'])
                 if log_scale:
                     plt.yscale('log')
                 
                 for container in ax.containers:
                     ax.bar_label(container)
                     
                 plt.ylabel(ylabel if ylabel else 'Count')
                 plt.xlabel(xlabel if xlabel else 'Category')
        elif chart_type == 'line':
             if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
                 ax = data.plot(kind='line', marker='o', color=theme['accent1'] if isinstance(data, pd.Series) else None, ax=plt.gca())
                 plt.ylabel('Count')
                 plt.xlabel('Year')
                 if isinstance(data, pd.DataFrame):
                     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                     plt.tight_layout()
                 
                 if hasattr(data, 'index') and np.issubdtype(data.index.dtype, np.number):
                     min_year = int(data.index.min())
                     max_year = int(data.index.max())
                     plt.xticks(np.arange(min_year, max_year + 1, 1), rotation=45)
        elif chart_type == 'pie':
             if isinstance(data, pd.Series):
                 total = data.sum()
                 threshold = 0.01 * total
                 
                 main_data = data[data >= threshold]
                 small_data = data[data < threshold]
                 
                 if not small_data.empty:
                     others_sum = small_data.sum()
                     main_data['Others'] = others_sum
                 
                 colors = [theme['accent1'], theme['accent2'], '#888888', '#aaaaaa', '#cccccc'] 
                 
                 main_data.plot(kind='pie', autopct='%1.1f%%', colors=colors, startangle=90)
                 plt.ylabel('')
        
        plt.title(title, color=theme['text'])
        plt.grid(True, color=theme['grid'], linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    # CLEAN CODING: DRY (DON'T REPEAT YOURSELF)
    # The theme application logic is separated into _apply_theme to be reused.

    def _visualize_trend(self, data: Dict, title: str, theme: Dict):
        counts = data['counts']
        trend = data['trend_line']
        
        plt.figure(figsize=(12, 6))
        
        plt.plot(counts.index, counts.values, marker='o', color=theme['accent1'], label='Actual Counts')
        
        if trend:
            x = counts.index.to_numpy()
            y_trend = trend['slope'] * x + trend['intercept']
            plt.plot(x, y_trend, linestyle='--', color=theme['accent2'], label='Trend Line')
            title = f"{title}\n{trend['description']}"
            
        plt.title(title, color=theme['text'])
        plt.xlabel('Year')
        plt.ylabel('Number of Books')
        plt.legend()
        plt.grid(True, color=theme['grid'], linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

class PlotlyVisualizer(IVisualizer):
    """
    Renders interactive plots in a browser using the Plotly library.
    """
    def visualize(self, data: Any, title: str, chart_type: str = 'bar', xlabel: str = None, ylabel: str = None, log_scale: bool = False) -> None:
        theme = ThemeManager.get_current()
        
        if isinstance(data, dict) and "counts" in data:
             self._visualize_trend_with_plotly(data, title, theme)
             return

        fig = None
        
        if chart_type == 'bar':
             if isinstance(data, pd.Series):
                 fig = px.bar(x=data.index, y=data.values, labels={'x': xlabel if xlabel else 'Category', 'y': ylabel if ylabel else 'Count'}, title=title, text_auto=True)
                 fig.update_traces(marker_color=theme['accent1'])
                 if log_scale:
                     fig.update_layout(yaxis_type="log")
        elif chart_type == 'line':
            if isinstance(data, pd.Series):
                fig = px.line(x=data.index, y=data.values, labels={'x': 'Year', 'y': 'Count'}, title=title, markers=True)
                fig.update_traces(line_color=theme['accent1'])
            elif isinstance(data, pd.DataFrame):
                fig = px.line(data, labels={'value': 'Count', 'year': 'Year', 'variable': 'Language'}, title=title, markers=True)
                fig.update_layout(
                    colorway=[theme['accent1'], theme['accent2'], theme['text']],
                    xaxis=dict(dtick=1)
                )
        elif chart_type == 'pie':
            if isinstance(data, pd.Series):
                 total = data.sum()
                 threshold = 0.01 * total
                 
                 main_data = data[data >= threshold]
                 small_data = data[data < threshold]
                 
                 if not small_data.empty:
                     others_sum = small_data.sum()
                     main_data['Others'] = others_sum
                 
                 fig = px.pie(values=main_data.values, names=main_data.index, title=title)
                 fig.update_traces(marker=dict(colors=[theme['accent1'], theme['accent2'], '#777777', '#999999']))
        
        if fig:
            self._apply_theme(fig, theme)
            fig.show()

    def _visualize_trend_with_plotly(self, data: Dict, title: str, theme: Dict):
        counts = data['counts']
        trend = data['trend_line']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=counts.index, 
            y=counts.values, 
            mode='lines+markers', 
            name='Actual Counts',
            line=dict(color=theme['accent1'])
        ))
        
        if trend:
            x = counts.index.to_numpy()
            y_trend = trend['slope'] * x + trend['intercept']
            fig.add_trace(go.Scatter(
                x=x, 
                y=y_trend, 
                mode='lines', 
                name='Trend Line', 
                line=dict(dash='dash', color=theme['accent2'])
            ))
            title = f"{title}<br>{trend['description']}"
            
        fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Count')
        self._apply_theme(fig, theme)
        fig.show()

    # CLEAN CODING: MEANINGFUL NAMES
    # Function names like '_apply_theme' clearly describe their purpose.

    def _apply_theme(self, fig, theme):
        fig.update_layout(
            paper_bgcolor=theme['bg'],
            plot_bgcolor=theme['bg'],
            font_color=theme['text'],
            xaxis=dict(gridcolor=theme['grid'], zerolinecolor=theme['grid']),
            yaxis=dict(gridcolor=theme['grid'], zerolinecolor=theme['grid'])
        )
