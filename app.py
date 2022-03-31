from flask import Flask, render_template,session,redirect,request,jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "zelly123"

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/new-game')
def new_game():
    """Generate new boggle board and store it in session"""
    
    if 'times_played' not in session:
        session['times_played'] = 0

    if 'high_score' not in session:
        session['high_score'] = 0

    session['boggle_board'] = boggle_game.make_board()
    return redirect('/play')

@app.route('/play')
def play_game():

    return render_template('game.html')

@app.route('/check-word')
def check_word():
    word = request.args['word']
    board = session['boggle_board']

    response = {"result": boggle_game.check_valid_word(board, word)}

    return jsonify(response)

@app.route('/game-over', methods=['POST'] )
def game_over():
    score = request.json['score']
    
    if score > session['high_score']:
        session['high_score'] = score

    high_score = session['high_score']

    response = {"result": high_score}
    
    plays = session['times_played']
    plays += 1
    session['times_played'] = plays

    return jsonify(response)
    