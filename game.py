#Made this as a school project
#Inspired by Snakes and Ladders
#Runs in a terminal - no fancy gui!!
#Requires live interaction with user
import random

board=[]
level=5# set this to 1 for a normal game
playerPos=[1,1]
dragonPos=[]
playerName=["A","B"]
levelInstr=['''Level 1: The Simple Race

This game consists of two players.
playerA -> A
playerB -> B

On each turn a dice will be rolled. The corresponding player can then move its piece on the
board by that value in either the foreward or the backward direcion.

The objective of the game is to reach the end position before any one else does.
There are teleporters which directly transfer you to that value.             
''','''Level 2: Things get a little spicy...

In this level, everything is almost just as same as the previous level except that the teleporters 
teleport you only in the backward direction. Be careful.''','''Level 3: Mystery

In this level the locations the teleporters teleport to are not displayed. Have fun.''','''Level 4: Dragons!

These are dragons -> ;]

They will wander aimlessly and will kill you (i.e. send you back to the starting position) upon meeting you.
Watch for them.''','''Level 5: The Final Battleground

Okay, there is nothing so special in this level. This is just the last chance for you to win.
To help you, we have also invited a few more dragons.''']
gameEnd=False
def createLevel(lvl):
    global level,board,playerPos,dragonPos
    board=[]
    dragonPos=[]
    playerPos=[1,1]
    freePos=set()
    level=lvl
    for i in range(49):
        board.append({'type':""})
        if(i not in (0,48)):
            freePos.add(i+1)
    board[0]['type']="START"
    board[48]['type']="END"
    if level!=2:
        for i in range(10):
            elems=random.sample(freePos,2)
            freePos.remove(elems[0])
            freePos.remove(elems[1])
            board[elems[0]-1]['type']="GOTO"
            board[elems[0]-1]['gotoval']=elems[1]
            if(level==3):
                board[elems[0]-1]['mystery']=True
            elif level>3 and random.random()>0.4:
                board[elems[0]-1]['mystery']=True
            else:
                board[elems[0]-1]['mystery']=False
        if level==4:
            dragonPos=random.sample(freePos,1)
            freePos.remove(dragonPos[0])
            
        elif level==5:
            dragonPos=random.sample(freePos,4)
            for d in range(4):
                freePos.remove(dragonPos[d])
    else:
        for i in range(48,1,-1):
            if(random.random()<0.2):
                board[i-1]['type']="GOTO"
                board[i-1]['mystery']=False
                board[i-1]['gotoval']=random.randrange(i-1,0,-1)

        
def drawGrid():
    for i in range(8):
        print(('+'+'-'*7)*7+'+')
        if i!=7:
            for line in range(3):
                for col in range(7):
                    n=7-i
                    pos=0
                    if(n%2==1):
                        pos=7*n-6+col
                    else:
                        pos=7*n-col
                    
                    if line==1:
                        print(('|'+str(pos).center(7)),end='')
                    elif line==0:
                        posTitle=board[pos-1]['type']
                        if posTitle=="GOTO":
                            gotoPosNum=str(board[pos-1]["gotoval"])
                            if(board[pos-1]["mystery"]):
                                gotoPosNum="??"
                            posTitle+=' '+gotoPosNum
                        print(('|'+posTitle.center(7)),end='')
                    else:
                        players=''
                        if(playerPos[0]==pos):
                            players+="A"
                        if(playerPos[1]==pos):
                            players+="B"
                        if(pos in dragonPos):
                            players+=";]"
                        print(('|'+players.center(7)),end='')
                print('|')
    print('\n\n')
    input("Press enter to continue...")
                        
def resultPos(pos):
    if pos>49:
        return 49
    if(board[pos-1]["type"]=='GOTO'):
        return resultPos(board[pos-1]["gotoval"])
    else:
        return pos
    
def movePossible(pos,disp):
    return 1<=pos+disp

def movePlayer(pid,disp):
    global playerPos
    if(not gameEnd):
        playerPos[pid]=playerPos[pid]+disp
        drawGrid()
    
        if(playerPos[pid]!=resultPos(playerPos[pid])):
            playerPos[pid]=resultPos(playerPos[pid])
            drawGrid()
            
        if playerPos[pid]>=49:
            playerPos[pid]=49
            playerWins(pid)
        for d in range(len(dragonPos)):
            if playerPos[pid]==dragonPos[d]:
                    playerKilled(pid)

def moveDragons():
    global dragonPos
    if(not gameEnd):
        for d in range(len(dragonPos)):
            disp=0
            if dragonPos[d]<5:
                disp=random.randrange(0,4)
            elif dragonPos[d]>45:
                disp=random.randrange(-3,1)
            else:
                disp=random.randrange(-3,4)
            dragonPos[d]+=disp
            print("Dragons are moving.")
            drawGrid()
            if(dragonPos[d]!=resultPos(dragonPos[d])):
                dragonPos[d]=resultPos(dragonPos[d])
                drawGrid()
                print("Dragons are moving.")
                
            for i in range(2):
                if playerPos[i]==dragonPos[d]:
                    playerKilled(i)
    
def playerKilled(pid):
    global playerPos
    if(not gameEnd):
        playerPos[pid]=1
        print('Player'+playerName[pid]+' was killed by a dragon.')
        drawGrid()

def playerWins(pid):
    global level, gameEnd
    print('Player'+playerName[pid]+" wins this level.")
    if (level<5):
        level+=1
        createLevel(level)
        print(levelInstr[level-1])
        drawGrid()
    else:
        gameEnd=True
    
def takeInput():
    if(not gameEnd):
        direct=input("You can move (f)orewards or (b)ackwards by this amount. Enter end to end the game. Enter f/b:").lower()
        if direct not in ('f','b','end'):
            print("Invalid input!")
            return takeInput()
        return direct

def runGame():
    createLevel(level)
    print(levelInstr[level-1])
    currentPlayer=0
    drawGrid()
    while(not gameEnd):
        
        diceRoll=random.randrange(1,7)
        print("Player"+playerName[currentPlayer]+"'s turn.")
        print("Rolling dice...")
        print("Value on dice is:",diceRoll)
        while(True):
            direct=takeInput()
            if direct=='end':
                print("Ending game.")
                return
            if direct=='b':
                disp=diceRoll*-1
            elif direct=='f':
                disp=diceRoll
            if movePossible(playerPos[currentPlayer],disp):
                movePlayer(currentPlayer,disp)
                break
            else:
                print("Move not possible.")
        if currentPlayer==0:
            currentPlayer=1
        else:
            currentPlayer=0
            moveDragons()
                
runGame()

        
        
