from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"

boggle = Boggle()


@app.route("/")
def homepage():
    """show board on homepage"""

    board = boggle.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template("index.html", board=board, highscore=highscore,
                           numplays=numplays)

@app.route("/check-word", methods=["POST"])
def check_word():
    """is word in dictionary?"""

    word = request.form["word"]
    board = session["board"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    response = boggle.check_valid_word(board, word)

    result = jsonify({'result': response, 'word': word})
    return result

@app.route("/post-score", methods=["POST"])
def post_score():
    """request score, update numplays + 1, update high score if score > highscore"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    session['numplays'] = numplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)

