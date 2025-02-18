from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load player data from Excel
def load_data():
    # Read the Excel file
    df = pd.read_excel('FGN DB Test v1.0 - FGNDB_20250218.xlsx')
    
    # Convert the data to a list of dictionaries
    data = df.to_dict(orient='records')
    
    # Ensure all headers are present in each record
    headers = [
        "Sorting Column", "FGN Manager", "FGN Club", "Sofifa ID", "PESDB ID", "Sofifa URL", 
        "PESDB URL", "TM URL", "Player", "Formatted Name", "EF Position", "EAFC Position", 
        "DoB", "Age", "Nationality", "League", "Club", "EF Overall", "EAFC Overall", 
        "TMV at Signing", "TMV", "Max Transfer Value", "Flag", "FGN Division", "Status", 
        "Wage", "FMID", "Face URL"
    ]
    
    # Add missing headers with None as the default value
    for record in data:
        for header in headers:
            if header not in record:
                record[header] = None
    
    return data

# Load the player data into memory
players_data = load_data()

# API endpoint to get players with pagination and search
@app.route('/api/players', methods=['GET'])
def get_players():
    club = request.args.get('club')
    search = request.args.get('search', '').lower()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))

    # Filter players by club
    filtered_players = [player for player in players_data if club in player['Club']]

    # Filter players by search query (if provided)
    if search:
        filtered_players = [player for player in filtered_players if search in player['Player'].lower()]

    # Pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_players = filtered_players[start_index:end_index]

    # Return JSON response with all headers
    return jsonify({
        'players': paginated_players,  # Players for the current page
        'totalPlayers': len(filtered_players)  # Total number of players (for pagination)
    })

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT if set, otherwise default to 5000
    app.run(host='0.0.0.0', port=port)  # Bind to 0.0.0.0 and use the specified port