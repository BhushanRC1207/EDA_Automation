from flask import Flask, render_template, jsonify
from utils.info import Information
from utils.analysis import Analysis  # NEW IMPORT
import os

app = Flask(__name__)

# PATH = "./data/calories.csv"
# PATH = "./data/crop_yield.csv"
PATH = "./data/crop.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-analysis')
def run_analysis():
    try:
        info = Information(PATH)
        results = info.get_info() 
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-visualization')  # NEW ROUTE
def run_visualization():
    """Generate visualizations for numeric columns"""
    try:
        analysis = Analysis(PATH)
        results = analysis.get_viz()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)