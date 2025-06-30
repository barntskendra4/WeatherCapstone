# Weather Dashboard

Welcome to your Weather Dashboard project! This application helps you track, compare, and visualize weather information with an intuitive GUI interface.

## 🌤️ Features

### Core Features
- **City Comparison** - Compare weather between multiple cities side-by-side
- **Theme Switcher** - Toggle between dark/light mode with custom color schemes
- **Tomorrow's Guess** - Predict tomorrow's weather and track accuracy over time

### Enhancement
- **Creative Visuals** - Weather icons, temperature graphs, and visual data representations using matplotlib

## 📁 Project Structure

```
weather-dashboard-kendra/
├── main.py                    # Entry point - GUI setup & main loop
├── config.py                  # API keys, WeatherAPI class, settings
├── .env                       # Environment variables (API key)
├── requirements.txt           # Python dependencies
├── features/                  # Feature modules
│   ├── city_comparison.py     # Feature 1: Compare multiple cities
│   ├── theme_switcher.py      # Feature 2: Dark/light mode
│   └── forecast_prediction.py # Feature 3: Tomorrow's weather guess
├── data/                      # Data storage
│   ├── weather_history.txt    # Historical weather data
│   ├── user_preferences.json  # Theme settings, favorite cities
│   └── forecast_accuracy.csv  # Track prediction success rate
├── docs/                      # Documentation
│   ├── README.md              # Project overview & setup
│   └── user_guide.md          # How to use the application
└── screenshots/               # Images for documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/barntskendra4/weather-dashboard-kendra.git
   cd weather-dashboard-kendra
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Create a `.env` file in the root directory
   - Add your OpenWeatherMap API key:
     ```
     api_key=your_actual_api_key_here
     ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🎯 Usage

1. **Basic Weather Lookup**: Enter a city name to get current weather conditions
2. **City Comparison**: Use the comparison feature to view multiple cities at once
3. **Theme Selection**: Switch between light and dark modes in settings
4. **Weather Predictions**: View tomorrow's forecast and track prediction accuracy

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
- tkinter (GUI framework)
- requests (API calls)
- python-dotenv (environment variables)
- matplotlib (data visualization)

## 🤝 Contributing

This is a capstone project for educational purposes. For questions or suggestions, please reach out through the course channels.

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