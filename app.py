from flask import Flask, request, jsonify, render_template
from db_handler import DatabaseHandler
import logging

app = Flask(__name__)
db = DatabaseHandler()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_player():
    player_name = request.args.get('name', '').strip()
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    try:
        decklists = db.get_player_decklists(player_name)
        if not decklists:
            return jsonify({"error": "No decklists found for this player"}), 404
            
        # Format the results with the most recent first
        formatted = [{
            "hero": decklist[0],
            "url": decklist[1],
            "tournament": decklist[2]
        } for decklist in decklists]
        
        return jsonify({
            "player": player_name,
            "decklists": formatted
        })
    except Exception as e:
        logging.error(f"Error searching for {player_name}: {e}")
        return jsonify({"error": "Database error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)