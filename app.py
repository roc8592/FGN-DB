from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load player data from Excel
def load_data():
    # Read the Excel file
    df = pd.read_excel('C:/Users/roc_0/OneDrive/Documents/FGN/Vercel/FGN DB Test v1.0 - FGNDB_20250218.xlsx')
    # Convert the data to a list of dictionaries
    return df.to_dict(orient='records')

# Load the player data into memory
players_data = load_data()

# API endpoint to get players with pagination and search
@app.route('/api/players', methods=['GET'])
def get_players():
    # Get query parameters from the request
    club = request.args.get('club')  # Selected club
    search = request.args.get('search', '').lower()  # Search query (optional)
    page = int(request.args.get('page', 1))  # Current page (default: 1)
    page_size = int(request.args.get('pageSize', 10))  # Players per page (default: 10)

    # Filter players by club
    filtered_players = [player for player in players_data if club in player['Club']]

    # Filter players by search query (if provided)
    if search:
        filtered_players = [player for player in filtered_players if search in player['Player'].lower()]

    # Pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_players = filtered_players[start_index:end_index]

    # Return JSON response
    return jsonify({
        'players': paginated_players,  # Players for the current page
        'totalPlayers': len(filtered_players)  # Total number of players (for pagination)
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Run in debug mode for development