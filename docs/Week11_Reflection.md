
## 🔖 Section 0: Fellow Details

Kendra Barnts
github username: barntskendra4
Data, Visual, & Interactive
Yes, Owner & contributor


## ✍️ Section 1: Week 11 Reflection
Answer each prompt with 3–5 bullet points:

Key Takeaways: What did you learn about capstone goals and expectations?

Concept Connections: Which Week 1–10 skills feel strongest? Which need more practice?

Early Challenges: Any blockers (e.g., API keys, folder setup)?

Support Strategies: Which office hours or resources can help you move forward?



## 🧠 Section 2: Feature Selection Rationale
List three features + one enhancement you plan to build.

Feature Name	Difficulty (1–3)	Why You Chose It / Learning Goal

1) City Comparison | 1 | Practice API calls and data parsing - allows users to compare weather between multiple cities side-by-side 
2) Theme Switcher | 2 | Learn Tkinter styling and user preferences - implement dark/light mode with color scheme management 
3) Tomorrow's Guess | 3 | Advanced API integration with forecast data - predict tomorrow's weather and track accuracy over time 
| Enhancement –  **Creative Visuals** |
-Weather Icons & Charts – Use matplotlib or PIL to display weather icons, temperature graphs, and visual data representations 

## 🗂️ Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:

Core Modules and Folders
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

Feature modules

Data flow between components
```
User Input (GUI) 
    ↓
main.py (Event Handler)
    ↓
config.py (WeatherAPI class)
    ↓
OpenWeatherMap API
    ↓
Feature Modules (process data)
    ↓
data/ files (persistence)
    ↓
GUI Updates (display results)
```

## 📊 Section 4: Data Model Plan
Fill in your planned data files or tables:

File/Table Name	Format (txt, json, csv, other)	Example Row
weather_history.txt	txt	2025-06-09,New Brunswick,78,Sunny


## 📆 Section 5: Personal Project Timeline (Weeks 12–17)
Customize based on your availability:

Week	Monday	Tuesday	Wednesday	Thursday	Key Milestone
12	API setup	Error handling	Tkinter shell	Buffer day	Basic working app
13	Feature 1			Integrate	Feature 1 complete
14	Feature 2 start		Review & test	Finish	Feature 2 complete
15	Feature 3	Polish UI	Error passing	Refactor	All features complete
16	Enhancement	Docs	Tests	Packaging	Ready-to-ship app
17	Rehearse	Buffer	Showcase	–	Demo Day



## ⚠️ Section 6: Risk Assessment
Identify at least 3 potential risks and how you’ll handle them.

Risk	Likelihood (High/Med/Low)	Impact (High/Med/Low)	Mitigation Plan
API Rate Limit	Medium	Medium	Add delays or cache recent results

-API Key Exposure/Invalid | High | High | Use .env file, add validation checks, create backup test data |
-Network/Internet Issues | Medium | High | Implement offline mode with cached data, graceful error handling |
-Time Management/Scope Creep | High | Medium | Prioritize core features first, cut enhancement if needed, track time weekly 


## 🤝 Section 7: Support Requests
What specific help will you ask for in office hours or on Slack?
-Review my WeatherAPI class structure - is the error handling robust enough for production use?
-Help designing the data flow between API calls, GUI updates, and file storage


## ✅ Section 8: Before Monday (Start of Week 12)
Complete these setup steps before Monday:

Push main.py, config.py, and a /data/ folder to your repo

Add OpenWeatherMap key to .env (⚠️ Do not commit the key)

Create files for the chosen feature in /features/ 

like this:
# weather_journal.py
"""
Feature: Weather Journal
- Stores daily mood and notes alongside weather data
"""
def add_journal_entry(date, mood, notes):
    # your code goes here
    pass
Commit and push a first-draft README.md

Book office hours if you're still stuck on API setup

