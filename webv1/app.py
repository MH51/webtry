import os
from flask import Flask, request, jsonify, send_file, render_template,redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')

# Create CSV with headers if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Name', 'Item', 'Quantity', 'Selection'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Try to parse JSON first
    if request.is_json:
        data = request.get_json()
        selection = data.get('option')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if selection:
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, '', '', '', selection])
            return jsonify({'message': 'Saved'})
        return jsonify({'message': 'No option received'}), 400
    else:
        # Handle form submission
        name = request.form.get('name')
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not all([name, item, quantity]):
            return render_template('index.html', message="Please fill in all fields.")

        with open(CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, name, item, quantity, ''])
        
        return render_template('index.html', message="Order submitted!")

@app.route('/download')
def download():
    if not os.path.exists(CSV_FILE):
        return "CSV file not found. Please submit some data first.", 404
    return send_file(CSV_FILE, as_attachment=True)

#Rest by del exsiting csv file in location
@app.route('/reset')
def reset():
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/main')
def main():
    return render_template('main.html')      
   
    

if __name__ == '__main__':
    app.run(debug=True)