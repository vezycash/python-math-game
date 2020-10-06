#This is a mini math game to train MY math ability with sums

from random import randint
import time
import colorama
from colorama import Fore, Back, Style
import os
import time
import sqlite3

clear, gameDB, conn, level, score = "","","","",""
answered, lives, timeUp, cur, end = "", "", "","", ""
rightAnswers =""

def initializeGame():
    global clear, cur, answered, lives, timeUp, gameDB, conn, level
    global score, end, rightAnswers

    clear = lambda: os.system('cls') #on Windows System

    gameDB = os.environ['USERPROFILE']+"\\test.db"

    clear()
    conn = sqlite3.connect(gameDB)

    cur = conn.cursor()
    colorama.init(autoreset=True)

    level = 1
    score = 0 #levels increments on score of 100, 200, 300...
              #if player has answered 20 or more questions.
              #Necessary because score is reduced on wrong answers.
    answered = 0 #Records how many questions have been answered. Reset on leveling up.
    lives = 3
    timeUp = 12
    rightAnswers = 0
    end = False

    """level = 1
    score = 90 #levels increments on score of 100, 200, 300...
              #if player has answered 20 or more questions.
              #Necessary because score is reduced on wrong answers.
    answered = 10 #Records how many questions have been answered. Reset on leveling up.
    lives = 3"""

def slap():
    import getpass
    global qEnd, qStart
    name = getpass.getpass('')
    clear()
    message = ["You are 90 years old.", "Go and marry.", "- original olodo.", "Mind your self!"]
    message = name.upper() + ", " + message[randint(1,len(message)-1)]
    typeWords(message)
    qStart = time.time()
def godMode():
    import getpass
    password = getpass.getpass('Password:')
    global timeUp
    timeUp = 20
    clear()
    if password != "lord of the rings":
        return
    print("1. Change life")
    print ("2. Change Level")
    choice = input("Enter a number: ")
    choice = int(choice)
    if choice==1:
        newlife = input("Set life: ")
        global lives
        lives = int(newlife)
    elif choice==2:
        newlevel = input("Set level: ")
        global level
        level = int(newlevel)
    elif choice==3:
        timeUp = int(input("Sekke: "))
    clear()
    global qStart
    qStart = time.time()

def typeWords(words,fore=Fore.GREEN):

    words = words.split()
    for char in words:
        time.sleep(0.2)
        print(fore + char, end=' ', flush=True)
    """
    for char in words:
        time.sleep(0.1)
        print(fore + char, end='', flush=True)
    """
    print("")


def newGameScreen():
    print(" ")
    typeWords(" This is a Math Game.")
    typeWords(" You have:")
    print("   ",end="")
    typeWords("• "+str(timeUp)+" seconds per question.")
    print("   ",end="")
    typeWords("• And 3 lives.")
    time.sleep(.5)
    print(" ")
    os.system('pause')
    clear()

def newSum(level):
    if   level ==  1: newNum = randint(1,10)
    elif level ==  2: newNum = randint(5,20)
    elif level ==  3: newNum = randint(10,30)
    elif level ==  4: newNum = randint(15,40)
    elif level ==  5: newNum = randint(20,50)
    elif level ==  6: newNum = randint(25,60)
    elif level ==  7: newNum = randint(30,70)
    elif level ==  8: newNum = randint(35,80)
    elif level ==  9: newNum = randint(40,90)
    elif level == 10: newNum = randint(45,100)
    return newNum

def printScore(state="right"):
    wrong = ""

    if state=="right":
        praise = ["Right!", "Good job!", "Nice!", "Alright!", "Sweet!", "Cool!",
                    "Fantastic!", "Keep it up!", "Wonderful!", "Correct!", "Lovely!"]
        praise = praise[randint(1,len(praise)-1)]
        if score % 7 == 0:
            print(Fore.BLUE + praise, end="")
        elif score % 3 == 0:
            print(Fore.CYAN + praise, end="")
        elif score % 2 == 0:
            print(Fore.GREEN + praise, end="")
        else:
            print(Fore.YELLOW + praise, end="")
    else:
        wrong = Back.YELLOW

    color = ""
    time.sleep(0.5)
    if score % 2 == 0:
        color = Fore.BLUE + Style.BRIGHT
    else:
        color = Fore.MAGENTA + Style.NORMAL
    print("  " + color + wrong + "Score: " + str(score))
    time.sleep(0.5)


def initializeDatabase():
    query = "CREATE TABLE if not exists highscore (NAME TEXT NOT NULL, SCORE INT NOT NULL, LEVEL INT NOT NULL);"
    doesTableExist = conn.execute(query)

    cur.execute("select * from highscore")
    isTableEmpty = cur.fetchall()

    if not isTableEmpty:
        conn.execute("INSERT INTO highscore VALUES('first',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('second',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('third',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('fourth',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('fifth',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('sixth',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('sevent',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('eight',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('ninth',100, 1)")
        conn.execute("INSERT INTO highscore VALUES('tenth',100, 1)")
        conn.commit()


def isHighscore(thisScore):
    #alternative ...score < "+str(score)+" limit 1")
    cur.execute("select rowid from highscore where score < ? limit 1", (thisScore,))
    scoreID = cur.fetchall()
    if scoreID:
        scoreID = scoreID[0][0]
        return scoreID

def addHighScore(previousScoreID, name, score, level):
    #Assign the 10 highscores from the database to an array
    scores = []
    query = "SELECT * FROM highscore"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        scores.append(row)

    #Insert the new score into its position in the array
    newScore = [name, score, level]
    scores.insert(previousScoreID-1, newScore)

    #Replace the database scores with the first 10 items in the array.
    query = "UPDATE highscore set name=?, score = ?, level=? where rowid=?"

    for x in range(0, 10):
        cur.execute (query,(scores[x][0], scores[x][1], scores[x][2], x+1))

    conn.commit()
    #end of addHighScore()

def showHighScore():
    #cur.execute("SELECT * FROM highscore")
    cur.execute ("select rowid, name, SCORE, LEVEL FROM highscore")
    rows = cur.fetchall()
    #value = format("line 1", " >10s")

    typeWords(" High Score", Fore.BLUE)
    print(format("  #", " <7s"), format("Name", " <15s"), "Score Level")
    for row in rows:
        name =  format(row[1]," <15s")
        score = format(str(row[2])," <5s")
        level = format(" "+str(row[3])," <5s")
        rowid = format(str(row[0])," <5s")
        print (" ",rowid, name[0:10], score, level)
        time.sleep(0.2)
    print(" ")



def gameOver():
    time.sleep(2)
    clear()
    typeWords(" GAME OVER", Fore.RED)
    typeWords(" You Scored: " + str(score))
    if isHighscore(score):
        print(" ")
        typeWords("Congratulations!!! You got a high score")
        print("")
        playerName = input("Enter your Name: ")
        print("")
        addHighScore(isHighscore(score), playerName, score, level)
    time.sleep(2)
    showHighScore()
    conn.close()
    os.system('pause')
    clear()
    startNewGame = ""
    while startNewGame =="":
        startNewGame = input("Start new Game? (Yes or No): ")
        startNewGame= startNewGame.lower()
        if startNewGame == "y" or startNewGame == "yes":
            newGame()
        elif startNewGame == 'n' or startNewGame == 'no':
            exit()
        else:
            startNewGame = ""

def newGame():
    initializeGame()
    initializeDatabase()
    newGameScreen()

newGame()

while not end:
    if rightAnswers > 15:
        wordA = newSum(level+3)
        wordB = newSum(level+3)
    elif rightAnswers >= 10:
        wordA = newSum(level+2)
        wordB = newSum(level+2)
    elif rightAnswers >= 5:
        wordA = newSum(level+1)
        wordB = newSum(level+1)
    else:
        wordA = newSum(level)
        wordB = newSum(level)

    correctAnswer = wordA + wordB
    if lives <=0: gameOver()

    qStart = time.time()
    answer = input("What is " + str(wordA) + " + " + str(wordB) + "? ")
    flag = answer
    flag = str(flag)
    if flag.lower() == "godmode": godMode()
    if flag.lower() == "slap": slap()
    answer = ''.join([n for n in answer if n.isdigit()])
    while answer == "":
        answer = input("What is " + str(wordA) + " + " + str(wordB) + "? ")
    qEnd = time.time()
    elapsed = int(qEnd - qStart)

    if elapsed > timeUp:
        lives -= 1
        rightAnswers = 0
        print("")
        print(Style.NORMAL +Fore.RED + " Too slow.")
        print(Fore.MAGENTA + " Respond in " + str(timeUp)+ " seconds!")
        if lives > 1:
            print(" "+Style.NORMAL +Fore.RED + str(lives) + " lives left.")
        elif lives ==1:
            print(Style.NORMAL + Back.WHITE + Fore.RED + " Last life!")
        print("")
        os.system('pause')
        clear()
    else:
        answer = ''.join([n for n in answer if n.isdigit()])

        if answer.isdigit(): answer = int(answer)

        if answer == 0:
            end = True
        elif correctAnswer == answer:
            score +=5
            rightAnswers+=1
            printScore("right")
        else:
            score -=5
            lives -=1
            rightAnswers = 0
            if score<=0: score = 0  #makes sure the score never goes to negative
            time.sleep(.1)
            print("  " + Back.MAGENTA + "Answer is " + Back.MAGENTA + str(correctAnswer)+ Back.MAGENTA)
            time.sleep(0.2)
            printScore("wrong")
            if lives ==1:
                typeWords ("  Last Life!", Fore.RED)
            elif lives <= 0:
                gameOver()
            else:
                if lives<= 3:
                    typeWords("  "+str(lives )+" lives left.")
            time.sleep(1)
        #This handles leveling up.
        answered +=1

    if score % 100 == 0 and answered > 10:
        level = int(score/100+1)
        answered = 0
        rightAnswers = 0
        if lives < 3:
            lives +=1
            lifeAdded = True
        else: lifeAdded = False
        time.sleep(1)
        clear()
        print("  "+Back.MAGENTA + " "*32)
        print("  "+Back.MAGENTA + " Congrats."+" "*22)
        print("  " + Back.MAGENTA +" You've reached level:" + str(level)+" "*9)
        if lifeAdded:
            print("  " + Fore.MAGENTA + Back.WHITE + " 1 Life added: You have " + Fore.RED + str(lives)+ " lives"+" ")
        else:
            print("  " + Fore.MAGENTA + Back.WHITE + " You have " + Fore.RED + "♥ ♥ ♥"+" "*17)
        time.sleep(4)
        clear()

conn.close()