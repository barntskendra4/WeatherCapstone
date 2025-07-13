# WeatherCap - Weather Dashboard

Welcome to WeatherCap! A comprehensive weather dashboard application with an intuitive tkinter GUI interface that helps you track, compare, and visualize weather information.

## 🌤️ Features

### Core Features
- **Real-time Weather Data** - Get current weather information for any city worldwide
- **5-Day Weather Forecasts** - Detailed weather predictions with daily highs/lows and hourly details
- **Weather Trend Analysis** - Comprehensive insights combining current conditions and forecasts
- **City Comparison** - Compare weather between multiple cities side-by-side with detailed analysis
- **Theme Switcher** - Toggle between dark/light mode with custom color schemes
- **Weather History** - Track and view historical weather data
- **User Preferences** - Save your favorite settings and default cities

### GUI Interface
- **Modern CustomTkinter Interface** - Clean, professional design with modern styling
- **Responsive Layout** - Adapts to different window sizes with side-by-side content
- **Status Updates** - Real-time feedback on operations
- **Tabbed Navigation** - Easy access to different features
- **Theme Support** - Built-in dark/light mode with custom red theme
- **Enhanced UX** - Professional appearance with better visual hierarchy

## 📁 Project Structure

```
WeatherCap/
├── main.py                    # Entry point - tkinter GUI application
├── config.py                  # Configuration settings and API setup
├── .env                       # Environment variables (API key)
├── requirements.txt           # Python dependencies
├── core/                      # Core functionality
│   ├── weather_api.py         # Weather API interface
│   └── data_manager.py        # Data management utilities
├── features/                  # Feature modules
│   ├── city_comparison.py     # Feature 1: Compare multiple cities
│   ├── theme_switcher.py      # Feature 2: Dark/light mode themes
│   └── forecast_predict.py    # Feature 3: Weather forecasting
├── data/                      # Data storage
│   ├── weather_history.txt    # Historical weather data
│   ├── user_preferences.json  # Theme settings, favorite cities
│   ├── red.json               # Toggle custom settings
│   └── forecast_accuracy.csv  # Track prediction success rate
├── docs/                      # Documentation
│   └── Week11_Reflection.md   # Development reflection
└── screenshots/               # Images for documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))
- CustomTkinter

### Installation

1. **Navigate to the project directory**
   ```bash
   cd WeatherCap
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - The `.env` file already contains an API key
   - If you need your own key, get one from [OpenWeatherMap](https://openweathermap.org/api)
   - Update the `.env` file with your API key:
     ```
     api_key=your_actual_api_key_here
     ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🎯 Usage

### Main Interface
- **Search Bar**: Enter any city name to get current weather
- **Current Weather Display**: Shows temperature, description, and humidity
- **Tabbed Interface**: Navigate between different features

### Features Tabs
1. **City Comparison**: Compare weather between two cities with detailed analysis
2. **Forecast Analysis**: 
   - 5-day detailed weather forecasts with daily highs/lows
   - Weather trend analysis and insights
   - Hourly weather details every 6 hours
3. **Weather History**: View your recent weather searches

### Settings
- **Theme Switcher**: Toggle between light and dark themes
- **Save Preferences**: Store your preferred settings and default city

## 🎨 Interface Versions

WeatherCap comes with two interface options:

### 🔶 Standard tkinter (main.py)
- Classic tkinter interface
- All core functionality included
- Lightweight and fast
- Compatible with all Python installations

### ⭐ Enhanced CustomTkinter (main_customtkinter.py) - **Recommended**
- Modern, professional appearance
- Custom red color theme
- Better visual hierarchy and spacing
- Dark/light mode toggle
- Enhanced user experience
- All forecast functionality integrated

Both versions include the complete weather dashboard functionality including forecast predictions and city comparisons.

## 📊 Data Storage

The application stores data in simple, readable formats:
- **weather_history.txt**: Historical weather data (Date, City, Temperature, Condition)
- **user_preferences.json**: User settings and favorite cities
- **forecast_accuracy.csv**: Prediction success tracking

## 🛠️ Development

### Architecture
The application follows a modular design:
- **main.py**: GUI setup and event handling
- **config.py**: API management and configuration
- **features/**: Independent feature modules
- **data/**: File-based data persistence

### Adding Features
1. Create a new module in the `features/` directory
2. Import and integrate in `main.py`
3. Update documentation and tests

## 📋 Requirements

See `requirements.txt` for complete dependency list:
- **customtkinter** (Modern GUI framework)
- **requests** (API calls)
- **python-dotenv** (environment variables)
- **Pillow** (Image processing for CustomTkinter)
- matplotlib (data visualization)

## 🤝 Contributing



## 📄 License

This project is created for educational purposes as part of a coding bootcamp capstone.

## 🙏 Acknowledgments

- OpenWeatherMap API for weather data
- Python community for excellent libraries
- Course instructors and fellow students for support

---

**Author**: Kendra Barnts  
**GitHub**: [@barntskendra4](https://github.com/barntskendra4)  
**Project Type**: Data, Visual, & Interactive Dashboard