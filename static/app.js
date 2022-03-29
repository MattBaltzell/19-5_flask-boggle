const form = document.getElementById('form')
const guess = document.getElementById('word')
const feedback = document.getElementById('feedback')

form.addEventListener('submit', guessHandler)

async function guessHandler(e){
    e.preventDefault();
    feedback.classList.remove('faded')
    let word = guess.value

    let res = await axios.get('http://127.0.0.1:5000/check-word',{params: {word}})
    let status = res.data.result
    guess.value = ''
    feedback.textContent = status.split('-').join(' ').toUpperCase()
    if(status !== 'ok'){
        feedback.classList.add('red')
    } else{feedback.classList.remove('red')}

    feedback.classList.add('faded')
    
}
