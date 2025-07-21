"""
Bike-Sharing Data Analysis Dashboard
Optimized for Data Analyst role
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import st_folium
from scipy import stats
from scipy.stats import probplot, shapiro
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Bike-Sharing Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for monochromatic white/black theme
st.markdown("""
<style>
    /* Main theme colors - Monochromatic white/black */
    :root {
        --primary-color: #ffffff;
        --secondary-color: #f5f5f5;
        --background-dark: #1a1a1a;
        --background-light: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #e0e0e0;
        --border-color: #404040;
        --accent-color: #ffffff;
        --success-color: #ffffff;
        --warning-color: #ffffff;
        --error-color: #ffffff;
        --hover-color: #3a3a3a;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .metric-card {
        background: var(--background-light);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        background: var(--hover-color);
    }
    
    .analysis-section {
        background: var(--background-light);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        color: var(--text-primary);
    }
    
    .insight-box {
        background: var(--background-dark);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    .insight-box:hover {
        border-left-color: var(--text-secondary);
        transform: translateX(4px);
        background: var(--hover-color);
    }
    
    /* Button styling - Monochromatic */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background-color: var(--primary-color);
        color: var(--background-dark);
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:hover {
        background-color: var(--text-secondary);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        background-color: var(--background-dark);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
        background-color: var(--hover-color);
    }
    
    /* Slider styling */
    .stSlider > div > div {
        border-radius: 8px;
    }
    
    .stSlider > div > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--background-dark);
        color: var(--text-primary);
    }
    
    /* Tabs styling - Monochromatic */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--background-dark);
        border-bottom: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--background-light);
        border-radius: 8px 8px 0 0;
        padding: 12px 20px;
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--hover-color);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: var(--background-dark);
        border-color: var(--primary-color);
    }
    
    /* Metrics styling */
    .stMetric {
        background-color: var(--background-light);
        color: var(--text-primary);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid var(--border-color);
    }
    
    /* Plotly charts styling */
    .stPlotlyChart {
        background-color: var(--background-light);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    /* Text styling */
    .stMarkdown {
        color: var(--text-primary);
    }
    
    .stSubheader {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .stHeader {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .stTitle {
        color: var(--primary-color);
        font-weight: 700;
    }
    
    .stText {
        color: var(--text-primary);
    }
    
    .stWrite {
        color: var(--text-primary);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: var(--background-light);
        color: var(--text-primary);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    /* Form elements styling */
    .stSelectbox label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stMultiselect label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stSlider label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stCheckbox label {
        color: var(--text-primary);
    }
    
    .stRadio label {
        color: var(--text-primary);
    }
    
    .stNumberInput label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stTextInput label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stTextArea label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stDateInput label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stTimeInput label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stFileUploader label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .stColorPicker label {
        color: var(--text-primary);
        font-weight: 500;
    }
    
    /* Progress and loading elements */
    .stProgress {
        background-color: var(--background-dark);
    }
    
    .stProgress > div > div {
        background-color: var(--primary-color);
    }
    
    .stSpinner {
        color: var(--primary-color);
    }
    
    /* Status messages */
    .stSuccess {
        background-color: var(--background-light);
        color: var(--success-color);
        border: 1px solid var(--success-color);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: var(--background-light);
        color: var(--error-color);
        border: 1px solid var(--error-color);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: var(--background-light);
        color: var(--warning-color);
        border: 1px solid var(--warning-color);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stInfo {
        background-color: var(--background-light);
        color: var(--primary-color);
        border: 1px solid var(--primary-color);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }
    
    /* Focus states */
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
    }
    
    .stMultiselect > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class BikeSharingAnalysis:
    def __init__(self):
        self.data_path = "data/"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        # This method is no longer needed as data loading is handled directly in run()
        pass
        
    def load_data(self):
        """Load and cache data efficiently"""
        @st.cache_data
        def load_csv_data():
            try:
                df = pd.read_csv("201902-fordgobike-tripdata.csv")
                return self.process_data(df)
            except FileNotFoundError:
                st.error("""
                **Data file not found!**
                
                Please ensure `201902-fordgobike-tripdata.csv` is in the project root directory.
                
                **Download the data:**
                1. Visit: https://www.fordgobike.com/system-data
                2. Download the February 2019 dataset
                3. Place the CSV file in the project root
                """)
                return None
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                return None
        
        return load_csv_data()
    
    def process_data(self, df):
        """Process and clean data efficiently"""
        # Convert time columns
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        
        # Create essential features
        df['duration_min'] = df['duration_sec'] / 60
        df['start_hour'] = df['start_time'].dt.hour
        df['day_of_week'] = df['start_time'].dt.day_name()
        df['month'] = df['start_time'].dt.month
        df['date'] = df['start_time'].dt.date
        
        # Time of day categorization
        df['time_of_day'] = pd.cut(
            df['start_hour'], 
            bins=[0, 6, 12, 18, 24], 
            labels=['Night', 'Morning', 'Afternoon', 'Evening']
        )
        
        # User age (if available)
        if 'member_birth_year' in df.columns:
            df['user_age'] = 2019 - df['member_birth_year']
            df['user_age'] = df['user_age'].clip(0, 100)  # Remove outliers
        
        # Trip distance estimation (simplified)
        df['trip_distance_km'] = df['duration_min'] * 0.3
        
        return df
        
    def run(self):
        """Main application runner"""
        
        # Header
        st.markdown('<h1 class="main-header">Bike-Sharing Data Analysis</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Comprehensive Data Analysis Project | February 2019 Dataset</p>', unsafe_allow_html=True)
        
        # Load data
        df = self.load_data()
        if df is None:
            st.stop()
        
        # Sidebar
        filters = self.create_sidebar(df)
        
        # Filter data based on sidebar selections
        filtered_df = self.filter_data(df, filters)
        
        # Main content
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "Executive Summary", 
            "Data Exploration", 
            "Business Insights", 
            "Geographic Analysis",
            "Trends & Patterns",
            "Statistical Analysis",
            "Data Quality",
            "KPI Dashboard"
        ])
        
        with tab1:
            self.executive_summary(filtered_df)
        
        with tab2:
            self.data_exploration(filtered_df)
            
        with tab3:
            self.business_insights(filtered_df)
            
        with tab4:
            self.geographic_analysis(filtered_df)
            
        with tab5:
            self.trends_patterns(filtered_df)
            
        with tab6:
            self.statistical_analysis(filtered_df)
            
        with tab7:
            self.data_quality_dashboard(df)
            
        with tab8:
            self.kpi_dashboard(filtered_df)
    
    def create_sidebar(self, df):
        """Create optimized sidebar with essential filters"""
        st.sidebar.title("Data Filters")
        
        # Essential filters only
        st.sidebar.subheader("User Type")
        user_types = st.sidebar.multiselect(
            "Select user types",
            df['user_type'].unique().tolist(),
            default=df['user_type'].unique().tolist()
        )
        
        st.sidebar.subheader("Trip Duration (minutes)")
        min_duration = st.sidebar.slider("Min duration", 0, 60, 0)
        max_duration = st.sidebar.slider("Max duration", 0, 120, 120)
        
        st.sidebar.subheader("Day of Week")
        days = st.sidebar.multiselect(
            "Select days",
            df['day_of_week'].unique().tolist(),
            default=df['day_of_week'].unique().tolist()
        )
        
        return {
            "user_types": user_types,
            "min_duration": min_duration,
            "max_duration": max_duration,
            "days": days
        }
    
    def filter_data(self, df, filters):
        """Filter data based on sidebar selections"""
        filtered_df = df.copy()
        
        # Filter by user type
        if filters["user_types"]:
            filtered_df = filtered_df[filtered_df['user_type'].isin(filters["user_types"])]
        
        # Filter by duration
        filtered_df = filtered_df[
            (filtered_df['duration_min'] >= filters["min_duration"]) & 
            (filtered_df['duration_min'] <= filters["max_duration"])
        ]
        
        # Filter by day of week
        if filters["days"]:
            filtered_df = filtered_df[filtered_df['day_of_week'].isin(filters["days"])]
        
        return filtered_df
    
    def executive_summary(self, df):
        """Optimized executive summary with key metrics"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Executive Summary")
        
        # Key metrics in a clean layout
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Trips", f"{len(df):,}")
        
        with col2:
            st.metric("Avg Duration", f"{df['duration_min'].mean():.1f} min")
        
        with col3:
            st.metric("Subscriber Rate", f"{(df['user_type'] == 'Subscriber').mean() * 100:.1f}%")
        
        with col4:
            peak_hour = df.groupby('start_hour').size().idxmax()
            st.metric("Peak Hour", f"{peak_hour}:00")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key insights
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**Peak Usage Patterns**")
            st.write(f"- Peak hours: {peak_hour}:00 and {(peak_hour + 12) % 24}:00")
            st.write(f"- Weekday usage: {len(df[~df['day_of_week'].isin(['Saturday', 'Sunday'])]) / len(df) * 100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**User Behavior**")
            st.write(f"- Subscribers: {(df['user_type'] == 'Subscriber').sum():,}")
            st.write(f"- Customers: {(df['user_type'] == 'Customer').sum():,}")
            st.write(f"- Avg trip distance: {df['trip_distance_km'].mean():.1f} km")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def data_exploration(self, df):
        """Optimized data exploration with essential visualizations"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Data Exploration")
        
        # Dataset overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Dataset Overview:**")
            st.write(f"- Total records: {len(df):,}")
            st.write(f"- Date range: {df['start_time'].min().strftime('%Y-%m-%d')} to {df['start_time'].max().strftime('%Y-%m-%d')}")
            st.write(f"- Missing values: {df.isnull().sum().sum():,}")
        
        with col2:
            st.write("**Statistical Summary:**")
            st.write(f"- Mean duration: {df['duration_min'].mean():.1f} minutes")
            st.write(f"- Median duration: {df['duration_min'].median():.1f} minutes")
            st.write(f"- Duration range: {df['duration_min'].min():.1f} - {df['duration_min'].max():.1f} minutes")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Essential visualizations
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Key Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Trip duration distribution
            fig = px.histogram(
                df, 
                x='duration_min', 
                nbins=30,
                title="Trip Duration Distribution",
                labels={'duration_min': 'Duration (minutes)', 'count': 'Number of Trips'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # User type distribution
            user_counts = df['user_type'].value_counts()
            fig = px.pie(
                values=user_counts.values, 
                names=user_counts.index,
                title="User Type Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Hourly usage pattern
        hourly_usage = df.groupby('start_hour').size()
        fig = px.line(
            x=hourly_usage.index, 
            y=hourly_usage.values,
            title="Hourly Usage Pattern",
            labels={'x': 'Hour of Day', 'y': 'Number of Trips'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def business_insights(self, df):
        """Optimized business insights with key metrics"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Business Insights")
        
        # Key business metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_trips = len(df)
            estimated_revenue = total_trips * 3.50
            st.metric("Estimated Revenue", f"${estimated_revenue:,.0f}")
        
        with col2:
            avg_daily_trips = df.groupby('date').size().mean()
            st.metric("Average Daily Trips", f"{avg_daily_trips:.0f}")
        
        with col3:
            subscriber_rate = (df['user_type'] == 'Subscriber').mean() * 100
            st.metric("Subscriber Rate", f"{subscriber_rate:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key recommendations
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Business Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**Peak Hour Optimization**")
            st.write("- Increase bike availability during 8-9 AM and 5-6 PM")
            st.write("- Consider dynamic pricing during peak hours")
            st.write("- Optimize station rebalancing schedules")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**User Conversion Strategy**")
            st.write("- Target casual users with subscription promotions")
            st.write("- Offer weekend packages to increase usage")
            st.write("- Implement loyalty programs for frequent users")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def geographic_analysis(self, df):
        """Optimized geographic analysis with essential insights"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Geographic Analysis")
        
        # Station performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top Starting Stations:**")
            top_start = df['start_station_name'].value_counts().head(5)
            for station, count in top_start.items():
                st.write(f"- {station}: {count:,} trips")
        
        with col2:
            st.write("**Top Ending Stations:**")
            top_end = df['end_station_name'].value_counts().head(5)
            for station, count in top_end.items():
                st.write(f"- {station}: {count:,} trips")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Simple map (if coordinates available)
        if 'start_station_latitude' in df.columns and 'start_station_longitude' in df.columns:
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            st.subheader("Station Map")
            
            # Create a simple map with top stations
            top_stations = df['start_station_name'].value_counts().head(10)
            station_coords = df[df['start_station_name'].isin(top_stations.index)].groupby('start_station_name').agg({
                'start_station_latitude': 'first',
                'start_station_longitude': 'first'
            }).reset_index()
            
            if not station_coords.empty:
                m = folium.Map(
                    location=[station_coords['start_station_latitude'].mean(), 
                             station_coords['start_station_longitude'].mean()],
                    zoom_start=12
                )
                
                for _, row in station_coords.iterrows():
                    folium.Marker(
                        [row['start_station_latitude'], row['start_station_longitude']],
                        popup=row['start_station_name']
                    ).add_to(m)
                
                st_folium(m, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def trends_patterns(self, df):
        """Optimized trends and patterns analysis"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Trends & Patterns")
        
        # Daily trends
        daily_trends = df.groupby('date').size()
        fig = px.line(
            x=daily_trends.index, 
            y=daily_trends.values,
            title="Daily Trip Volume",
            labels={'x': 'Date', 'y': 'Number of Trips'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Day of week patterns
        col1, col2 = st.columns(2)
        
        with col1:
            day_patterns = df['day_of_week'].value_counts()
            fig = px.bar(
                x=day_patterns.index, 
                y=day_patterns.values,
                title="Trips by Day of Week",
                labels={'x': 'Day of Week', 'y': 'Number of Trips'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Hourly patterns by day type
            weekday_hours = df[~df['day_of_week'].isin(['Saturday', 'Sunday'])].groupby('start_hour').size()
            weekend_hours = df[df['day_of_week'].isin(['Saturday', 'Sunday'])].groupby('start_hour').size()
            
            fig = px.line(
                x=weekday_hours.index,
                y=weekday_hours.values,
                title="Hourly Patterns: Weekday vs Weekend",
                labels={'x': 'Hour of Day', 'y': 'Number of Trips'}
            )
            fig.add_scatter(x=weekend_hours.index, y=weekend_hours.values, name='Weekend')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def statistical_analysis(self, df):
        """Optimized statistical analysis with essential tests"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Statistical Analysis")
        
        # Analysis type selector
        analysis_type = st.selectbox(
            "Select statistical analysis",
            ["Descriptive Statistics", "Correlation Analysis", "Hypothesis Testing", "Distribution Analysis"]
        )
        
        if analysis_type == "Descriptive Statistics":
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Numerical Variables Summary")
                numeric_cols = ['duration_min', 'start_hour']
                if 'user_age' in df.columns:
                    numeric_cols.append('user_age')
                
                stats_df = df[numeric_cols].describe()
                st.dataframe(stats_df, use_container_width=True)
            
            with col2:
                st.subheader("Categorical Variables Summary")
                st.write("**User Type Distribution:**")
                user_dist = df['user_type'].value_counts()
                st.write(user_dist)
                
                st.write("**Day of Week Distribution:**")
                day_dist = df['day_of_week'].value_counts()
                st.write(day_dist)
        
        elif analysis_type == "Correlation Analysis":
            st.subheader("Correlation Analysis")
            
            # Select numerical columns for correlation
            numeric_cols = ['duration_min', 'start_hour']
            if 'user_age' in df.columns:
                numeric_cols.append('user_age')
            
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                title="Correlation Heatmap",
                color_continuous_scale='RdBu',
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("**Key Correlations:**")
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_val = corr_matrix.iloc[i, j]
                    st.write(f"- {numeric_cols[i]} vs {numeric_cols[j]}: {corr_val:.3f}")
        
        elif analysis_type == "Hypothesis Testing":
            st.subheader("Hypothesis Testing")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # T-test: Duration by user type
                subscriber_duration = df[df['user_type'] == 'Subscriber']['duration_min']
                customer_duration = df[df['user_type'] == 'Customer']['duration_min']
                
                t_stat, p_value = stats.ttest_ind(subscriber_duration, customer_duration)
                
                st.write("**T-Test: Duration by User Type**")
                st.write(f"- T-statistic: {t_stat:.3f}")
                st.write(f"- P-value: {p_value:.6f}")
                st.write(f"- Significant: {'Yes' if p_value < 0.05 else 'No'}")
            
            with col2:
                # Chi-square test: Day of week vs user type
                contingency_table = pd.crosstab(df['day_of_week'], df['user_type'])
                chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                
                st.write("**Chi-Square Test: Day vs User Type**")
                st.write(f"- Chi-square: {chi2:.3f}")
                st.write(f"- P-value: {p_value:.6f}")
                st.write(f"- Significant: {'Yes' if p_value < 0.05 else 'No'}")
        
        elif analysis_type == "Distribution Analysis":
            st.subheader("Distribution Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Duration distribution with normal curve
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.hist(df['duration_min'], bins=30, density=True, alpha=0.7, color='skyblue')
                
                # Add normal curve
                mu, sigma = df['duration_min'].mean(), df['duration_min'].std()
                x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
                ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label='Normal Distribution')
                ax.set_title('Duration Distribution vs Normal')
                ax.legend()
                st.pyplot(fig)
            
            with col2:
                # Q-Q plot
                fig, ax = plt.subplots(figsize=(8, 6))
                probplot(df['duration_min'], dist="norm", plot=ax)
                ax.set_title('Q-Q Plot: Duration vs Normal Distribution')
                st.pyplot(fig)
            
            # Normality test
            stat, p_value = shapiro(df['duration_min'])
            st.write(f"**Shapiro-Wilk Test for Normality:**")
            st.write(f"- Statistic: {stat:.3f}")
            st.write(f"- P-value: {p_value:.6f}")
            st.write(f"- Normal distribution: {'Yes' if p_value > 0.05 else 'No'}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def data_quality_dashboard(self, df):
        """Optimized data quality dashboard with essential metrics"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Data Quality Dashboard")
        
        # Data quality overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_rows = len(df)
            st.metric("Total Records", f"{total_rows:,}")
        
        with col2:
            missing_values = df.isnull().sum().sum()
            missing_percentage = (missing_values / (total_rows * len(df.columns))) * 100
            st.metric("Missing Values", f"{missing_values:,} ({missing_percentage:.1f}%)")
        
        with col3:
            duplicate_rows = df.duplicated().sum()
            duplicate_percentage = (duplicate_rows / total_rows) * 100
            st.metric("Duplicate Records", f"{duplicate_rows:,} ({duplicate_percentage:.1f}%)")
        
        with col4:
            data_completeness = 100 - missing_percentage
            st.metric("Data Completeness", f"{data_completeness:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Column-wise analysis
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Column-wise Data Quality")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Missing Values by Column:**")
            missing_by_column = df.isnull().sum()
            missing_df = pd.DataFrame({
                'Column': missing_by_column.index,
                'Missing Values': missing_by_column.values,
                'Missing Percentage': (missing_by_column.values / len(df)) * 100
            }).sort_values('Missing Percentage', ascending=False)
            
            missing_df = missing_df.astype({
                'Column': 'string',
                'Missing Values': 'int64',
                'Missing Percentage': 'float64'
            })
            
            st.dataframe(missing_df, use_container_width=True)
        
        with col2:
            st.write("**Data Types:**")
            dtype_df = pd.DataFrame({
                'Column': df.dtypes.index,
                'Data Type': df.dtypes.values.astype(str)
            })
            st.dataframe(dtype_df, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data validation
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Data Validation Checks")
        
        validation_results = []
        
        # Check for negative durations
        negative_durations = (df['duration_min'] < 0).sum()
        validation_results.append({
            'Check': 'Negative Durations',
            'Issues Found': negative_durations,
            'Status': '✅ Pass' if negative_durations == 0 else '❌ Fail'
        })
        
        # Check for extreme trips (> 3 hours)
        extreme_trips = (df['duration_min'] > 180).sum()
        validation_results.append({
            'Check': 'Extreme Trips (>3 hours)',
            'Issues Found': extreme_trips,
            'Status': '⚠️ Review' if extreme_trips > 0 else '✅ Pass'
        })
        
        # Check for future dates
        future_dates = (df['start_time'] > pd.Timestamp('2019-12-31')).sum()
        validation_results.append({
            'Check': 'Future Dates',
            'Issues Found': future_dates,
            'Status': '✅ Pass' if future_dates == 0 else '❌ Fail'
        })
        
        # Display validation results
        validation_df = pd.DataFrame(validation_results)
        validation_df = validation_df.astype({
            'Check': 'string',
            'Issues Found': 'int64',
            'Status': 'string'
        })
        st.dataframe(validation_df, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def kpi_dashboard(self, df):
        """Optimized KPI dashboard with essential metrics"""
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("KPI Dashboard")
        
        # Key Performance Indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = len(df) * 3.50
            avg_daily_revenue = total_revenue / df['date'].nunique()
            st.metric("Average Daily Revenue", f"${avg_daily_revenue:,.0f}")
        
        with col2:
            avg_trips_per_day = len(df) / df['date'].nunique()
            st.metric("Average Daily Trips", f"{avg_trips_per_day:.0f}")
        
        with col3:
            avg_duration = df['duration_min'].mean()
            st.metric("Average Trip Duration", f"{avg_duration:.1f} min")
        
        with col4:
            subscriber_rate = (df['user_type'] == 'Subscriber').mean() * 100
            st.metric("Subscriber Rate", f"{subscriber_rate:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # KPI Trends
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("KPI Trends Over Time")
        
        # Daily KPIs
        daily_kpis = df.groupby('date').agg({
            'duration_min': ['count', 'mean'],
            'user_type': lambda x: (x == 'Subscriber').mean() * 100
        }).reset_index()
        
        daily_kpis.columns = ['date', 'daily_trips', 'avg_duration', 'subscriber_rate']
        daily_kpis['daily_revenue'] = daily_kpis['daily_trips'] * 3.50
        
        # KPI trend charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                daily_kpis,
                x='date',
                y='daily_revenue',
                title="Daily Revenue Trend",
                labels={'daily_revenue': 'Revenue ($)', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                daily_kpis,
                x='date',
                y='daily_trips',
                title="Daily Trip Volume",
                labels={'daily_trips': 'Number of Trips', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Performance summary
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Performance Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Peak hour performance
            peak_hour = df.groupby('start_hour').size().idxmax()
            peak_hour_trips = df.groupby('start_hour').size().max()
            
            st.write("**Peak Hour Performance:**")
            st.write(f"- Peak Hour: {peak_hour}:00")
            st.write(f"- Peak Hour Trips: {peak_hour_trips:,}")
            st.write(f"- Peak Hour Revenue: ${peak_hour_trips * 3.50:,.0f}")
        
        with col2:
            # User type performance
            st.write("**User Type Performance:**")
            for user_type in df['user_type'].unique():
                user_data = df[df['user_type'] == user_type]
                avg_duration = user_data['duration_min'].mean()
                total_trips = len(user_data)
                revenue = total_trips * 3.50
                
                st.write(f"**{user_type}:**")
                st.write(f"- Trips: {total_trips:,}")
                st.write(f"- Avg Duration: {avg_duration:.1f} min")
                st.write(f"- Revenue: ${revenue:,.0f}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        app = BikeSharingAnalysis()
        app.run()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 