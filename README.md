# Goal Tracker Calendar

A minimalist web app to track your daily goal achievements with a beautiful calendar interface.

## Features

- ✅ Mark days as completed when you achieve your goals
- 📅 View single month or entire year
- 📊 Track statistics (monthly and total)
- 📤 Export your data as JSON or CSV
- 🎨 Modern, minimalist UI with smooth animations
- 💾 SQLite database for local storage

## Setup Instructions

### Prerequisites
- Python 3.7 or higher

### Installation

1. Open a terminal in the project directory

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

- **Mark a day**: Click on any day to mark it as completed (green)
- **Unmark a day**: Click on a completed day to unmark it
- **Navigate months**: Use the arrow buttons to move between months
- **Today button**: Quickly jump to the current month
- **Year View**: Click "Year View" to see all 12 months at once
- **Export Data**: Click "Export Data" to download your progress as JSON or CSV

## Database

The app uses SQLite and automatically creates a `goals.db` file in the project directory. This file stores all your completed days.

## Project Structure

```
app/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── goals.db              # SQLite database (auto-created)
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Styles
    └── js/
        └── app.js        # JavaScript logic
```

## Tips

- Your data is stored locally in the `goals.db` file
- Backup the database file to preserve your data
- Export your data regularly for additional backups
- The app is designed for personal, local use

Enjoy tracking your goals! 🎯
