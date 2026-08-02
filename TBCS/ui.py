from pyscript import document
import asyncio

#---VARIABLES---

outputBox = document.querySelector('#outputBox')
inputBox = document.querySelector('#inputBox')

opponent = None
intelligence = None
weights = []

inputQueue = asyncio.Queue()

#---FUNCTIONS---

#this runs once
def setupInputListener():
    submitButton = document.querySelector("#submitButton")
    inputField = document.querySelector("#inputField")
    
    def OnClick(event):
        text = inputField.value
        if text:
            inputField.value = ""
            inputQueue.put_nowait(text)
    submitButton.onclick = OnClick


def Output(text, style="normal"):
    line = document.createElement("div")
    line.className = style
    line.innerText = text
    outputBox.appendChild(line)
    outputBox.scrollTop = outputBox.scrollHeight


def Clear():
    outputBox.innerHTML = ""


async def Ask():  
    return await inputQueue.get()


def CreateInputField():
    inputField = document.createElement("input")
    inputField.id = "inputField"
    inputField.type = "text"
    inputField.placeholder = "type number"
    inputBox.appendChild(inputField)

    submitButton = document.createElement("button")
    submitButton.innerText = "submit"
    submitButton.id = "submitButton"
    inputBox.appendChild(submitButton)



async def DisplayPlay():
    play = document.createElement("button")
    play.innerText = "PLAY"
    play.id = "playButton"
    outputBox.appendChild(play)

    loop = asyncio.get_running_loop()
    pressedPlay = loop.create_future() 

    def PlayClicked(event):
        document.querySelector("#playButton").remove()
        CreateInputField()
        pressedPlay.set_result(True) 

    play.onclick = PlayClicked

    return await pressedPlay


#user is displayed the screen on opponents they would like to fight
#output window shows the opponents stats
#user selects intelligence for opponent
#fight can begin
    #output window presents fight
    #waits for button click to continue code
    #once action has been selected it preforms
    #normal game loop
    #if dead, it will go back, play button in the middle