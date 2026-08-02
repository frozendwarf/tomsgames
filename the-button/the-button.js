//timer uses 3d.p.  and  ms
//e.g. 4.569ms

//Variables
const button = document.querySelector('#reaction-button');
const bestTimeLabel = document.querySelector('#best-time');
const attemptsLabel =  document.querySelector('#attempts');

let bestTime = 9999;
let attempts = [];

let buttonStatus = "black"
let playerStatus = "anticipating"

let timeUntilGreen = 0;
let startTimer = 0;
let reactionTime = 0;

let rounds = [];
let currentRound = 0;
let debounce = false;


//Functions
function sleep(ms) {
	return new Promise(function(resolve) {
		setTimeout(resolve, ms);
	});
} 


function GetRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


async function StartGame() {
	currentRound++;
	buttonStatus = "red";
	const style = window.getComputedStyle(button);
	button.style.backgroundColor = "red";
	button.innerText = "";

	timeUntilGreen = GetRandomInt(1000, 10000); // ms

	rounds.push(currentRound);	
	console.log(rounds);
	await sleep(timeUntilGreen);

	if (rounds[rounds.length-1] === currentRound) {
		buttonStatus = "green";
	  button.style.backgroundColor = "green";	
	  startTimer = performance.now();

	}
	
	
	
	
}
async function EndGame(condition) {
	playerStatus = condition;

	const style = window.getComputedStyle(button);
	button.style.backgroundColor = "black";
	
	if (playerStatus === "early") {
		button.innerText = "too early, you suck!";
	} else if (playerStatus === "late") {
		reactionTime  = performance.now() - startTimer;
		button.innerText = "Time: "+reactionTime/1000+"s";
		if (reactionTime  <  bestTime && reactionTime > 0) {
			bestTime  =  reactionTime;
			
			bestTimeLabel.innerText = "BEST: "+bestTime/1000+"s";
		}
	}
	reactionTime = 0;

	debounce = true;
	await sleep(1500);
	button.innerText = "Start";
	buttonStatus = "black"
	playerStatus = "anticipating"
	debounce = false;
}


//RUNTIME
button.addEventListener('click', function() {
	if (debounce) return;
	
	if (buttonStatus === "black") {
		StartGame();
	} else if (buttonStatus === "red") {
		EndGame("early");
	} else if (buttonStatus === "green") {
		EndGame("late");
	}
});



/*Idea
when button is first clicked, start a timer
decide length of how long button will be pressed for
if user presses button before timer, end game, they lose
turn button green after timer
if button pressed after timer, log difference between timer ended
and when pressed
prompt user to restart
*/
