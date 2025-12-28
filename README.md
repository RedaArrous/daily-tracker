# Goal Tracker Calendar 🎯

> A minimalist web app to track your daily goal achievements with a beautiful calendar interface.

## ⚠️ Disclaimer

**This app was fully developed with AI assistance and is not my own original work.**

---

## ✨ Features

### Web Interface

- 📅 **Interactive Calendar** - Mark days as completed with a single click
- 🗓️ **Month & Year Views** - Switch between detailed monthly view or overview of entire year
- 📝 **Notes System** - Add notes to any day (right-click on a day)
- 📊 **Statistics** - Track monthly and total completed days
- 📤 **Data Export** - Export your data as JSON or CSV
- 🎨 **Modern UI** - Clean, minimalist design with smooth animations
- 💾 **Persistent Storage** - SQLite database + CSV export

### Command Line Tool

- 🚀 **Quick Mark** - Standalone executable to mark today as completed
- ⚡ **Fast Note Entry** - Add notes via command prompt
- 🔄 **Auto-sync** - Updates both database and CSV automatically
- 📦 **Portable** - No Python installation required for the .exe

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (optional, for cloning) - [Download Git](https://git-scm.com/downloads)

### Step-by-Step Installation

#### Option 1: Using Git (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** and go to:
   ```
   http://127.0.0.1:5000
   ```

   You should see the Goal Tracker Calendar interface! 🎉

#### Option 2: Manual Download

1. **Download the ZIP** from GitHub and extract it
2. **Open terminal/command prompt** in the extracted folder
3. **Follow steps 2-5** from Option 1 above

### First Run

- On first run, the app automatically creates:
  - `goals.db` - SQLite database file
  - `data.csv` - CSV export file with headers
- Both files will be in your app directory
- Your data is stored locally and never sent anywhere

---

## 💻 Usage Guide

### Web Interface - Complete Tutorial

#### 1. Starting the Application

```bash
# Make sure you're in the app directory
cd path/to/app

# Activate virtual environment (if using one)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the app
python app.py

# You should see:
# * Running on http://127.0.0.1:5000
```

#### 2. Basic Operations

**Marking Days as Completed:**
- **Click any day** in the calendar to mark it as completed (turns green ✓)
- **Click again** on a completed day to unmark it (turns gray)
- Completed days are instantly saved to the database

**Navigation:**
- **Arrow buttons (← →)** - Navigate between months
- **"Today" button** - Jump back to current month
- **"Year View" button** - See all 12 months at once
- In year view, click any day to mark/unmark it

**Statistics:**
- **This Month** - Shows completed days in current month
- **Total Days** - Shows all completed days ever

#### 3. Notes Feature (Right-Click)

**Adding a Note:**
1. **Right-click** on any day in the calendar
2. A modal window appears with a text area
3. **Type your note** (supports any text, quotes, emojis, etc.)
4. **Click "Save Note"** or press Enter
5. A small **dot indicator** appears on that day

**Editing a Note:**
1. **Right-click** on a day that has a note
2. The existing note appears in the text area
3. **Modify** the text as needed
4. **Click "Save Note"** to update

**Viewing Notes:**
- **Hover** over the dot indicator to see a preview
- **Right-click** to see the full note

**Deleting a Note:**
1. Right-click on the day
2. **Clear all text** in the text area
3. Click "Save Note"
4. The note is removed (set to empty)

#### 4. Exporting Your Data

**Export as JSON:**
1. Click **"Export Data"** button
2. Select **"Export as JSON"**
3. File downloads as `goals_export_YYYYMMDD.json`
4. Use this for backups or data analysis

**Export as CSV:**
1. Click **"Export Data"** button
2. Select **"Export as CSV"**
3. File downloads as `goals_export_YYYYMMDD.csv`
4. Open in Excel, Google Sheets, or pandas

**Note:** The `data.csv` file in your app directory is automatically updated with every change!

### Command Line Tool (MarkToday) - Complete Guide

The MarkToday tool lets you quickly mark today as completed without opening the web browser.

#### Creating the Executable (.exe)

**Step 1: Install PyInstaller**
```bash
# Make sure you're in the app directory with venv activated
pip install pyinstaller
```

**Step 2: Build the Executable**
```bash
# Run PyInstaller
pyinstaller --onefile --name="MarkToday" --console mark_today.py

# Wait for the build to complete (15-30 seconds)
# Output will be in: dist/MarkToday.exe
```

**Step 3: Copy to App Directory**
```bash
# Windows
copy dist\MarkToday.exe .

# macOS/Linux
cp dist/MarkToday MarkToday
```

**Step 4: Optional - Create Desktop Shortcut**
1. Right-click `MarkToday.exe`
2. Select "Create shortcut"
3. Move shortcut to your desktop
4. Rename to "Mark Today" (remove .exe)

#### Using the MarkToday Tool

**Method 1: Double-Click the .exe**
1. **Double-click** `MarkToday.exe` in your app folder
2. A console window opens
3. Shows today's date and current status
4. Prompts: "Do you want to add a note for today? (y/n):"
5. Type `y` to add a note, or `n` to skip
6. If `y`, type your note and press Enter
7. Confirmation message appears
8. Press Enter to close

**Method 2: Command Line**
```bash
# Navigate to app directory
cd path/to/app

# Run the executable
./MarkToday.exe   # Windows
./MarkToday       # macOS/Linux
```

**Example Workflows:**

*Quick mark without note:*
```
Do you want to add a note for today? (y/n): n
✓ No note added
✓ CSV file updated successfully!
```

*Mark with a note:*
```
Do you want to add a note for today? (y/n): y
Enter your note (press Enter when done):
> Completed my workout and studied for 2 hours
✓ Note saved: "Completed my workout and studied for 2 hours"
✓ CSV file updated successfully!
```

*Editing today's existing note:*
```
✓ Today is already marked as completed!
Existing note: "Old note"

Do you want to edit today's note? (y/n): y
Enter your note (press Enter when done):
> Updated note with more details
✓ Note saved: "Updated note with more details"
```

**Important Notes:**
- The `.exe` must be in the **same directory** as `goals.db` and `data.csv`
- Running it multiple times on the same day won't create duplicates
- Changes are automatically synced to both database and CSV
- The tool works even when the web app is not running

See [MARK_TODAY_INSTRUCTIONS.md](MARK_TODAY_INSTRUCTIONS.md) for more details.

---

## 📁 Project Structure

```
app/
├── app.py                          # Flask web server
├── mark_today.py                   # CLI script for marking today
├── requirements.txt                # Python dependencies
├── data.csv                        # CSV export (auto-created)
├── goals.db                        # SQLite database (auto-created)
├── README.md                       # This file
├── MARK_TODAY_INSTRUCTIONS.md      # CLI tool documentation
├── templates/
│   └── index.html                  # Main HTML template
└── static/
    ├── css/
    │   └── style.css               # Stylesheet
    └── js/
        └── app.js                  # Frontend JavaScript
```

---

## 🗄️ Data Storage

### Database (`goals.db`)

- SQLite database created automatically on first run
- Stores: date, completion status, and notes
- Schema:
  ```sql
  CREATE TABLE completed_days (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT UNIQUE NOT NULL,
      completed INTEGER DEFAULT 1,
      note TEXT DEFAULT NULL
  );
  ```

### CSV Export (`data.csv`)

- Automatically synced with database on every change
- Format: `date,done,note`
- Compatible with Excel, pandas, and other data analysis tools
- Proper CSV escaping for special characters

---

## 📦 Dependencies

```
Flask==3.1.0
```

Optional (for building executable):

```
pyinstaller==6.17.0
```

Optional (for data analysis):

```
pandas==2.3.3
```

---

## 🔧 Configuration

### Change Port or Host

Edit `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
```

### Database Location

Edit the `CSV_FILE` and database path in `app.py` if needed.

---

## 💡 Tips & Best Practices

- ✅ **Backup regularly**: Export your data or backup `goals.db` and `data.csv`
- ✅ **Use notes wisely**: Add context about why you completed or missed a day
- ✅ **Build the .exe**: Create `MarkToday.exe` for quick daily updates
- ✅ **Version control**: `.gitignore` is configured to exclude personal data
- ✅ **Data portability**: CSV export ensures your data is never locked in

---

## 🐛 Troubleshooting

### "Failed to update day status"

1. Stop the Flask app (Ctrl+C)
2. Delete `goals.db`
3. Restart the app - database will be recreated

### CSV not updating

- Check file permissions in the app directory
- Ensure `data.csv` is not open in Excel or another program

### MarkToday.exe not working

- Make sure it's in the same directory as `goals.db` and `data.csv`
- Run from command prompt to see error messages

---

## 📄 License

This project is open source and available for personal use.

---

## 🙏 Acknowledgments

Built with assistance from AI tools for rapid prototyping and development.

---

**Enjoy tracking your goals!** 🎯✨
