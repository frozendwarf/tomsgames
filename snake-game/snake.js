//to do:
/*
	-add grids, draw square (grey and black) to guide user when to turn
	-change apple spawning, make a list of spawnable squares,
		if unspawnable, remove from the list
	-SCORE
*/

//Global Variables
const screen = document.getElementById("screen");
const ctx = screen.getContext("2d");

const tickRate = 4.5; //ticks per second
const gridSize = 25;
const numOfSquares = screen.width/gridSize *  screen.height/gridSize;
console.log(numOfSquares);

const darkBlue = "rgb(50,50,255)";
const lightBlue = "rgb(100,100,255)";


let player = null;
const snake = []; //snake squares basically
let directionQueue = [];
const maxDirQueue  = 3
let squareIndex = null;
let apple = null;

let inGame = true;


const playerKeys = {
	"ArrowUp" : "up",
	"ArrowLeft": "left",
	"ArrowDown" : "down",
	"ArrowRight" : "right",
	
	"w" : "up",
	"a" : "left",
	"s" : "down",
	"d" : "right",
}

//Classes
class Square {
    constructor(id, x, y, width, height, color, direction) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.color = color;
        this.direction = direction;
    }

    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
}


//Functions
function sleep(ms) {
	return new Promise(function(resolve) {
		setTimeout(resolve, ms);
	});
} 

function GetRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function SnapAppleToGrid(apple) {
	apple.x = Math.floor(apple.x / gridSize) * gridSize;apple.x = Math.round(apple.x / gridSize) * gridSize;
	apple.y = Math.floor(apple.y / gridSize) * gridSize;
}

function EndGame(condition) {
	inGame = false;
	directionQueue = ["undefined"];
	
	const button  = document.createElement("button")
	button.addEventListener("click", function() {
		player.x = gridSize;
		player.y = gridSize;
		snake.splice(1, snake.length)
	
		
		button.remove();
		SpawnApple();
		inGame  =  true;
		updateScreen();
	});
	
	if (condition === "win")  {
		button.innerText = "CONGRATS!, You WIN! Well done, Retry?"
	} else  {		
		button.innerText = "you lose! Retry?"		
	}
	document.getElementById('gamePage').appendChild(button);
}

function CheckForCollisons()  {
	//loop through each square in snake, check if position meets anything
	
	for (const square1 of snake) {
		for (const square2 of snake) {
			
			if (square1.x === apple.x && square1.y === apple.y) {
				return "apple"
			}
			
			if (square1 === square2) continue; 
			if (square1.x === square2.x && square1.y === square2.y) {
				return "snake"
			}
		}
	}
	return false;
}


function SpawnApple()  {
		
	let validSpawn = false;
	let tempApple;
	
	while (!validSpawn) {
		let x = GetRandomInt(0,500);
		let y = GetRandomInt(0,500); 
		
		tempApple = new Square( "apple", x, y, 
		gridSize, gridSize, "red")
		SnapAppleToGrid(tempApple);
		
		 let collision = false;
        for (const square of snake) {
            if (square.x === tempApple.x && square.y === tempApple.y) {
                collision = true;
                console.log("apple spawned on snake");
                break;
            }
        }

        if (!collision) {
            validSpawn = true;
        }
	}
	apple = tempApple;
	return apple;
}

function ExtendSnake() {
	let x  = null, y = null;
	let tail = snake[snake.length-1]
	
	if (tail["direction"] == "up") y = player.y + gridSize;
	if (tail["direction"] == "down") y  =  player.y - gridSize;
	if (tail["direction"] == "left") x = player.x + gridSize;
	if (tail["direction"] == "right") x =  player.x - gridSize;
		
	snake.push(new Square(
	"player", x, y, 
	gridSize, gridSize, lightBlue, player.direction));
	if (snake.length === numOfSquares) {
		EndGame("win");
	}
}

function CreateMap() {
	ctx.fillStyle = "black";
	const sideCount = Math.sqrt(numOfSquares);
	for (let i = 0; i < sideCount; i++) {
		for (let j = 0; j < sideCount; j++)  {
			if (j % 2 === 0) ctx.fillstyle = "grey";
			else ctx.fillStyle = "black";
			ctx.fillRect(i * gridSize, j * gridSize, gridSize, gridSize);
		}
	}
	//ctx.fillRect(0, 0, screen.width, screen.height);
	
}

function InBoundary(x, y) {
	if (-gridSize < x && x < screen.width) {
		if (-gridSize < y && y < screen.width) {
			return true;
		}
	}
	return false;
}
  

function ChangePlayerDirection(key) {
	if (directionQueue.length === maxDirQueue) return;
	direction = playerKeys[key];
	
	const lastDirection = directionQueue.at(-1);
	
	if (direction === "up"  && lastDirection === "down") return;
	if (direction === "right"  && lastDirection === "left") return;
	if (direction === "down"  && lastDirection === "up") return;
	if (direction === "left"  && lastDirection === "right") return;

	
	directionQueue.push(direction);
	console.log(directionQueue);
}



//RUNTIME
player = new Square("player",  200, 200, gridSize, gridSize, darkBlue);
snake.push(player);
apple = SpawnApple();


document.addEventListener('keydown', function(event) {
	if (inGame) ChangePlayerDirection(event.key);
})

async function updateScreen() {
    while (inGame) {
		
        CreateMap();
        
        //every square gets position from  previous square
       for (let i = snake.length - 1; i > 0; i--) {
            snake[i].x = snake[i - 1].x;
            snake[i].y = snake[i - 1].y;
        }    
       
		//changes player direction by first in queue, updates if old
		player.direction = directionQueue[0];
		if (directionQueue.length > 1) directionQueue.shift();
		
		//changes player pos based on direction
		if (player["direction"] == "up") player.y -= gridSize;
		if (player["direction"] == "down") player.y += gridSize;
		if (player["direction"] == "left") player.x -= gridSize;
		if (player["direction"] == "right") player.x += gridSize;
		
		
        for (const square of snake)  {
			square.draw(ctx);
		}   
		
		apple.draw(ctx);
        
        if (!InBoundary(player.x, player.y)) EndGame("loss");
        const collision = CheckForCollisons();
		if (collision === "apple") {
			SpawnApple();
			ExtendSnake();
		} else if (collision === "snake") EndGame("loss");
		
        await sleep(1000/tickRate);
    }
}
updateScreen();
