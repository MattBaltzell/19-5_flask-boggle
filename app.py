from flask import Flask, render_template,session,redirect,request,jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "zelly123"

@app.route('/')
def new_game():
    """Generate new boggle board and store it in session"""

    session['boggle_board'] = boggle_game.make_board()
    return redirect('/play')

@app.route('/play')
def play_game():

    return render_template('index.html')

@app.route('/check-word')
def check_word():
    word = request.args['word']
    board = session['boggle_board']

    response = {"result": boggle_game.check_valid_word(board, word)}

    return jsonify(response)