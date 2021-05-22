
class BoggleGame {
  //make new game

  constructor(boardId, secs = 60) {
    //game length = 60s
    this.secs = secs;
    this.displayTimer();

    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);

    // increment every 1000 ms
    this.timer = setInterval(this.time.bind(this), 1000);

    $(".make-guess").on("submit", this.handleSubmit.bind(this));
  }

  displayWord(word) {
    $(".words").append($("<li>", { text: word }));
  }

  displayScore() {
    $(".score").text(game.score);
  }

  displayMessage(msg, cls) {
    $(".msg")
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`);
  }

  //submit guess
  async handleSubmit(evt) {
    evt.preventDefault();
    let word = $(".word").val();
    if (game.words.has(word)) {
      game.displayMessage(`Already found ${word}`, "err");
      return;
    }

    let guess = $('.word').val();
    let guessObject = {word:guess};
    const resp = await $.ajax({
      type: 'POST',
      url: '/check-word',
      data: guessObject,
      // success: wordAdded()
    });
    let str_resp = JSON.stringify(resp)
    let new_resp = JSON.parse(str_resp)
    wordAdded(new_resp)

    function wordAdded(resp){
      if (new_resp.result === "not-word") {
        game.displayMessage(`${new_resp.word} is not a valid English word`, "err");
      }
      else if (resp.result === "not-on-board") {
        game.displayMessage(`${new_resp.word} is not a valid word on this board`, "err");
      }
      else {
        game.displayWord(new_resp.word);
        game.score += new_resp.word.length;
        game.displayScore();
        game.words.add(new_resp.word);
        game.displayMessage(`Added: ${new_resp.word}`, "ok");
      }
    }
  }

    displayTimer(){
      let time_left = this.secs
      $(".timer").text(time_left);
    }

    //increment timer
    async time(){
      this.secs -= 1;
      this.displayTimer();
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.endGame();
      }
    }

    //end game. score game and display message
    async endGame(){
      $(".make-guess").hide();
      const resp = await axios.post("/post-score", { score: this.score });
      if (resp.data.brokeRecord) {
        game.displayMessage(`New record: ${game.score}`, "ok");
      }
      else {
        game.displayMessage(`Final score: ${game.score}`, "ok");
      }
    }
}