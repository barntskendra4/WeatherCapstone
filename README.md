# WeatherCap - Weather Dashboard

A modern, comprehensive weather dashboard application built with Python and CustomTkinter. WeatherCap provides real-time weather information with an intuitive interface, featuring city comparisons, forecasts, and customizable themes.

## Screenshot

<!-- add a screenshot of the application here -->

## 🌤️ Features

### Core Features
- **Real-time Weather Data** - Get current weather information for any city worldwide with robust state validation
- **5-Day Weather Forecasts** - Detailed weather predictions with comprehensive daily forecasts
- **City Comparison** - Compare weather between multiple cities side-by-side with detailed analysis
- **Smart State Validation** - Intelligent handling of US states with abbreviations, full names, and error suggestions
- **Theme Management** - Toggle between dark/light mode with persistent preferences
- **Weather History** - Track and view your recent weather searches with statistics
- **User Preferences** - Save your favorite settings, default cities, and theme preferences

### Technical Features
- **Modular Architecture** - Clean separation of concerns with organized codebase
- **Error Handling** - Comprehensive input validation and user-friendly error messages  
- **Data Persistence** - JSON-based settings and history storage
- **Responsive Design** - Modern interface that adapts to different window sizes
- **Status Feedback** - Real-time updates on all operations

## 📁 Project Architecture

WeatherCap follows a clean, modular architecture with separation of concerns:

```
WeatherCap/
├── main.py                    # Application entry point
├── app_controller.py          # Main application controller
├── config.py                  # Configuration and API settings
├── .env                       # Environment variables (API key)
├── requirements.txt           # Python dependencies
├── ARCHITECTURE.md            # Detailed architecture documentation
├── ui/                        # User Interface Layer
│   ├── gui_components.py      # UI widget creation and layout
│   └── event_handlers.py      # User interaction handling
├── utils/                     # Utility Modules
│   ├── preferences_manager.py # User preferences management
│   └── theme_manager.py       # Theme switching logic
├── features/                  # Feature Modules
│   ├── city_comparison.py     # City weather comparison
│   ├── forecast_predict.py    # Weather forecasting (5-day)
│   └── theme_switcher.py      # Theme management interface
├── core/                      # Core Business Logic
│   └── weather_api.py         # Weather API communication
└── data/                      # Data Storage
    ├── weather_history.txt    # Historical weather searches
    ├── user_preferences.json  # User settings and preferences
    ├── purple_theme.json      # Theme configuration files
    └── red.json               # Custom theme settings
```

### Architecture Highlights
- **Separation of Concerns**: UI, business logic, and data management are cleanly separated
- **Modular Design**: Each feature is self-contained and independently maintainable
- **Event-Driven Architecture**: Clean separation between UI events and business logic
- **Data Persistence**: JSON-based storage for preferences and history

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))
- Internet connection for weather data

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/barntskendra4/WeatherCapstone.git
   cd WeatherCap
   ```

2. **Set up virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Create a `.env` file in the project root:
     ```
     API_KEY=your_actual_api_key_here
     ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 🎯 Usage

### Main Dashboard
- **Search Interface**: Enter city name and optional state for accurate results
- **Smart State Validation**: Handles US states as abbreviations (FL, CA, TX) or full names (Florida, California, Texas)
- **Current Weather Display**: Real-time temperature, conditions, and humidity
- **Theme Toggle**: Switch between light and dark modes with persistent preferences

### Feature Tabs

#### 🏙️ City Comparison
- Compare weather conditions between two cities simultaneously
- Side-by-side input layout with intuitive VS design
- Detailed comparison including temperature differences, humidity, and conditions
- Optional state specification for cities with common names

#### 📅 Weather Forecast  
- **5-Day Forecast**: Comprehensive daily weather predictions
- Temperature highs and lows for each day
- Detailed conditions and weather descriptions
- Easy-to-read format with date and day information

#### 📊 Weather History
- **Recent Searches**: View your last weather lookups
- **Statistics**: Summary of your weather search patterns
- Persistent history tracking across sessions

#### ⚙️ Settings & Preferences
- **Save Settings**: Store your theme and default city preferences
- **Application Info**: Version details and feature overview
- Settings persist across application restarts

### Smart Features
- **Error Handling**: Helpful suggestions for invalid state names
- **Input Validation**: Real-time feedback on search inputs  
- **Status Updates**: Clear feedback on all operations
- **Data Persistence**: All preferences and history automatically saved

## 🎨 User Interface

WeatherCap features a modern, professional interface built with CustomTkinter:

### Design Highlights
- **Modern CustomTkinter Framework** - Clean, contemporary styling with professional appearance
- **Responsive Layout** - Side-by-side main content with adaptable sizing
- **Dark/Light Theme Support** - Complete theme switching with user preference persistence
- **Intuitive Navigation** - Tabbed interface for easy access to all features
- **Visual Feedback** - Real-time status updates and clear error messaging
- **Professional Typography** - Consistent font hierarchy for optimal readability

### Interface Organization
- **Header Section** - Application title with theme toggle controls
- **Search Section** - Primary weather lookup with city and state inputs
- **Main Content Area** - Split layout with weather display and feature tabs
- **Status Bar** - Real-time operation feedback and system status

## � Data Management

The application uses JSON-based storage for persistence and reliability:

### Storage Files
- **user_preferences.json** - Theme settings, default city, and user configurations
- **weather_history.txt** - Historical weather search data with timestamps  
- **Theme Configuration** - Custom color schemes and appearance settings

### Data Features
- **Automatic Persistence** - All settings and history saved automatically
- **Error Recovery** - Graceful handling of corrupted data files
- **Human-Readable Format** - Easy to backup and transfer user data
- **Privacy-Focused** - All data stored locally, no external data collection

## 🛠️ Development & Architecture

### Code Organization
WeatherCap follows modern software engineering principles:

- **Modular Architecture** - Clear separation between UI, business logic, and data layers
- **Single Responsibility** - Each module has a focused, well-defined purpose  
- **Event-Driven Design** - Clean separation between user interactions and business logic
- **Error Handling** - Comprehensive input validation and graceful error recovery
- **Data Persistence** - Reliable storage with automatic backup and recovery

### Key Components
- **app_controller.py** - Central application coordinator and state management
- **ui/gui_components.py** - Pure UI widget creation and layout logic
- **ui/event_handlers.py** - User interaction processing and event routing
- **utils/preferences_manager.py** - Settings persistence and configuration management
- **features/** - Self-contained feature modules for extensibility

### Development Standards
- **Type Safety** - Consistent parameter validation and error handling
- **Documentation** - Comprehensive code comments and architectural documentation
- **Testing** - API testing and error handling validation
- **Version Control** - Git-based development with clean commit history

## 📋 Dependencies

Core requirements (see `requirements.txt` for complete list):
- **customtkinter>=5.0.0** - Modern GUI framework for professional appearance
- **requests>=2.25.0** - HTTP library for weather API communication  
- **python-dotenv>=0.19.0** - Environment variable management for secure API keys
- **Pillow>=8.0.0** - Image processing support for CustomTkinter themes

## 🚀 Features in Detail

### State Validation System
- **Comprehensive Coverage** - Supports all 50 US states plus territories
- **Multiple Formats** - Accepts abbreviations (FL, CA, TX) and full names
- **Smart Suggestions** - Provides helpful corrections for invalid inputs
- **Alias Support** - Handles common alternative names for states

### Weather API Integration  
- **OpenWeatherMap API** - Reliable, professional weather data source
- **Rate Limiting** - Efficient API usage with built-in request management
- **Error Handling** - Graceful handling of network issues and API limits
- **Data Formatting** - Clean, user-friendly presentation of weather information

### Theme Management
- **Dynamic Switching** - Real-time theme changes without restart
- **Preference Persistence** - Theme choice saved across sessions
- **Custom Color Schemes** - Professional color palettes for both themes
- **UI Consistency** - All components properly themed and coordinated

## 🤝 Contributing

WeatherCap is designed with extensibility in mind. To contribute:

1. **Fork the repository** and create a feature branch
2. **Follow the modular architecture** - add new features in the `features/` directory
3. **Maintain separation of concerns** - keep UI, business logic, and data management separate
4. **Test thoroughly** - ensure all features work with both light and dark themes
5. **Update documentation** - include README updates and code comments
6. **Submit a pull request** with a clear description of your changes

### Development Guidelines
- Follow existing code style and naming conventions
- Add comprehensive error handling for new features
- Ensure theme compatibility for all UI components
- Test with various city/state combinations
- Update requirements.txt if adding new dependencies

## 🔧 Troubleshooting

### Common Issues
- **API Key Issues** - Ensure your `.env` file contains a valid OpenWeatherMap API key
- **Network Connectivity** - Check internet connection for weather data retrieval
- **State Validation** - Use standard state abbreviations (FL, CA, TX) or full names
- **Theme Problems** - Try toggling themes or restarting the application

### Getting Help
- Check the `ARCHITECTURE.md` file for detailed technical documentation
- Review error messages for specific guidance on input formatting
- Ensure all dependencies are installed correctly via `pip install -r requirements.txt`

## 📄 License

This project is open source and available under the MIT License. Created as part of a coding bootcamp capstone project to demonstrate full-stack development skills.

## 🙏 Acknowledgments

- **OpenWeatherMap** - Reliable weather data API service
- **CustomTkinter Community** - Modern Python GUI framework and documentation
- **Python Community** - Excellent libraries and development tools
- **Course Instructors** - Guidance and support throughout development
- **Fellow Students** - Collaboration and code review feedback

---

## 📊 Project Stats

- **Language**: Python 3.8+
- **Framework**: CustomTkinter GUI
- **Architecture**: Modular with separation of concerns  
- **Testing**: API integration and error handling validation
- **Storage**: JSON-based persistence with local data management
- **API**: OpenWeatherMap REST API integration

**Author**: Kendra Barnts  
**GitHub**: [@barntskendra4](https://github.com/barntskendra4)  
**Repository**: [WeatherCapstone](https://github.com/barntskendra4/WeatherCapstone)  
**Project Type**: Data, Visual, & Interactive Dashboard Application