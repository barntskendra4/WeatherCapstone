# WeatherCap - Weather Dashboard

A modern, comprehensive weather dashboard application built with Python and CustomTkinter. WeatherCap provides real-time weather information with an intuitive interface, featuring city comparisons, forecasts, CSV data analysis, and customizable themes.

## Screenshot

<!-- add a screenshot of the application here -->

## 🌤️ Features

### Core Features
- **Real-time Weather Data** - Get current weather information for any city worldwide with robust zip code validation
- **5-Day Weather Forecasts** - Detailed weather predictions with comprehensive daily forecasts and state input support
- **City Comparison** - Compare weather between multiple cities side-by-side with detailed analysis
- **CSV Weather History** - Advanced CSV data processing with historical weather analysis and group comparisons
- **Smart Input Validation** - Comprehensive zip code validation with intelligent error handling and suggestions
- **Theme Management** - Toggle between dark/light mode with persistent preferences
- **Group Data Analysis** - Compare recent CSV data with live API weather information
- **User Preferences** - Save your favorite settings, default cities, and theme preferences

### Advanced Features
- **CSV Group Analysis** - Process multiple CSV files from `data/groupCsvs/` directory for group weather comparisons
- **Recent Data Focus** - Smart algorithms to find and display the most recent weather data from CSV files
- **Progressive Time Range Search** - Automatically adjusts search parameters to find available data
- **Live vs Historical Comparison** - Compare CSV historical data with current live API data
- **Intelligent File Detection** - Auto-discovery and validation of CSV files in group directories

### Technical Features
- **Modular Architecture** - Clean separation of concerns with organized codebase
- **Comprehensive Error Handling** - Advanced input validation with zip code verification and user-friendly error messages  
- **Multi-format Data Persistence** - JSON-based settings and CSV historical data storage
- **Responsive Design** - Modern interface that adapts to different window sizes
- **Real-time Status Feedback** - Live updates on all operations with detailed progress indicators
- **Git Integration** - Proper line ending handling with `.gitattributes` configuration

## 📁 Project Architecture

WeatherCap follows a clean, modular architecture with separation of concerns:

```
WeatherCap/
├── main.py                    # Application entry point
├── app_controller.py          # Main application controller
├── config.py                  # Configuration and API settings
├── .env                       # Environment variables (API key)
├── requirements.txt           # Python dependencies
├── ui/                        # User Interface Layer
│   ├── gui_components.py      # UI widget creation and layout
│   └── event_handlers.py      # User interaction handling with zip code validation
├── utils/                     # Utility Modules
│   ├── preferences_manager.py # User preferences management
│   └── state_validator.py     # Input validation and error handling
├── features/                  # Feature Modules
│   ├── city_comparison.py     # City weather comparison functionality
│   ├── forecast_predict.py    # Weather forecasting (5-day) with state support
│   ├── theme_switcher.py      # Theme management interface
│   └── weather_history_csv.py # CSV data processing and analysis
├── core/                      # Core Business Logic
│   └── weather_api.py         # Weather API communication and data handling
└── data/                      # Data Storage
    ├── weather_history.csv    # Historical weather searches and data
    ├── user_preferences.json  # User settings and preferences
    ├── purple_theme.json      # Theme configuration files
    ├── red.json               # Custom theme settings
    └── groupCsvs/             # Group CSV data directory
        ├── abil.csv           # Individual weather data files
        ├── felix.csv          # Historical group weather data
        ├── kendra.csv         # CSV comparison datasets
        └── ricky.csv          # Multi-user weather tracking
```

### Architecture Highlights
- **Separation of Concerns**: UI, business logic, and data management are cleanly separated
- **Modular Design**: Each feature is self-contained and independently maintainable
- **Event-Driven Architecture**: Clean separation between UI events and business logic
- **Advanced Data Processing**: Multi-format data handling with CSV analysis and JSON persistence
- **Comprehensive Input Validation**: Zip code verification and intelligent error handling
- **Git Integration**: Proper version control with line ending normalization

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
- **Search Interface**: Enter city name with comprehensive zip code validation
- **Smart Input Validation**: Advanced zip code verification with error prevention and helpful suggestions
- **Current Weather Display**: Real-time temperature, conditions, humidity, and detailed weather information
- **Theme Toggle**: Switch between light and dark modes with persistent preferences and immediate application

### Feature Tabs

#### 🏙️ City Comparison
- Compare weather conditions between two cities simultaneously
- Side-by-side input layout with intuitive VS design and responsive interface
- Detailed comparison including temperature differences, humidity, and comprehensive weather conditions
- Advanced input validation for both city names and zip codes

#### 📅 Weather Forecast  
- **5-Day Forecast**: Comprehensive daily weather predictions with detailed information
- **State Input Support**: Proper handling of US states with improved API query formatting
- Temperature highs and lows for each day with accurate forecasting
- Detailed conditions and weather descriptions with easy-to-read formatting
- Enhanced error handling for invalid locations and API responses

#### 📊 CSV Weather Analysis
- **Historical Data Processing**: Advanced CSV file analysis from `data/groupCsvs/` directory
- **Recent Data Focus**: Smart algorithms to automatically find and display the most recent weather data
- **Group Comparisons**: Multi-file CSV processing for comprehensive weather analysis
- **Live vs Historical**: Compare CSV historical data with current live API weather information
- **Progressive Search**: Intelligent time range adjustment to find available data across different periods
- **Visual Comparisons**: Generated comparison charts and graphs for data analysis

#### ⚙️ Settings & Preferences
- **Save Settings**: Store your theme preferences, default cities, and user configurations
- **Input Validation Settings**: Configure zip code validation and error handling preferences
- **Application Info**: Version details, feature overview, and system information
- Settings persist across application restarts with reliable JSON storage

### Smart Features
- **Advanced Error Handling**: Comprehensive input validation with helpful suggestions for zip codes and city names
- **Real-time Input Validation**: Immediate feedback on search inputs with zip code verification
- **Progressive Data Search**: Intelligent algorithms that adjust search parameters to find available CSV data
- **Multi-format Data Processing**: Seamless handling of both CSV historical data and live API responses
- **Status Updates**: Clear, real-time feedback on all operations with detailed progress indicators
- **Data Persistence**: All preferences, history, and CSV data automatically saved and managed

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

The application uses a hybrid storage approach combining JSON and CSV formats for comprehensive data management:

### Storage Files
- **user_preferences.json** - Theme settings, default cities, zip code preferences, and user configurations
- **weather_history.csv** - Historical weather search data with timestamps and detailed weather information
- **groupCsvs/ Directory** - Individual CSV files (abil.csv, felix.csv, kendra.csv, ricky.csv) for group weather analysis
- **Theme Configuration** - Custom color schemes and appearance settings (purple_theme.json, red.json)

### Advanced Data Features
- **Automatic Persistence** - All settings, history, and CSV data saved automatically with error recovery
- **Multi-format Processing** - Seamless integration between JSON preferences and CSV weather data
- **Progressive Data Search** - Smart algorithms to find recent data across different time periods
- **Group Data Analysis** - Simultaneous processing of multiple CSV files for comparative analysis
- **Data Validation** - Comprehensive validation for both user inputs and stored data integrity
- **Error Recovery** - Graceful handling of corrupted data files with automatic backup and restoration
- **Human-Readable Format** - Easy to backup, transfer, and manually edit user data files
- **Privacy-Focused** - All data stored locally with no external data collection or transmission

## �🛠️ Development & Architecture

### Code Organization
WeatherCap follows modern software engineering principles:

- **Modular Architecture** - Clear separation between UI, business logic, and data layers
- **Single Responsibility** - Each module has a focused, well-defined purpose  
- **Event-Driven Design** - Clean separation between user interactions and business logic
- **Error Handling** - Comprehensive input validation and graceful error recovery
- **Data Persistence** - Reliable storage with automatic backup and recovery

### Key Components
- **app_controller.py** - Central application coordinator and state management with feature integration
- **ui/gui_components.py** - Pure UI widget creation and layout logic with modern CustomTkinter design
- **ui/event_handlers.py** - User interaction processing, event routing, and comprehensive zip code validation
- **utils/preferences_manager.py** - Settings persistence and configuration management with JSON handling
- **utils/state_validator.py** - Advanced input validation with zip code verification and error handling
- **features/weather_history_csv.py** - CSV data processing, analysis, and group comparison functionality
- **features/forecast_predict.py** - 5-day weather forecasting with enhanced state input support
- **features/city_comparison.py** - Side-by-side city weather comparison with validation
- **core/weather_api.py** - Weather API communication with enhanced error handling and data processing

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

### Advanced Input Validation System
- **Comprehensive Zip Code Validation** - Real-time verification of US zip codes with error prevention
- **Smart Error Handling** - Intelligent suggestions and corrections for invalid inputs
- **Multi-format Support** - Handles various input formats with automatic normalization
- **Progressive Validation** - Real-time feedback during user input with immediate error detection

### Enhanced Weather API Integration  
- **OpenWeatherMap API** - Professional weather data source with reliable, up-to-date information
- **Enhanced Query Formatting** - Improved API queries with proper state handling (city,state,US format)
- **Rate Limiting Management** - Efficient API usage with built-in request management and optimization
- **Comprehensive Error Handling** - Graceful handling of network issues, API limits, and invalid responses
- **Data Formatting** - Clean, user-friendly presentation of complex weather information

### Advanced CSV Data Processing
- **Group File Analysis** - Simultaneous processing of multiple CSV files from `data/groupCsvs/` directory
- **Recent Data Focus** - Smart algorithms to automatically identify and display the most recent weather data
- **Progressive Time Range Search** - Intelligent adjustment of search parameters to find available data across different periods
- **Live vs Historical Comparison** - Comprehensive comparison between CSV historical data and current live API information
- **Data Validation** - Thorough validation of CSV file structure and content integrity

### Professional Theme Management
- **Dynamic Theme Switching** - Real-time theme changes without application restart
- **Persistent Preferences** - Theme choices automatically saved across sessions with reliable storage
- **Custom Color Schemes** - Professional color palettes optimized for both light and dark themes
- **UI Consistency** - All components properly themed and coordinated with comprehensive styling
- **Accessibility Features** - High contrast ratios and readable typography for enhanced user experience

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
- **Network Connectivity** - Check internet connection for weather data retrieval and API access
- **Input Validation** - Use valid US zip codes (5-digit format) or proper city names for accurate results
- **CSV Data Issues** - Ensure CSV files in `data/groupCsvs/` have proper formatting and recent data
- **Theme Problems** - Try toggling themes or restarting the application if visual issues occur
- **File Permissions** - Ensure the application has read/write access to the data directory for CSV processing

### Getting Help
- Check error messages for specific guidance on input formatting and validation requirements
- Review CSV file structure in `data/groupCsvs/` for proper data formatting
- Ensure all dependencies are installed correctly via `pip install -r requirements.txt`
- Verify `.env` file contains a valid OpenWeatherMap API key
- Check file permissions for data directory access and CSV processing capabilities

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
- **Framework**: CustomTkinter GUI with modern design
- **Architecture**: Modular with separation of concerns and advanced data processing
- **Data Processing**: CSV analysis, JSON persistence, and live API integration
- **Input Validation**: Comprehensive zip code verification and error handling
- **Testing**: API integration, CSV processing, and error handling validation
- **Storage**: Multi-format persistence with CSV and JSON data management
- **API Integration**: OpenWeatherMap REST API with enhanced query formatting
- **Version Control**: Git integration with proper line ending handling via `.gitattributes`

**Author**: Kendra Barnts  
**GitHub**: [@barntskendra4](https://github.com/barntskendra4)  
**Repository**: [WeatherCapstone](https://github.com/barntskendra4/WeatherCapstone)  
**Project Type**: Advanced Data Analysis, Visualization, & Interactive Dashboard Application