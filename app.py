from flask import Flask, render_template, jsonify, send_file
import sqlite3
from datetime import datetime
import json
import io
import csv

app = Flask(__name__)

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            completed INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/days', methods=['GET'])
def get_days():
    """Get all completed days"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date FROM completed_days WHERE completed = 1')
    days = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'completed_days': days})

@app.route('/api/days/<date>', methods=['POST'])
def toggle_day(date):
    """Toggle a day's completion status"""
    try:
        datetime.strptime(date, '%Y-%m-%d')
        
        conn = sqlite3.connect('goals.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT completed FROM completed_days WHERE date = ?', (date,))
        result = cursor.fetchone()
        
        if result:
            new_status = 0 if result[0] == 1 else 1
            cursor.execute('UPDATE completed_days SET completed = ? WHERE date = ?', (new_status, date))
            completed = new_status == 1
        else:
            cursor.execute('INSERT INTO completed_days (date, completed) VALUES (?, 1)', (date,))
            completed = True
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'completed': completed})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export data as JSON"""
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, completed FROM completed_days ORDER BY date')
    data = [{'date': row[0], 'completed': bool(row[1])} for row in cursor.fetchall()]
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
    cursor.execute('SELECT date, completed FROM completed_days ORDER BY date')
    data = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Completed'])
    for row in data:
        writer.writerow([row[0], 'Yes' if row[1] else 'No'])
    
    buffer = io.BytesIO(output.getvalue().encode())
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'goals_export_{datetime.now().strftime("%Y%m%d")}.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
