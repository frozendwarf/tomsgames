#Text based combat system

#Sir, this is a wendy's inspired gameplay
#the game was funny fun on repl.it in 2022 and I remember me and my friends playing it alot
#so i decided to make a custom combat system, which is imo better

#--------------------------------------------------------------------

from pyscript import document
import random
import ui
import asyncio


#-----------------------
#-------Variables-------
#-----------------------


damage = {
    "LightAtkMin" : 2,
    "LightAtkMax" : 3,

    "HeavyAtkMin" : 6,
    "HeavyAtkMax" : 8,
   
    "HealMin" : 3,
    "HealMax" : 5,

    "CounterAtkMin": 1,
    "CounterAtkMax": 2
}

stamina = {
    "lightAttack" : -1,
    "heavyAttack" : -5,
    "defend" : 1,
    "focus" : 2,
    "heal" : -4,
    "counter" : -2
}

actions = ("lightAttack", "heavyAttack", "defend", "focus", "heal", "counter") #which order of moves the user is displayed
actionsOrder = ("counter", "defend", "focus", "heal", "lightAttack", "heavyAttack") #for display which goes first


staggerNerf = 0.5 #outgoing attacks have 0.5x damage for 2 turns
focusBuff = 1.5 #outgoing attacks deal  1.5x damage

      

#-----------------------
#-------Functions-------
#-----------------------


async def Legend():
    ui.Output("This is the legend for the system. \n \n")
    ui.Output("--Light Attack--")
    ui.Output("Base Damage = 2-3, SP = -1 \n")
    ui.Output("--Heavy Attack--")
    ui.Output("Base Damage = 6-8, SP = -5 \n")
    ui.Output("--Defend--")
    ui.Output("Incoming damage is halved, SP = +1 \n")
    ui.Output("--Focus--")
    ui.Output("Focus boost = 1.5x, SP = +2")
    ui.Output("For the next turn, the next attack will deal 1.5x damage, if an attack is not used, it does nothing")
    ui.Output("Attacking moves focus buffs: Light Attack, Heavy Attack, Counter \n")
    ui.Output("--Heal--")
    ui.Output("HP gain = 3-5, SP = -4 \n")
    ui.Output("--Counter--")
    ui.Output("Counters the incoming attack. If used and the opponent uses light attack or heavy attack, damage is negated.")
    ui.Output("It also deals a small base damage of 1-2.")
    ui.Output("Finally it gives the effect 'staggered' to the opponent for 2 turns, which halves their damage. \n")
    await asyncio.sleep(3)
    ui.Output("Now type your move: ")


            
def TickDownEffects(actor):
    for key, value in actor.status.items():
        if value > 0:
            actor.status[key] -= 1



async def GetPlayerPick(player):
        ValidChoice = False
        PlayerPick = None
        while not ValidChoice:
            try:
                Choice = await ui.Ask()
                if Choice == "legend":
                    await Legend()
                    Choice = int(await ui.Ask())
                Choice = int(Choice)
                if 1 <= Choice <= len(actions): #from the 6 actions
                    PlayerPick = actions[Choice-1]
                    
                    if stamina[PlayerPick]*-1 <= player.stamina: #checks if there is enogh stamina
                        ValidChoice = True
                    else:
                        ui.Output("not enough stamina. Try again:")
                else:
                    ui.Output("you fool, there is no action "+str(Choice)+", I can't make one up, I don't make the rules. Try again:")
            except ValueError:
                ui.Output("You should probably try typing in the numbers corresponding to the action, try again:")
        return PlayerPick

#OLD completely Random
def GetEnemyPick(enemy):
    ValidChoice = False
    EnemyPick = None
    while not ValidChoice:
        EnemyPick = actions[random.randint(0,5)]
        if stamina[EnemyPick]*-1 <= enemy.stamina: #checks if there is enough stamina
            ValidChoice = True
                    
    return EnemyPick




async def ExecutePlayerAndEnemyActions(player, PlayerPick, enemy, EnemyPick):
     
     for order, action in enumerate(actionsOrder):
            if PlayerPick == action:
                PlayerAction = getattr(player, PlayerPick)   
                if action == "lightAttack" or action == "heavyAttack":
                    await PlayerAction(enemy)
                else:
                    await PlayerAction()

            if EnemyPick == action:
                 EnemyAction = getattr(enemy, EnemyPick)
                 if action == "lightAttack" or action == "heavyAttack":
                    await EnemyAction(player)
                 else:
                    await EnemyAction()

def DisplayStats(actor):
    ui.Output(actor.name+": "+str(actor.hp)+"/"+str(actor.max_hp)+" HP, "+str(actor.stamina)+"/"+str(actor.max_stamina)+" SP")
    if actor.status["Focused"] > 0:
        ui.Output("Focused x"+str(actor.status["Focused"]))
    if actor.status["Staggered"] > 0:
        ui.Output("Staggered x"+str(actor.status["Staggered"]))
        

def Display(player, enemy):
    ui.Output("\n")
    ui.Output("Type 'legend' for details on each move.")
    ui.Output("\n")
    DisplayStats(player)
    ui.Output("\n")
    DisplayStats(enemy)
    ui.Output("\n")
    ui.Output("\n")
    ui.Output("Here are your options:")
    ui.Output(" 1. Light Attack [1 SP] \n 2. Heavy Attack [5 SP] \n 3. Defend [+1 SP] \n 4. Focus [+2 SP] \n 5. Heal [4 SP] \n 6. Counter [2 SP]")


#What should be done:
        #1Display Options
        #2get enemy and player picks
        #3make sure they are both valid
        #4execute in this order:
            #dodge, heal, focus, defend, light, heavy
        #5 tick down effects (like dodged, staggered)
async def fight(player, enemy):
    
    while player.isAlive() and enemy.isAlive():
        ui.Clear()
        Display(player, enemy)
    
        PlayerPick = await GetPlayerPick(player) 
        EnemyPick = enemy.decide(player) #enemy also considers itself aswell as the player when making a choice

        await asyncio.sleep(0.5)
        
        await ExecutePlayerAndEnemyActions(player, PlayerPick, enemy, EnemyPick)
        
        TickDownEffects(player)
        TickDownEffects(enemy)
        
        await asyncio.sleep(3)

    ui.Output("Game Over")
    if player.isAlive():
        ui.Output(enemy.name+" died! You WON!")
    else:
        ui.Output("You died")
    await asyncio.sleep(10)
    


def CounterOpponent(defender, countered):
    ui.Output(defender.name+" countered the attack!")
    Atkdamage = random.randint(damage["CounterAtkMin"],damage["CounterAtkMax"])
    Atkdamage *= defender.damageMultiplier
    if defender.status["Focused"] > 0:
        Atkdamage *= focusBuff
    Atkdamage = round(Atkdamage)
    countered.hp -= Atkdamage
    
    countered.status["Staggered"] = 3 #includes turn set, 2+1=3
    ui.Output(defender.name+" has delt "+str(Atkdamage)+" damage")
    ui.Output(countered.name+" has also been staggered! They now deal less damage for 2 turns!")
    ui.Output("\n")

#---ENEMY AI Calculation Functions
def lightAtkScore(enemy, player):
    if enemy.stamina <= stamina["lightAttack"]*-1:
        return 0
    bias = 1
    if player.stamina < 2:
        bias += 2
    Php = player.hp/player.max_hp

    score = 1/Php + enemy.status["Focused"] - enemy.status["Staggered"] + bias
    weight = enemy.weights["lightAttack"]
    return score * weight 
    
def heavyAtkScore(enemy, player):
    if enemy.stamina <= stamina["heavyAttack"]*-1:
        return 0
    bias = 3
    if player.stamina < 2:
        bias += 2

    Esp = enemy.stamina/enemy.max_stamina
    Psp = player.stamina/player.max_stamina

    if Psp == 0:
        Psp = 0.01

    score = 2*Esp * 2*enemy.status["Focused"] * 0.5/Psp - 2*enemy.status["Staggered"] + bias
    weight = enemy.weights["heavyAttack"]             
    return score * weight
        
def defendScore(enemy, player):
    if enemy.stamina <= stamina["defend"]*-1:
        return 0
    if player.stamina == 0:
        return 0
    weight = 1
    Esp = enemy.stamina/enemy.max_stamina
    if Esp == 1:
        weight *= 0.5
    if Esp == 0:
        Esp = 0.01
    Ehp = enemy.hp/enemy.max_hp
            
    weight *= enemy.weights["defend"]

    score = 1/Ehp + 1/Esp
    return score * weight
        
def focusScore(enemy):        
    if enemy.stamina <= stamina["focus"]*-1:
        return 0
    bias = 0
    Esp = enemy.stamina/enemy.max_stamina
    Ehp = enemy.hp/enemy.max_hp
    if Ehp > 0.2:
        bias += 1
    else:
        bias -= 1
    if Esp == 1:
        bias -= 2
    elif Esp == 0:
        Esp = 0.01
    if enemy.status["Focused"] == 0: #tried to make it so with 0 focus it will probably attack but maybe decieve the user and focus
        bias += 2
            
    weight = enemy.weights["focus"]
    score = 1/Esp + bias
    return score * weight

def healScore(enemy):
    if enemy.stamina <= stamina["heal"]*-1:
        return 0
    Ehp = enemy.hp/enemy.max_hp
    if Ehp == 1: #if hp is max, there is no need to heal
        return 0
     
    score =  2*(1/Ehp)
    weight = enemy.weights["heal"]
    return score * weight
        
def counterScore(enemy, player):
    if enemy.stamina <= stamina["counter"]*-1:
        return 0
    if player.stamina == 0:
        return 0
    bias = 1
    Psp = player.stamina/player.max_stamina
    if player.status["Focused"] and player.stamina >= 5:
        bias += 3
    if player.stamina >= 5:
        bias += 2
    score = Psp + player.status["Focused"] + bias
    weight = enemy.weights["counter"]  
    return score * weight 


#-----------------------
#--------Classes--------
#-----------------------
class Actor:
    def __init__(self, name, hp, stamina, damageMultiplier, accuracy):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.stamina = stamina
        self.max_stamina = stamina    
        self.damageMultiplier = damageMultiplier
        self.accuracy = accuracy
        self.intelligence = None
        self.status = {
            "Guard" : 0,
            "Focused" : 0,
            "Counter" : 0,
            "Staggered" : 0
        }
        self.weights = {
            "lightAttack" : 1,
            "heavyAttack" : 1,
            "defend" : 1,
            "focus" : 1,
            "heal" : 1,
            "counter" : 1
        }

    def isAlive(self):
        return self.hp > 0

    def setWeights(self, **weights):
        weightsVerified = 0
        for weight in weights:
            for action in actions:
                if weight == action:
                    weightsVerified += 1
        if not(weightsVerified == len(weights)):
            raise Exception("Not all the arguements are weights for actual actions")
            
        self.weights = weights

    def setIntelligence(self, level):
        if isinstance(level, int):
            if level < 6:
                self.intelligence = level
            else:
                raise Exception("Intelligence level above 6, the max is 6")
        else:
            raise Exception("this intelligence level is invalid")
            
        
        
    async def lightAttack(self, target):

        ui.Output(self.name+" used a light attack on "+target.name)
        await asyncio.sleep(1)
        ui.Output("it cost "+str(-1 * stamina["lightAttack"])+" stamina")
        ui.Output("\n")
        
        self.stamina += stamina["lightAttack"]
        
        if self.accuracy < random.random():
            await asyncio.sleep(1)
            ui.Output(self.name+" missed their attack!")
            return
        if target.status["Counter"] > 0:
            await asyncio.sleep(1)
            if target.accuracy > random.random():
                CounterOpponent(target, self)
                return
            else:
                ui.Output(target.name+" tried to counter attack, but it failed!")
            
            
        Atkdamage = random.randint(damage["LightAtkMin"],damage["LightAtkMax"])
        Atkdamage = Atkdamage * self.damageMultiplier

    
        if self.status["Focused"] > 0:
            Atkdamage *= focusBuff
        if self.status["Staggered"]> 0:
            Atkdamage *= staggerNerf
        if target.status["Guard"] > 0:
            Atkdamage *= 0.5
        Atkdamage = round(Atkdamage)
        target.hp -= Atkdamage
        
        if target.status["Guard"]:
            await asyncio.sleep(1)
            ui.Output(target.name+" defended the attack! "+self.name+" had their damage halved!")
            ui.Output("\n")
        if self.status["Focused"]:
            await asyncio.sleep(1)
            ui.Output(self.name+" used focus, so the damage has increased by "+str(focusBuff)+"x!")
            ui.Output("\n")
        await asyncio.sleep(1)
        ui.Output("it did "+str(Atkdamage)+" damage.")
        ui.Output("\n")
        await asyncio.sleep(1)


    async def heavyAttack(self, target):
        
        ui.Output(self.name+" used a heavy attack on "+target.name+"!")
        await asyncio.sleep(1)
        ui.Output("it cost "+str(-1 * stamina["heavyAttack"])+" stamina")
        ui.Output("\n")
        
        self.stamina += stamina["heavyAttack"]
        if self.accuracy-0.1 < random.random():
            await asyncio.sleep(1)
            ui.Output(self.name+" missed their attack!")
            return
        if target.status["Counter"] > 0:
            await asyncio.sleep(1)
            if target.accuracy > random.random():
                CounterOpponent(target, self)
                return
            else:
                ui.Output(target.name+" tried to counter attack, but it failed!")
        
        Atkdamage = random.randint(damage["HeavyAtkMin"],damage["HeavyAtkMax"])
        Atkdamage = Atkdamage * self.damageMultiplier

        if self.status["Focused"]:
            Atkdamage *= focusBuff
        if self.status["Staggered"]:
            Atkdamage *= staggerNerf
        if target.status["Guard"]:
            Atkdamage *= 0.5
        Atkdamage = round(Atkdamage)
        target.hp -= Atkdamage


        if target.status["Guard"]:
            await asyncio.sleep(1)
            ui.Output(target.name+" defended the attack!"+ self.name+" had their damage halved!")
            ui.Output("\n")
        if self.status["Focused"]:
            await asyncio.sleep(1)
            ui.Output(self.name+" used focus, so the damage has increased by "+str(focusBuff)+"x!")
            ui.Output("\n")
        await asyncio.sleep(1)
        ui.Output("it did "+str(Atkdamage)+" damage.")
        ui.Output("\n")
        await asyncio.sleep(1)

        
        

    async def defend(self):
        ui.Output(self.name+" used defend")
        await asyncio.sleep(1)
        ui.Output("it gained "+str(stamina["defend"])+" stamina")
        await asyncio.sleep(1)
        ui.Output(self.name+" will be able to defend an attack this turn")
        ui.Output("\n")

        
        if self.stamina + stamina["defend"] <= self.max_stamina:
            self.stamina += stamina["defend"]
        else:
            self.stamina = self.max_stamina
        self.status["Guard"] = 1 

    async def focus(self):
        ui.Output(self.name+" used focus")
        await asyncio.sleep(1)
        ui.Output("it gained "+str(stamina["focus"])+" stamina")
        await asyncio.sleep(1)
        ui.Output(self.name+" will be able to deal "+str(focusBuff)+"x damage the next turn")
        ui.Output("\n")
        
        if self.stamina + stamina["focus"] <= self.max_stamina:
            self.stamina += stamina["focus"]
        else:
            self.stamina = self.max_stamina
        self.status["Focused"] = 2 #includes turn set, 1+1=2

    async def heal(self):
        ui.Output(self.name+" used heal")
        await asyncio.sleep(1)
        ui.Output("it cost"+str(-1 * stamina["heal"])+" stamina")
        ui.Output("\n")

        self.stamina += stamina["heal"]
        healAmount = random.randint(damage["HealMin"],damage["HealMax"])
        
        if self.hp + healAmount <= self.max_hp:
            self.hp += healAmount
            ui.Output(self.name+" gained "+str(healAmount)+" hp")
        else:
            self.hp = self.max_hp
            ui.Output(self.name+" is at MAX hp!")

    async def counter(self):
        ui.Output(self.name+" used counter")
        await asyncio.sleep(1)
        ui.Output("it costed "+str(-1 * stamina["counter"])+" stamina")
        ui.Output("\n")

        self.stamina += stamina["counter"]
        self.status["Counter"] = 1
        await asyncio.sleep(1)
        ui.Output(self.name+" will be able to counter an attack this turn")
        ui.Output("\n")

    def decide(enemy, player):
        if enemy.weights is None:
            raise Exception("Enemy does not have any state weights, set their weights")
        if enemy.intelligence is None:
            raise Exception("Enemy intelligence has not been set!")

        scores = {
            "lightAttack" : lightAtkScore(enemy,player),
            "heavyAttack" : heavyAtkScore(enemy, player),
            "defend" : defendScore(enemy, player),
            "focus" : focusScore(enemy),
            "heal" : healScore(enemy),
            "counter" : counterScore(enemy, player)
        }
        attacks = []
        weights = []
        for i in scores:
            attacks.append(i)
            weights.append(scores[i])

        
        if enemy.intelligence > 1:
            for i in range(0, enemy.intelligence//2):
                #swap 1st best move with worst move
                #swap worst move with best
                #then swarp 2nd best with 2nd to worst, etc
                
                indexes = range(len(weights)) 
                sortedIndices = sorted(indexes, key=lambda k: weights[k], reverse=True)
                
                idxBest = sortedIndices[i]
                idxWorst = sortedIndices[enemy.intelligence-1 - i]
                weights[idxBest], weights[idxWorst] = weights[idxWorst], weights[idxBest]
                

                
        return random.choices(attacks, weights=weights)[0]
        
    
#-----------------------
#--------Runtime--------
#-----------------------

#Actor(hp, sp, damageMultiplier, accuracy) -- makes actor
#setIntelligence -- sets intelligence (intelligence-1 as its a list)
#setWeights -- sets weights for certain moves
#fight -- puts two actors in a fight
opponents = {
    "dummy" : Actor("dummy", 15, 12, 0.8, 0.9),
    "doppelganger": Actor("Doppelganger", 20, 10, 1 ,0.9),
    "dayem" : Actor("Dayem", 16, 50, 4, 0.75),

}

async def main():
    document.querySelector("#loading").remove()
    


    player = Actor("Player", 20, 10, 1, 0.9)
   
    while True:
        await ui.DisplayPlay()
        ui.setupInputListener()
        ui.Clear()   
        ui.Output("choose your opponent: \n dummy \n doppelganger \n dayem")
        opponent = await ui.Ask()
        ui.Clear()

        ui.Output("choose enemy intelligence, where 1 is smartest and 6 is dumbest")
        intelligence = await ui.Ask()
        ui.Clear()
        opponent.setIntelligence(int(intelligence))
        await fight(player, opponents[opponent])
    

asyncio.ensure_future(main())



