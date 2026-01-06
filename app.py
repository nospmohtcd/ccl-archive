from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB_NAME = "ccl_archive.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_archive_structure():
    """Fetches unique year/month pairs to build the sidebar."""
    conn = get_db_connection()
    # Get distinct year and month combinations
    structure = conn.execute(
        "SELECT DISTINCT year, month FROM ccl_messages ORDER BY year DESC, month ASC"
    ).fetchall()
    conn.close()
    
    # Organize into a dictionary: { '91': ['01', '02', ...], '92': [...] }
    tree = {}
    for row in structure:
        if row['year'] not in tree:
            tree[row['year']] = []
        tree[row['year']].append(row['month'])
    return tree

@app.route('/')
def index():
    query = request.args.get('q')
    browse_year = request.args.get('year')
    browse_month = request.args.get('month')
    
    messages = []
    conn = get_db_connection()
    
    # Logic 1: If user is searching
    if query:
        sql = "SELECT id, year, month, day_file, subject, sender FROM ccl_messages WHERE content LIKE ? OR subject LIKE ? LIMIT 100"
        term = f"%{query}%"
        messages = conn.execute(sql, (term, term)).fetchall()
        
    # Logic 2: If user clicked a specific month in the sidebar
    elif browse_year and browse_month:
        sql = "SELECT id, year, month, day_file, subject, sender FROM ccl_messages WHERE year = ? AND month = ? ORDER BY day_file ASC"
        messages = conn.execute(sql, (browse_year, browse_month)).fetchall()
        
    conn.close()
    
    sidebar_data = get_archive_structure()
    return render_template('index.html', 
                           messages=messages, 
                           query=query, 
                           sidebar=sidebar_data,
                           selected_year=browse_year,
                           selected_month=browse_month)

@app.route('/message/<int:msg_id>')
def message(msg_id):
    conn = get_db_connection()
    msg = conn.execute("SELECT * FROM ccl_messages WHERE id = ?", (msg_id,)).fetchone()
    conn.close()
    return render_template('message.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
