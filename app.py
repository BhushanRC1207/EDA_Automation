from flask import Flask, render_template, jsonify
from utils.info import Information
import os

app = Flask(__name__)

# Use the path defined in your original app.py
PATH = "./data/crop_yield.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-analysis')
def run_analysis():
    try:
        info = Information(PATH)
        # Capture the dictionary from our updated info.py
        results = info.get_info() 
        # return ONLY JSON here
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)