"""
WeatherCap Group Features - CSV vs Live API Comparison
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from datetime import datetime, timedelta

# Import WeatherAPI if available
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from core.weather_api import WeatherAPI
    WEATHER_API_AVAILABLE = True
except ImportError:
    WEATHER_API_AVAILABLE = False


def load_last_5_days_csv_data(csv_files):
    """Load recent CSV data - tries last 5 days first, then expands to find available data"""
    csv_data = {}
    
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"⚠️ File not found: {csv_file}")
            continue
            
        try:
            df = pd.read_csv(csv_file)
            label = os.path.basename(csv_file).replace('.csv', '')
            
            # Create DateTime column if needed
            if 'DateTime' not in df.columns and 'Date' in df.columns and 'Time' in df.columns:
                df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
            elif 'DateTime' not in df.columns and 'Date' in df.columns:
                df['DateTime'] = pd.to_datetime(df['Date'])
            
            df['DateTime'] = pd.to_datetime(df['DateTime'])
            df = df.sort_values('DateTime')
            
            # Try different time ranges to find recent data
            recent_df = None
            days_to_try = [5, 10, 15, 30, 60, 90]  # Try progressively longer periods
            
            for days in days_to_try:
                cutoff_date = datetime.now() - timedelta(days=days)
                temp_df = df[df['DateTime'] >= cutoff_date]
                
                if len(temp_df) > 0:
                    recent_df = temp_df
                    period_desc = f"last {days} days"
                    break
            
            # If no recent data found, take the most recent entries available
            if recent_df is None or len(recent_df) == 0:
                # Take the most recent 20 entries or all if less than 20
                recent_df = df.tail(min(20, len(df)))
                if len(recent_df) > 0:
                    oldest_date = recent_df['DateTime'].min().strftime('%Y-%m-%d')
                    newest_date = recent_df['DateTime'].max().strftime('%Y-%m-%d')
                    period_desc = f"available data ({oldest_date} to {newest_date})"
                else:
                    period_desc = "no data"
            
            if len(recent_df) > 0:
                csv_data[label] = {
                    'datetimes': recent_df['DateTime'].tolist(),
                    'temperatures': recent_df['Temperature_F'].tolist()
                }
                print(f"✅ {label}: {len(recent_df)} temperature points ({period_desc})")
            else:
                print(f"⚠️ {label}: No temperature data found")
                
        except Exception as e:
            print(f"❌ Error loading {csv_file}: {e}")
    
    return csv_data


def create_last_5_days_comparison(csv_files, cities, output_file="recent_csv_vs_live_comparison.png"):
    """Create comparison chart of recent CSV data vs live API data"""
    print("🌤️ Creating recent CSV vs live API comparison chart...")
    
    # Load recent CSV data 
    csv_data = load_last_5_days_csv_data(csv_files)
    
    # Get live weather data
    api_data = {}
    if WEATHER_API_AVAILABLE:
        weather_api = WeatherAPI()
        for city in cities:
            try:
                recent_data = weather_api.get_recent_weather_data(city, days=5)
                api_data[city] = {
                    'datetimes': [item['datetime'] for item in recent_data],
                    'temperatures': [item['temperature'] for item in recent_data]
                }
                print(f"✅ {city}: {len(recent_data)} live temperature points")
            except Exception as e:
                print(f"❌ Error fetching weather for {city}: {e}")
    
    if not csv_data and not api_data:
        print("❌ No data available for comparison")
        return False
    
    # Create the plot
    plt.figure(figsize=(16, 10))
    
    # Plot CSV data
    if csv_data:
        csv_colors = plt.cm.Set1(np.linspace(0, 1, len(csv_data)))
        for i, (label, data) in enumerate(csv_data.items()):
            plt.plot(data['datetimes'], data['temperatures'], 
                    marker='o', markersize=4, linewidth=2,
                    label=f"{label} (Recent CSV Data)", 
                    color=csv_colors[i], alpha=0.8)
    
    # Plot live API data
    if api_data:
        api_colors = plt.cm.Set2(np.linspace(0, 1, len(api_data)))
        for i, (city, data) in enumerate(api_data.items()):
            plt.plot(data['datetimes'], data['temperatures'], 
                    marker='s', markersize=6, linewidth=3, linestyle='--',
                    label=f"{city} (Live API)", 
                    color=api_colors[i], alpha=0.9)
    
    # Formatting
    plt.title("Recent Group CSV Data vs Live Weather API", 
             fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Date/Time", fontsize=12)
    plt.ylabel("Temperature (°F)", fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Comparison saved as: {output_file}")
    return True


if __name__ == "__main__":
    print("🌤️ WeatherCap Group Features - CSV vs Live API Comparison")
    
    csv_files = [
        'data/groupCsvs/felix.csv',
        'data/groupCsvs/kendra.csv', 
        'data/groupCsvs/ricky.csv',
        'data/groupCsvs/abil.csv'
    ]
    
    cities = ['Toronto', 'Lincoln', 'Rockland', 'Los Angeles']
    
    success = create_last_5_days_comparison(csv_files, cities)
    if success:
        print("✅ CSV vs Live API comparison completed!")
    else:
        print("❌ Comparison failed")
