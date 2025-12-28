# Mark Today Script - Quick Start Guide

## 📌 What Does It Do?

The **MarkToday.exe** program allows you to quickly mark today as completed and optionally add a note by simply double-clicking the executable file.

## 🚀 How to Use

1. **Double-click** `MarkToday.exe` in the app folder
2. The program will:
   - Automatically mark today as completed
   - Ask if you want to add/edit a note
   - Update both the database and CSV file
   - Show a success message

## 💡 Features

✅ **Smart Detection**: If today is already marked as completed, it won't create duplicate entries

✅ **Note Management**: You can add a new note or edit an existing one

✅ **Empty Notes**: If you choose not to add a note, the note field will be empty (not "None")

✅ **Automatic Sync**: Changes are automatically saved to both `goals.db` and `data.csv`

## 📝 Usage Examples

### Example 1: Mark Today (No Note)

```
Do you want to add a note for today? (y/n): n
✓ No note added
✓ CSV file updated successfully!
```

### Example 2: Mark Today with Note

```
Do you want to add a note for today? (y/n): y
Enter your note (press Enter when done):
> Finished all my tasks today!
✓ Note saved: "Finished all my tasks today!"
✓ CSV file updated successfully!
```

### Example 3: Edit Existing Note

```
✓ Today is already marked as completed!
Existing note: "Old note"

Do you want to edit today's note? (y/n): y
Enter your note (press Enter when done):
> Updated note with new information
✓ Note saved: "Updated note with new information"
✓ CSV file updated successfully!
```

## 📁 Files

- `MarkToday.exe` - The executable program (8.9 MB)
- `mark_today.py` - The source Python script
- `goals.db` - SQLite database (created automatically)
- `data.csv` - CSV export of all data

## ⚠️ Important Notes

1. **Run from app directory**: The .exe must be in the same folder as `goals.db` and `data.csv`
2. **No duplicates**: Running it multiple times on the same day won't create duplicate entries
3. **Note format**: Notes can contain any text including quotes, commas, and special characters
4. **CSV compatible**: The CSV file can be opened in Excel, pandas, or any CSV reader

## 🔧 Technical Details

- Built with PyInstaller
- Standalone executable (no Python installation required)
- Windows compatible
- Uses SQLite for database and CSV for exports
- Proper CSV formatting with QUOTE_NONNUMERIC for special characters

## 🎯 Quick Workflow

**Daily routine:**

1. Double-click `MarkToday.exe`
2. Press `n` if no note needed, or `y` to add a note
3. Press Enter to exit
4. Done! ✓

That's it! Your progress is automatically tracked and saved.
