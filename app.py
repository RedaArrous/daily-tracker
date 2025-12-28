from flask import Flask, render_template, jsonify, send_file, request
import sqlite3
from datetime import datetime
import json
import io
import csv
import os

app = Flask(__name__)
CSV_FILE = 'data.csv'

def init_db():
    """Initialize the database and load data from CSV"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            completed INTEGER DEFAULT 1,
            note TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    
    # Load data from CSV if it exists and has data
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows_loaded = 0
                for row in reader:
                    if row.get('date') and row.get('done'):
                        completed = 1 if row['done'].strip().lower() == 'yes' else 0
                        note_str = row.get('note', '').strip()
                        # Convert 'None' string or empty to NULL
                        note = None if (not note_str or note_str.lower() == 'none') else note_str
                        cursor.execute('''
                            INSERT OR REPLACE INTO completed_days (date, completed, note) 
                            VALUES (?, ?, ?)
                        ''', (row['date'].strip(), completed, note))
                        rows_loaded += 1
                conn.commit()
                print(f"Loaded {rows_loaded} rows from CSV into database")
        except Exception as e:
            print(f"Error loading from CSV: {str(e)}")
    
    conn.close()

def sync_to_csv():
    """Sync database content to CSV file"""
    try:
        conn = sqlite3.connect('goals.db')
        cursor = conn.cursor()
        cursor.execute('SELECT date, completed, note FROM completed_days ORDER BY date')
        data = cursor.fetchall()
        conn.close()
        
        # Write to CSV with explicit flushing and proper quoting
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            # Use QUOTE_NONNUMERIC to properly quote all string values
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(['date', 'done', 'note'])
            for row in data:
                date_val = row[0]
                done_value = 'Yes' if row[1] == 1 else 'No'
                # Mark empty notes as empty string (pandas handles this better than 'None')
                note_value = row[2] if (row[2] and row[2].strip()) else ''
                writer.writerow([date_val, done_value, note_value])
            f.flush()  # Ensure data is written to disk
            os.fsync(f.fileno())  # Force write to disk
        
        print(f"CSV synced successfully with {len(data)} records to {CSV_FILE}")
        return True
    except Exception as e:
        print(f"Error syncing to CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/days', methods=['GET'])
def get_days():
    """Get all completed days with notes"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, note FROM completed_days WHERE completed = 1')
    days = [row[0] for row in cursor.fetchall()]
    notes_data = {row[0]: row[1] for row in cursor.execute('SELECT date, note FROM completed_days').fetchall()}
    conn.close()
    return jsonify({'completed_days': days, 'notes': notes_data})

@app.route('/api/days/<date>', methods=['POST'])
def toggle_day(date):
    """Toggle a day's completion status"""
    try:
        datetime.strptime(date, '%Y-%m-%d')
        
        conn = sqlite3.connect('goals.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT completed, note FROM completed_days WHERE date = ?', (date,))
        result = cursor.fetchone()
        
        if result:
            new_status = 0 if result[0] == 1 else 1
            cursor.execute('UPDATE completed_days SET completed = ? WHERE date = ?', (new_status, date))
            completed = new_status == 1
        else:
            # Insert with None as note value
            cursor.execute('INSERT INTO completed_days (date, completed, note) VALUES (?, 1, NULL)', (date,))
            completed = True
        
        conn.commit()
        conn.close()
        
        # Sync changes to CSV and verify
        sync_success = sync_to_csv()
        
        print(f"Toggled day {date}: completed={completed}, CSV sync: {sync_success}")
        return jsonify({'success': True, 'completed': completed})
    except Exception as e:
        print(f"Error toggling day: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/days/<date>/note', methods=['POST'])
def update_note(date):
    """Update or add a note for a specific day"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
            
        note = data.get('note', '').strip()
        # Store NULL in database if note is empty
        note_value = note if note else None
        
        datetime.strptime(date, '%Y-%m-%d')
        
        conn = sqlite3.connect('goals.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM completed_days WHERE date = ?', (date,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute('UPDATE completed_days SET note = ? WHERE date = ?', (note_value, date))
        else:
            cursor.execute('INSERT INTO completed_days (date, completed, note) VALUES (?, 0, ?)', (date, note_value))
        
        conn.commit()
        conn.close()
        
        # Sync changes to CSV and verify
        sync_success = sync_to_csv()
        
        print(f"Updated note for {date}: note={'None' if not note else 'set'}, CSV sync: {sync_success}")
        return jsonify({'success': True, 'note': note})
    except Exception as e:
        print(f"Error updating note: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/days/<date>/note', methods=['GET'])
def get_note(date):
    """Get note for a specific day"""
    try:
        conn = sqlite3.connect('goals.db')
        cursor = conn.cursor()
        cursor.execute('SELECT note FROM completed_days WHERE date = ?', (date,))
        result = cursor.fetchone()
        conn.close()
        
        note = result[0] if result and result[0] else ''
        return jsonify({'success': True, 'note': note})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export data as JSON"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, completed, note FROM completed_days ORDER BY date')
    data = [{'date': row[0], 'completed': bool(row[1]), 'note': row[2] if row[2] else ''} for row in cursor.fetchall()]
    conn.close()
    
    json_str = json.dumps(data, indent=2)
    buffer = io.BytesIO(json_str.encode())
    
    return send_file(
        buffer,
        mimetype='application/json',
        as_attachment=True,
        download_name=f'goals_export_{datetime.now().strftime("%Y%m%d")}.json'
    )

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export data as CSV"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, completed, note FROM completed_days ORDER BY date')
    data = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Completed', 'Note'])
    for row in data:
        writer.writerow([row[0], 'Yes' if row[1] else 'No', row[2] if row[2] else ''])
    
    buffer = io.BytesIO(output.getvalue().encode())
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'goals_export_{datetime.now().strftime("%Y%m%d")}.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
