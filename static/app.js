const form = document.getElementById('form')
const guess = document.getElementById('word')
const feedback = document.getElementById('feedback')
let score = 0;
let playing = false;

form.addEventListener('submit', guessHandler)
window.addEventListener('load',getFocus)


function getFocus() {
    document.getElementById('word').focus();
}

async function guessHandler(e){
    e.preventDefault();
    if(!playing) return;
    feedback.classList.remove('faded')
    let word = guess.value
    const points = word.length;

    let res = await axios.get('/check-word',{params: {word}})
    let status = res.data.result
    await showStatusMsg(status,points)
    
    guess.value = ''
    guess.focus();
    
}

function showStatusMsg(status,points){
    if(status !== 'ok'){
        feedback.textContent = status.split('-').join(' ').toUpperCase()
        feedback.classList.add('red')
    } else{
        feedback.textContent = `${status.split('-').join(' ').toUpperCase()} +${points} points!` 
        feedback.classList.remove('red')
        updateScore(points)
    }
    feedback.classList.add('faded')
}

function updateScore(points){
    score += points
    document.querySelector('#score').textContent = score;
}

/** 
 * GAME TIMER
 * 
 */
const startBtn = document.getElementById('start')
const innerBar = document.querySelector('.innerBar')
const progressText = document.querySelector('.progressText')
const boardRows = document.querySelectorAll('.board__row')
const endScreenMsg = document.querySelector('.end-screen p')


window.addEventListener('load', function () {
  playing = true;
  let timeLeft = 59;
//   boardRows.forEach(el=> el.classList.remove('hidden'))

  startBtn.style.opacity = '0'
  innerBar.animate({ width: "0%" }, 0);
  progressText.textContent = "Game in Progress";

  const countdown = setInterval(function () {
    if (!timeLeft) {
      clearInterval(countdown);
      progressText.textContent = "Time up!";
      boardRows.forEach(el=> el.classList.add('hidden'))
      startBtn.closest('tr').classList.remove('hidden')
      endScreenMsg.textContent = `You scored ${score} points!`
      startBtn.style.opacity = '1'
      playing = false;
      setHighScore()
      return;
    }
    timeLeft--;
  }, 1000);

  innerBar.animate({ width: "100%" }, 60000, "linear");
});

async function setHighScore(){
  let res = await axios.post('/game-over',{score})
  let highScore = res.data.result
  document.querySelector('#high-score').textContent = highScore;
}