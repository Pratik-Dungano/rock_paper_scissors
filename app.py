from flask import Flask, render_template, request, redirect, session
import random
import secrets

# Generate a secure secret key for the session
secret_key = secrets.token_hex(16)

# Create the Flask application
app = Flask(__name__)
app.secret_key = secret_key

# Define the possible choices in the game
choices = ('r', 'p', 's')

# Define the number of rounds for the game
NUM_ROUNDS = 5

@app.route('/')
def index():
    """ Serve the game interface """
    # Initialize session variables if they don't exist
    if 'round' not in session:
        session['round'] = 0
    if 'pPoints' not in session:
        session['pPoints'] = 0
    if 'cPoints' not in session:
        session['cPoints'] = 0
    if 'tie' not in session:
        session['tie'] = 0
    if 'pChoice' not in session:
        session['pChoice'] = 'r'  # Default value for player choice
    if 'cChoice' not in session:
        session['cChoice'] = 'r'  # Default value for computer choice
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    """ Handle the gameplay logic and decision making """
    # Get the player's choice from form data
    symbol = request.form['symbol']
    # Randomly select the computer's choice
    cChoice = random.choice(choices)
    session['cChoice'] = cChoice
    
    # Check if the player's choice is valid
    if symbol not in choices:
        return "Invalid choice"
    
    session['pChoice'] = symbol
    
    # Update the game score based on the choices
    
    
    # Check if the game has completed 5 rounds
    if session['round'] == NUM_ROUNDS:
        # Determine the winner and redirect to the result page
        winner = determine_winner(session['pPoints'], session['cPoints'])
        return redirect('/result/' + winner)
    
    update_score(symbol, cChoice)
    # Increment the round counter
    session['round'] += 1
    
    return redirect('/')

@app.route('/status')
def status():
    """Display current scores and choices"""
    return render_template('status.html', pChoice=session['pChoice'],
                           cChoice=session['cChoice'],
                           pPoints=session['pPoints'],
                           cPoints=session['cPoints'],
                           round=session['round'])

@app.route('/reset', methods=['POST'])
def reset():
    """ Reset the game scores """
    session['cPoints'] = 0
    session['pPoints'] = 0
    session['round'] = 0
    session['tie'] = 0
    session['pChoice'] = 'r'
    session['cChoice'] = 'r'
    return redirect('/')

@app.route('/result/<winner>')
def result(winner):
    """ Display the winner of the game """
    return render_template('result.html', winner=winner)

@app.route('/continue', methods=['POST'])
def continue_game():
    """ Continue the game without resetting the round """
    session['round'] = 0
    return redirect('/')

def update_score(player_choice, computer_choice):
    """ Update scores based on the player and computer choices """
    if player_choice == computer_choice:
        session['tie'] += 1  # No points awarded for a tie
    elif (player_choice == 'r' and computer_choice == 's') or \
         (player_choice == 's' and computer_choice == 'p') or \
         (player_choice == 'p' and computer_choice == 'r'):
        session['pPoints'] += 1
    else:
        session['cPoints'] += 1

def determine_winner(player_points, computer_points):
    """ Determine the winner of the game """
    if player_points > computer_points:
        return "Player"
    elif computer_points > player_points:
        return "Computer"
    else:
        return "Tie"

if __name__ == '__main__':
    app.run(debug=True)
