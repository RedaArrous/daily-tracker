#!/usr/bin/env python
"""Mark today as completed and optionally add a note"""
import sqlite3
import csv
import os
from datetime import datetime

# Configuration
DB_FILE = 'goals.db'
CSV_FILE = 'data.csv'

def sync_to_csv():
    """Sync database content to CSV file"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT date, completed, note FROM completed_days ORDER BY date')
        data = cursor.fetchall()
        conn.close()
        
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(['date', 'done', 'note'])
            for row in data:
                date_val = row[0]
                done_value = 'Yes' if row[1] == 1 else 'No'
                note_value = row[2] if (row[2] and row[2].strip()) else ''
                writer.writerow([date_val, done_value, note_value])
            f.flush()
            os.fsync(f.fileno())
        
        return True
    except Exception as e:
        print(f"Error syncing to CSV: {str(e)}")
        return False

def mark_today_completed():
    """Mark today as completed and optionally add a note"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 60)
    print("           MARK TODAY AS COMPLETED")
    print("=" * 60)
    print(f"\nToday's date: {today}")
    print()
    
    # Check if database exists
    if not os.path.exists(DB_FILE):
        print(f"Error: Database file '{DB_FILE}' not found!")
        print("Please make sure you're running this from the app directory.")
        input("\nPress Enter to exit...")
        return
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if today is already in the database
        cursor.execute('SELECT completed, note FROM completed_days WHERE date = ?', (today,))
        result = cursor.fetchone()
        
        if result:
            already_completed = result[0] == 1
            existing_note = result[1] if result[1] else ''
            
            if already_completed:
                print("✓ Today is already marked as completed!")
                if existing_note:
                    print(f"\nExisting note: \"{existing_note}\"")
            else:
                # Mark as completed
                cursor.execute('UPDATE completed_days SET completed = 1 WHERE date = ?', (today,))
                conn.commit()
                print("✓ Today has been marked as completed!")
        else:
            # Insert new entry as completed
            cursor.execute('INSERT INTO completed_days (date, completed, note) VALUES (?, 1, NULL)', (today,))
            conn.commit()
            print("✓ Today has been marked as completed!")
            existing_note = ''
        
        # Ask about note
        print("\n" + "-" * 60)
        if existing_note:
            response = input("\nDo you want to edit today's note? (y/n): ").strip().lower()
        else:
            response = input("\nDo you want to add a note for today? (y/n): ").strip().lower()
        
        if response in ['y', 'yes']:
            print("\nEnter your note (press Enter when done):")
            if existing_note:
                print(f"Current note: {existing_note}")
            note = input("> ").strip()
            
            if note:
                cursor.execute('UPDATE completed_days SET note = ? WHERE date = ?', (note, today))
                conn.commit()
                print(f"\n✓ Note saved: \"{note}\"")
            else:
                # User entered empty string, remove note
                cursor.execute('UPDATE completed_days SET note = NULL WHERE date = ?', (today,))
                conn.commit()
                print("\n✓ Note cleared (empty value)")
        else:
            if not existing_note:
                # Make sure note is NULL/empty
                cursor.execute('UPDATE completed_days SET note = NULL WHERE date = ?', (today,))
                conn.commit()
            print("\n✓ No note added")
        
        conn.close()
        
        # Sync to CSV
        print("\nSyncing to CSV file...")
        if sync_to_csv():
            print("✓ CSV file updated successfully!")
        else:
            print("✗ Warning: Failed to sync to CSV file")
        
        print("\n" + "=" * 60)
        print("           SUCCESS!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    mark_today_completed()
