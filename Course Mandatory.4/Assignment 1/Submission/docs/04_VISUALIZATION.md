# Data Visualization Study Notes - AAL Project

## Advanced Data Visualization
*Personal Study Notes: Visualization Techniques*

### Setup and Configuration

```python
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib.gridspec import GridSpec
from typing import List, Dict, Tuple, Optional

# Set visualization styles
def setup_visualization_style():
    """Configure consistent visualization styles."""
    try:
        # Set style parameters
        plt.style.use('seaborn')
        sns.set_palette('husl')
        
        # Custom style parameters
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
        
        # Set color blind friendly palette
        sns.set_palette('colorblind')
        
        print("Visualization style configured successfully")
        
    except Exception as e:
        print(f"Error setting visualization style: {str(e)}")
        raise

# Call setup function
setup_visualization_style()
```

### Visualization Utilities

```python
def create_figure(width: int = 12, height: int = 8) -> Tuple[plt.Figure, plt.Axes]:
    """Create a new figure with specified dimensions.
    
    Args:
        width: Figure width in inches
        height: Figure height in inches
        
    Returns:
        Tuple of (figure, axes)
    """
    try:
        fig, ax = plt.subplots(figsize=(width, height))
        return fig, ax
    except Exception as e:
        print(f"Error creating figure: {str(e)}")
        raise

def save_plot(fig: plt.Figure, filename: str, dpi: int = 300):
    """Save plot to file with error handling.
    
    Args:
        fig: Figure to save
        filename: Output filename
        dpi: Resolution in dots per inch
    """
    try:
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving plot: {str(e)}")
        raise

def add_annotations(ax: plt.Axes, title: str, xlabel: str, ylabel: str):
    """Add consistent annotations to plot.
    
    Args:
        ax: Axes to annotate
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    try:
        ax.set_title(title, pad=20)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Error adding annotations: {str(e)}")
        raise
```

### Regional Analysis Framework

```python
class RegionalAnalysis:
    """Class for regional performance visualization."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with dataframe.
        
        Args:
            df: Input dataframe with sales data
        """
        self.df = df.copy()
        self.validate_data()
    
    def validate_data(self):
        """Validate required columns exist."""
        required_cols = ['State', 'Sales', 'Group']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def plot_sales_distribution(self) -> plt.Figure:
        """Create regional sales distribution plot.
        
        Returns:
            matplotlib Figure object
        """
        try:
            fig, ax = create_figure(15, 8)
            
            # Create boxplot
            sns.boxplot(
                data=self.df,
                x='State',
                y='Sales',
                hue='Group',
                ax=ax
            )
            
            # Add annotations
            add_annotations(
                ax=ax,
                title='Regional Sales Distribution Analysis',
                xlabel='State Location',
                ylabel='Sales Value (AUD)'
            )
            
            # Customize legend
            ax.legend(title='Customer Segment', bbox_to_anchor=(1.05, 1))
            
            # Add statistical annotations
            state_means = self.df.groupby('State')['Sales'].mean()
            for i, state in enumerate(state_means.index):
                ax.text(i, state_means[state], 
                        f'Mean:\n${state_means[state]:,.0f}',
                        ha='center', va='bottom')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating sales distribution plot: {str(e)}")
            raise
    
    def plot_total_revenue(self) -> plt.Figure:
        """Create total revenue by region plot.
        
        Returns:
            matplotlib Figure object
        """
        try:
            # Aggregate data
            revenue_data = self.df.groupby('State').agg({
                'Sales': ['sum', 'count'],
                'Group': 'nunique'
            }).reset_index()
            
            revenue_data.columns = ['State', 'Total_Sales', 'Transaction_Count', 'Unique_Groups']
            
            fig, ax = create_figure(15, 6)
            
            # Create barplot
            bars = sns.barplot(
                data=revenue_data,
                x='State',
                y='Total_Sales',
                ax=ax
            )
            
            # Add value labels
            for i, bar in enumerate(bars.patches):
                transactions = revenue_data.iloc[i]['Transaction_Count']
                groups = revenue_data.iloc[i]['Unique_Groups']
                
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}\n'
                    f'({transactions:,} trans)\n'
                    f'({groups} groups)',
                    ha='center', va='bottom'
                )
            
            # Add annotations
            add_annotations(
                ax=ax,
                title='Regional Revenue Analysis',
                xlabel='State Market',
                ylabel='Total Revenue (AUD)'
            )
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating total revenue plot: {str(e)}")
            raise

# Create analysis object and generate plots
regional_analysis = RegionalAnalysis(df)

# Generate and display plots
fig1 = regional_analysis.plot_sales_distribution()
plt.show()

fig2 = regional_analysis.plot_total_revenue()
plt.show()

# Optionally save plots
save_plot(fig1, 'regional_distribution.png')
save_plot(fig2, 'regional_revenue.png')
```

### Customer Segment Analysis

```python
class SegmentAnalysis:
    """Class for customer segment analysis visualization."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with dataframe.
        
        Args:
            df: Input dataframe with sales data
        """
        self.df = df.copy()
        self.validate_data()
        
    def validate_data(self):
        """Validate required columns exist."""
        required_cols = ['Group', 'Sales']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def plot_revenue_distribution(self) -> plt.Figure:
        """Create segment revenue distribution plot.
        
        Returns:
            matplotlib Figure object
        """
        try:
            fig, ax = create_figure(15, 6)
            
            # Plot distribution for each group
            for group in self.df['Group'].unique():
                group_data = self.df[self.df['Group'] == group]['Sales']
                
                sns.kdeplot(
                    data=group_data,
                    label=f"{group} (Mean: ${group_data.mean():,.0f})",
                    ax=ax
                )
                
                # Add vertical line for mean
                ax.axvline(
                    x=group_data.mean(),
                    color=ax.lines[-1].get_color(),
                    linestyle='--',
                    alpha=0.5
                )
            
            # Add annotations
            add_annotations(
                ax=ax,
                title='Segment Revenue Distribution Analysis',
                xlabel='Revenue Range (AUD)',
                ylabel='Density'
            )
            
            # Customize legend
            ax.legend(title='Customer Segments', bbox_to_anchor=(1.05, 1))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating revenue distribution plot: {str(e)}")
            raise
    
    def plot_segment_performance(self) -> plt.Figure:
        """Create segment performance comparison plot.
        
        Returns:
            matplotlib Figure object
        """
        try:
            # Aggregate segment metrics
            segment_metrics = self.df.groupby('Group').agg({
                'Sales': ['sum', 'mean', 'count', 'std']
            }).round(2)
            
            segment_metrics.columns = ['Total_Sales', 'Avg_Sale', 'Transactions', 'Std_Dev']
            segment_metrics = segment_metrics.reset_index()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Total revenue plot
            bars1 = sns.barplot(
                data=segment_metrics,
                x='Group',
                y='Total_Sales',
                ax=ax1
            )
            
            # Add value labels
            for i, bar in enumerate(bars1.patches):
                transactions = segment_metrics.iloc[i]['Transactions']
                ax1.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}\n'
                    f'({transactions:,} trans)',
                    ha='center', va='bottom'
                )
            
            add_annotations(
                ax=ax1,
                title='Total Revenue by Segment',
                xlabel='Customer Segment',
                ylabel='Total Revenue (AUD)'
            )
            
            # Average sale plot
            bars2 = sns.barplot(
                data=segment_metrics,
                x='Group',
                y='Avg_Sale',
                ax=ax2
            )
            
            # Add value labels with std dev
            for i, bar in enumerate(bars2.patches):
                std_dev = segment_metrics.iloc[i]['Std_Dev']
                ax2.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}\n'
                    f'(±${std_dev:,.0f})',
                    ha='center', va='bottom'
                )
            
            add_annotations(
                ax=ax2,
                title='Average Sale by Segment',
                xlabel='Customer Segment',
                ylabel='Average Sale (AUD)'
            )
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating segment performance plot: {str(e)}")
            raise

# Create analysis object and generate plots
segment_analysis = SegmentAnalysis(df)

# Generate and display plots
fig1 = segment_analysis.plot_revenue_distribution()
plt.show()

fig2 = segment_analysis.plot_segment_performance()
plt.show()

# Optionally save plots
save_plot(fig1, 'segment_distribution.png')
save_plot(fig2, 'segment_performance.png')
```

### Time Pattern Analysis Framework

```python
class TimePatternAnalysis:
    """Class for temporal pattern analysis visualization."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with dataframe.
        
        Args:
            df: Input dataframe with sales data
        """
        self.df = df.copy()
        self.validate_data()
        self.prepare_time_components()
    
    def validate_data(self):
        """Validate required columns exist."""
        required_cols = ['Date', 'Sales']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Ensure Date is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['Date']):
            try:
                self.df['Date'] = pd.to_datetime(self.df['Date'])
            except Exception as e:
                raise ValueError(f"Error converting Date to datetime: {str(e)}")
    
    def prepare_time_components(self):
        """Extract time components from date."""
        try:
            self.df['Hour'] = self.df['Date'].dt.hour
            self.df['DayOfWeek'] = self.df['Date'].dt.day_name()
            self.df['WeekDay'] = self.df['Date'].dt.dayofweek
            self.df['Month'] = self.df['Date'].dt.month
            self.df['Quarter'] = self.df['Date'].dt.quarter
            
        except Exception as e:
            print(f"Error preparing time components: {str(e)}")
            raise
    
    def plot_daily_pattern(self) -> plt.Figure:
        """Create daily sales pattern plot.
        
        Returns:
            matplotlib Figure object
        """
        try:
            # Calculate hourly patterns
            hourly_metrics = self.df.groupby('Hour').agg({
                'Sales': ['mean', 'std', 'count']
            }).round(2)
            
            hourly_metrics.columns = ['Mean_Sales', 'Std_Dev', 'Transaction_Count']
            hourly_pattern = hourly_metrics['Mean_Sales']
            
            # Identify peak times (top 25%)
            peak_times = hourly_pattern[hourly_pattern > hourly_pattern.quantile(0.75)].index
            
            fig, ax = create_figure(15, 6)
            
            # Plot mean sales
            ax.plot(
                hourly_pattern.index,
                hourly_pattern.values,
                marker='o',
                label='Average Sales'
            )
            
            # Add confidence interval
            ax.fill_between(
                hourly_pattern.index,
                hourly_pattern - hourly_metrics['Std_Dev'],
                hourly_pattern + hourly_metrics['Std_Dev'],
                alpha=0.2,
                label='±1 Std Dev'
            )
            
            # Highlight peak times
            ax.vlines(
                peak_times,
                ymin=hourly_pattern.min(),
                ymax=hourly_pattern.max(),
                colors='red',
                linestyles='dashed',
                label='Peak Hours'
            )
            
            # Add transaction counts
            ax2 = ax.twinx()
            ax2.plot(
                hourly_metrics.index,
                hourly_metrics['Transaction_Count'],
                color='green',
                linestyle=':',
                label='Transaction Count'
            )
            ax2.set_ylabel('Number of Transactions')
            
            # Combine legends
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
            
            # Add annotations
            add_annotations(
                ax=ax,
                title='Daily Sales Pattern Analysis',
                xlabel='Hour of Day (24-hour)',
                ylabel='Average Sales (AUD)'
            )
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating daily pattern plot: {str(e)}")
            raise
    
    def plot_weekly_heatmap(self) -> plt.Figure:
        """Create weekly pattern heatmap.
        
        Returns:
            matplotlib Figure object
        """
        try:
            # Create pivot table for heatmap
            time_patterns = pd.pivot_table(
                data=self.df,
                values='Sales',
                index='DayOfWeek',
                columns='Hour',
                aggfunc='mean'
            ).round(0)
            
            # Ensure days are in correct order
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']
            time_patterns = time_patterns.reindex(day_order)
            
            fig, ax = create_figure(15, 8)
            
            # Create heatmap
            sns.heatmap(
                time_patterns,
                cmap='YlOrRd',
                annot=True,
                fmt=',d',
                ax=ax,
                cbar_kws={'label': 'Average Sales (AUD)'}
            )
            
            # Add annotations
            ax.set_title('Weekly Business Pattern Analysis', pad=20)
            ax.set_xlabel('Hour of Day')
            ax.set_ylabel('Day of Week')
            
            # Add peak hour markers
            peak_mask = time_patterns > time_patterns.values.mean() + time_patterns.values.std()
            for i in range(peak_mask.shape[0]):
                for j in range(peak_mask.shape[1]):
                    if peak_mask.iloc[i, j]:
                        ax.add_patch(plt.Rectangle(
                            (j, i),
                            1,
                            1,
                            fill=False,
                            edgecolor='black',
                            lw=2
                        ))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating weekly heatmap: {str(e)}")
            raise
    
    def plot_monthly_trends(self) -> plt.Figure:
        """Create monthly trends plot.
        
        Returns:
            matplotlib Figure object
        """
        try:
            # Calculate monthly metrics
            monthly_metrics = self.df.groupby(['Month', 'Quarter']).agg({
                'Sales': ['sum', 'mean', 'count']
            }).round(2)
            
            monthly_metrics.columns = ['Total_Sales', 'Avg_Sale', 'Transactions']
            monthly_metrics = monthly_metrics.reset_index()
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
            
            # Plot total sales by month
            bars1 = sns.barplot(
                data=monthly_metrics,
                x='Month',
                y='Total_Sales',
                hue='Quarter',
                ax=ax1
            )
            
            # Add value labels
            for i, bar in enumerate(bars1.patches):
                ax1.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}',
                    ha='center',
                    va='bottom'
                )
            
            add_annotations(
                ax=ax1,
                title='Monthly Sales Trends',
                xlabel='Month',
                ylabel='Total Sales (AUD)'
            )
            
            # Plot average transaction value
            bars2 = sns.barplot(
                data=monthly_metrics,
                x='Month',
                y='Avg_Sale',
                hue='Quarter',
                ax=ax2
            )
            
            # Add transaction count labels
            for i, bar in enumerate(bars2.patches):
                transactions = monthly_metrics.iloc[i]['Transactions']
                ax2.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}\n({transactions:,} trans)',
                    ha='center',
                    va='bottom'
                )
            
            add_annotations(
                ax=ax2,
                title='Monthly Average Sale',
                xlabel='Month',
                ylabel='Average Sale (AUD)'
            )
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating monthly trends plot: {str(e)}")
            raise

# Create analysis object and generate plots
time_analysis = TimePatternAnalysis(df)

# Generate and display plots
fig1 = time_analysis.plot_daily_pattern()
plt.show()

fig2 = time_analysis.plot_weekly_heatmap()
plt.show()

fig3 = time_analysis.plot_monthly_trends()
plt.show()

# Optionally save plots
save_plot(fig1, 'daily_pattern.png')
save_plot(fig2, 'weekly_pattern.png')
save_plot(fig3, 'monthly_trends.png')
```

### Dashboard Development Guide

```python
class SalesDashboard:
    """Class for creating comprehensive sales analysis dashboard."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with dataframe.
        
        Args:
            df: Input dataframe with sales data
        """
        self.df = df.copy()
        self.validate_data()
        self.prepare_time_components()
        
    def validate_data(self):
        """Validate required columns exist."""
        required_cols = ['Date', 'Sales', 'State', 'Group']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Ensure Date is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['Date']):
            try:
                self.df['Date'] = pd.to_datetime(self.df['Date'])
            except Exception as e:
                raise ValueError(f"Error converting Date to datetime: {str(e)}")
    
    def prepare_time_components(self):
        """Extract time components from date."""
        try:
            self.df['Hour'] = self.df['Date'].dt.hour
            self.df['DayOfWeek'] = self.df['Date'].dt.day_name()
            self.df['Month'] = self.df['Date'].dt.month_name()
            self.df['Quarter'] = self.df['Date'].dt.quarter
            
        except Exception as e:
            print(f"Error preparing time components: {str(e)}")
            raise
    
    def create_static_dashboard(self) -> plt.Figure:
        """Create static dashboard with multiple views.
        
        Returns:
            matplotlib Figure object
        """
        try:
            # Create figure with grid layout
            fig = plt.figure(figsize=(20, 15))
            gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])
            
            # 1. Sales Trend (Top Panel)
            ax1 = fig.add_subplot(gs[0, :])
            daily_trend = self.df.groupby('Date')['Sales'].agg(['sum', 'count'])
            
            # Plot daily sales
            line1 = ax1.plot(
                daily_trend.index,
                daily_trend['sum'],
                label='Daily Sales',
                color='blue'
            )[0]
            
            # Add transaction count on secondary axis
            ax1_twin = ax1.twinx()
            line2 = ax1_twin.plot(
                daily_trend.index,
                daily_trend['count'],
                label='Transactions',
                color='red',
                linestyle='--'
            )[0]
            
            # Combine legends
            ax1.legend(handles=[line1, line2], loc='upper right')
            
            add_annotations(
                ax=ax1,
                title='Daily Revenue and Transaction Trends',
                xlabel='Date',
                ylabel='Daily Revenue (AUD)'
            )
            ax1_twin.set_ylabel('Number of Transactions')
            
            # 2. Regional Performance (Middle Left)
            ax2 = fig.add_subplot(gs[1, 0])
            regional_metrics = self.df.groupby('State').agg({
                'Sales': ['sum', 'mean', 'count']
            }).round(2)
            
            bars = sns.barplot(
                x=regional_metrics.index,
                y=regional_metrics[('Sales', 'sum')],
                ax=ax2
            )
            
            # Add value labels
            for i, bar in enumerate(bars.patches):
                transactions = regional_metrics.iloc[i][('Sales', 'count')]
                avg_sale = regional_metrics.iloc[i][('Sales', 'mean')]
                
                ax2.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}\n'
                    f'({transactions:,} trans)\n'
                    f'(Avg: ${avg_sale:,.0f})',
                    ha='center', va='bottom'
                )
            
            add_annotations(
                ax=ax2,
                title='Regional Performance Analysis',
                xlabel='State',
                ylabel='Total Revenue (AUD)'
            )
            
            # 3. Segment Analysis (Middle Right)
            ax3 = fig.add_subplot(gs[1, 1])
            segment_metrics = self.df.groupby('Group').agg({
                'Sales': ['sum', 'mean', 'count', 'std']
            }).round(2)
            
            bars = sns.barplot(
                x=segment_metrics.index,
                y=segment_metrics[('Sales', 'sum')],
                ax=ax3
            )
            
            # Add value labels
            for i, bar in enumerate(bars.patches):
                transactions = segment_metrics.iloc[i][('Sales', 'count')]
                std_dev = segment_metrics.iloc[i][('Sales', 'std')]
                
                ax3.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height(),
                    f'${bar.get_height():,.0f}\n'
                    f'({transactions:,} trans)\n'
                    f'(±${std_dev:,.0f})',
                    ha='center', va='bottom'
                )
            
            add_annotations(
                ax=ax3,
                title='Segment Performance Analysis',
                xlabel='Customer Segment',
                ylabel='Total Revenue (AUD)'
            )
            
            # 4. Daily Pattern (Bottom Left)
            ax4 = fig.add_subplot(gs[2, 0])
            hourly_metrics = self.df.groupby('Hour').agg({
                'Sales': ['mean', 'std', 'count']
            }).round(2)
            
            # Plot mean sales
            line1 = ax4.plot(
                hourly_metrics.index,
                hourly_metrics[('Sales', 'mean')],
                marker='o',
                label='Average Sales'
            )[0]
            
            # Add confidence interval
            ax4.fill_between(
                hourly_metrics.index,
                hourly_metrics[('Sales', 'mean')] - hourly_metrics[('Sales', 'std')],
                hourly_metrics[('Sales', 'mean')] + hourly_metrics[('Sales', 'std')],
                alpha=0.2,
                label='±1 Std Dev'
            )
            
            # Add transaction count
            ax4_twin = ax4.twinx()
            line2 = ax4_twin.plot(
                hourly_metrics.index,
                hourly_metrics[('Sales', 'count')],
                color='red',
                linestyle='--',
                label='Transactions'
            )[0]
            
            # Combine legends
            ax4.legend(handles=[line1, line2], loc='upper right')
            
            add_annotations(
                ax=ax4,
                title='Daily Sales Pattern',
                xlabel='Hour of Day',
                ylabel='Average Sales (AUD)'
            )
            ax4_twin.set_ylabel('Number of Transactions')
            
            # 5. Distribution Analysis (Bottom Right)
            ax5 = fig.add_subplot(gs[2, 1])
            sns.boxplot(
                data=self.df,
                x='Group',
                y='Sales',
                ax=ax5
            )
            
            # Add statistical annotations
            stats = self.df.groupby('Group')['Sales'].agg(['mean', 'median', 'std']).round(2)
            for i, group in enumerate(stats.index):
                stats_text = (
                    f'Mean: ${stats.loc[group, "mean"]:,.0f}\n'
                    f'Median: ${stats.loc[group, "median"]:,.0f}\n'
                    f'Std: ${stats.loc[group, "std"]:,.0f}'
                )
                ax5.text(
                    i,
                    self.df['Sales'].max(),
                    stats_text,
                    ha='center',
                    va='bottom'
                )
            
            add_annotations(
                ax=ax5,
                title='Sales Distribution by Segment',
                xlabel='Customer Segment',
                ylabel='Sales (AUD)'
            )
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating dashboard: {str(e)}")
            raise
    
    def create_interactive_dashboard(self) -> None:
        """Create interactive dashboard using plotly."""
        try:
            # 1. Sales Trend
            daily_trend = self.df.groupby('Date').agg({
                'Sales': ['sum', 'count']
            }).reset_index()
            
            fig1 = px.line(
                daily_trend,
                x='Date',
                y=[('Sales', 'sum'), ('Sales', 'count')],
                title='Daily Revenue and Transaction Trends',
                labels={
                    'Date': 'Date',
                    'value': 'Value',
                    'variable': 'Metric'
                }
            )
            fig1.show()
            
            # 2. Regional and Segment Analysis
            performance_metrics = self.df.groupby(['State', 'Group']).agg({
                'Sales': ['sum', 'mean', 'count']
            }).round(2).reset_index()
            
            fig2 = px.sunburst(
                performance_metrics,
                path=['State', 'Group'],
                values=('Sales', 'sum'),
                title='Hierarchical Revenue Analysis'
            )
            fig2.show()
            
            # 3. Time Pattern Analysis
            time_patterns = pd.pivot_table(
                data=self.df,
                values='Sales',
                index='DayOfWeek',
                columns='Hour',
                aggfunc='mean'
            ).round(0)
            
            fig3 = px.imshow(
                time_patterns,
                title='Weekly Business Pattern Analysis',
                labels={
                    'x': 'Hour of Day',
                    'y': 'Day of Week',
                    'color': 'Average Sales (AUD)'
                }
            )
            fig3.show()
            
        except Exception as e:
            print(f"Error creating interactive dashboard: {str(e)}")
            raise

# Create dashboard object
dashboard = SalesDashboard(df)

# Generate and display static dashboard
fig = dashboard.create_static_dashboard()
plt.show()

# Save dashboard
save_plot(fig, 'sales_dashboard.png', dpi=300)

# Generate interactive dashboard
dashboard.create_interactive_dashboard()
```

### Analysis Learning Notes

```python
# Complete analysis dashboard
fig = plt.figure(figsize=(20, 15))  # Full view
gs = fig.add_gridspec(3, 2)         # Layout grid

# Sales trend (top panel)
ax1 = fig.add_subplot(gs[0, :])
daily_trend = df.groupby('Date')['Sales'].sum()
ax1.plot(daily_trend.index, daily_trend.values)
ax1.set_title('Revenue Trend Analysis')
ax1.tick_params(axis='x', rotation=45)

# Regional view (middle left)
ax2 = fig.add_subplot(gs[1, 0])
state_revenue = df.groupby('State')['Sales'].sum()
sns.barplot(
    x=state_revenue.index,
    y=state_revenue.values,
    ax=ax2
)
ax2.set_title('Regional Performance')
ax2.tick_params(axis='x', rotation=45)

# Segment view (middle right)
ax3 = fig.add_subplot(gs[1, 1])
group_revenue = df.groupby('Group')['Sales'].sum()
sns.barplot(
    x=group_revenue.index,
    y=group_revenue.values,
    ax=ax3
)
ax3.set_title('Segment Analysis')

# Daily pattern (bottom left)
ax4 = fig.add_subplot(gs[2, 0])
hourly_pattern = df.groupby('Hour')['Sales'].mean()
ax4.plot(
    hourly_pattern.index,
    hourly_pattern.values,
    marker='o'
)
ax4.set_title('Daily Business Pattern')
ax4.grid(True)

# Distribution study (bottom right)
ax5 = fig.add_subplot(gs[2, 1])
sns.boxplot(
    data=df,
    x='Group',
    y='Sales',
    ax=ax5
)
ax5.set_title('Segment Distribution')

plt.tight_layout()
plt.show()
```

### Interactive Analysis (Additional Practice)

```python
# Time series study
fig = px.line(
    df.groupby('Date')['Sales'].sum().reset_index(),
    x='Date',
    y='Sales',
    title='Dynamic Revenue Trend'
)
fig.update_layout(
    xaxis_title="Date Range",
    yaxis_title="Daily Revenue (AUD)",
    hovermode='x unified'  # Better tooltips
)
fig.show()

# Regional segment analysis
fig = px.bar(
    df.groupby(['State', 'Group'])['Sales'].sum().reset_index(),
    x='State',
    y='Sales',
    color='Group',
    title='Regional Segment Performance'
)
fig.update_layout(
    xaxis_title="State Market",
    yaxis_title="Revenue (AUD)",
    barmode='group'     # Grouped view
)
fig.show()
```

### Visualization Learning Notes

```markdown
## Key Insights from Visualization

### 1. Regional Patterns Learned
- Market distribution shape
- Segment preferences by region
- Performance variations study

### 2. Customer Insights Gained
- Segment revenue patterns
- Distribution characteristics
- Cross-segment learning

### 3. Time Pattern Understanding
- Peak hour identification
- Weekly cycle analysis
- Business timing study

### 4. Business Strategy Notes
✓ Resource optimization
✓ Marketing targeting
✓ Operational planning
```

### Study Questions
1. Why use different plot types?
   - Distribution understanding
   - Pattern recognition
   - Trend analysis

2. Color scheme importance:
   - Data representation
   - Visual hierarchy
   - Accessibility

3. Layout considerations:
   - Information flow
   - Visual balance
   - Story telling

### Next Steps
1. Refine visualizations
2. Add interactivity
3. Prepare presentation
4. Document insights
- Operational optimization opportunities
```
