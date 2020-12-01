"""This is the game of War. The deck is shuffled and the split between two players. Players then draw: highest card takes both cards.
If the drawn cards are the same, players draw one card face down and one card face up. Continue until highest card takes all drawn cards.
The game ends when the winner takes the entire deck.
There are three versions:
1) Play the game in the terminal
2) Simulate game play. Wins are counted using a string for practice-
It would definitely quicker not to cast to str, and even better to do this with a library
3) In the TK canvas

Zoe Berling GameofWar.py COMPLETE 10/14/2020"""

import tkinter
import time
import random


CANVAS_WIDTH = 900
CANVAS_HEIGHT = 800
CARDS_IN_HAND = 4
CARD_HEIGHT = 130
CARD_WIDTH = 100


def main():
    """Pick Game Version: 1 = terminal 2 = histogram (string) 3 = TK canvas"""
    # create the deck of cards
    gameVersion = int(input(f' Choose 1 for terminal, 2 for histogram, 3 for Canvas. '))

    suits = ['grey', 'pink', 'red', 'white']

    # List better suited for gameVersion 1
    # suits = ['hearts', 'diamonds', 'spades', 'clubs']

    values = 13
    # Create the deck
    deck = createDeck(suits, values)
    playerOne = []
    playerTwo = []
    dumpOne = []
    dumpTwo = []
    # split deck
    splitDeck(playerOne, playerTwo, deck)
    # create canvas
    histogramresults = ''

    # Example list to showcase the Canvas
    # playerOne = [("pink", 3), ("pink", 11), ("red", 10), ("white", 12), ("pink", 13)]
    # playerTwo = [("pink", 3), ("red", 0), ("pink", 1), ("white", 2), ("pink", 3), ("red", 4), ("red", 5), ("red", 6)]
    # dumpOne = []
    # dumpTwo = []

    # choose game play

    # play through terminal
    if gameVersion == 1:
        print(f'Welcome to the Game of War!')
        print(f'Player {playGame(gameVersion, playerOne, playerTwo, dumpOne, dumpTwo)} wins!')

    # simulate play and evaluate
    if gameVersion == 2:
        numberTimes = int(input(f'How many times would you like to simulate the game? '))
        for i in range(numberTimes):
            deck = createDeck(suits, values)
            splitDeck(playerOne, playerTwo, deck)
            histogramresults += str((playGame(gameVersion, playerOne, playerTwo, dumpOne, dumpTwo)))
        print(f'Player 1 wins : Player 2 wins = {histogramresults.count("1")}:{histogramresults.count("2")}')

    # play on canvas
    if gameVersion == 3:
        # trying to save mouse clicks into a usable form: update- it didn't work this way
        # mouseClickDict = {'click': (100, 100)}

        canvas = makeCanvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Game of War')

        canvas.bind("<Button-1>", lambda e: mousePress(e, canvas, gameVersion, playerOne, playerTwo, dumpOne, dumpTwo))  # I got this from my last project: binds events to mouse clicks
    # draw player 1 cards on the left and create space for their dump cards (the user)
        drawCards(canvas, dumpOne, playerOne, -1)

    # draw player 2 cards on the right and create space for their dump cards. (the computer)
        drawCards(canvas, dumpTwo, playerTwo, 1)

        playPrompt = "Pick a card."
        canvas.create_text(CANVAS_WIDTH / 2, (CANVAS_HEIGHT/2)+CARD_HEIGHT, font='Arial 20 italic', text=playPrompt, tags='play')

        canvas.update()

    # Check Mouse Pressed function for canvas related game play code

        canvas.mainloop()


# Canvas Functions go here


def drawCards(canvas, dump, player, a):
    """creates rectangles to display the player cards on the canvas: the computer's cards are blue to hide the value"""

    # elements = []
    for i in range(CARDS_IN_HAND):
        x = (CANVAS_WIDTH / 2) - (CARD_WIDTH / 2) + a * (3.75 * CARD_WIDTH)
        y = (CANVAS_HEIGHT/2) - (CARD_HEIGHT) + (i * CARD_HEIGHT)


        if a < 0:

            #edge case where player has fewer than 4 cards
            if i + 1 > len(player):
                color = 'white'
                textvalue = ''
            else:
                color = player[i][0]
                textvalue = str(player[i][1])

        else:
            if i + 1 > len(player):
                color = 'white'
                textvalue = ''
            else:
                color = 'blue'
                textvalue = ''

        canvas.create_rectangle(x, y, x + CARD_WIDTH, y + CARD_HEIGHT, fill=color)
        canvas.create_text(x + (CARD_WIDTH/2), y + (CARD_HEIGHT/2), font='Arial 18 bold', text=textvalue)

    playerCount = len(player)
    canvas.create_text(x + (CARD_WIDTH / 2), CANVAS_HEIGHT / 3.5, font='Arial 16 bold', text=f'{playerCount} cards', tags='count')

    # create the dump piles
    for i in range(len(dump)):
        x = (CANVAS_WIDTH / 2) - ((CARD_WIDTH + 5) / 2) + a * (2 * (CARD_WIDTH+5))
        y = (CANVAS_HEIGHT / 5.5) - (CARD_HEIGHT) + (i * CARD_HEIGHT)

        color = dump[i][0]
        textvalue = str(dump[i][1])

        canvas.create_rectangle(x, y, x + CARD_WIDTH, y + CARD_HEIGHT, fill=color, tags='dump')
        canvas.create_text(x + (CARD_WIDTH / 2), y + (CARD_HEIGHT / 2), font='Arial 18 bold', text=textvalue, tags='dump')






def makeCanvas(width, height, title):
    """make the window that contains the canvas"""

    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)

    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly. I got this from my last project
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off. I got this from my last project

    return canvas


"""Dear god please help"""
def mousePress(event, canvas, gameVersion, playerOne, playerTwo, dumpOne, dumpTwo):
    """Track mouse clicks to play the game on the tkinter canvas"""
    # print('mouse pressed', event.x, event.y)
    x = event.x
    y = event.y
    found = canvas.find_overlapping(x, y, x, y)

    if found[0] > 0:

        canvas.delete('count')
        canvas.update()

    # maybe build everything inside this function?

        revealCards(gameVersion, playerOne, playerTwo, dumpOne, dumpTwo, found)

        # redraw the canvas for user (player 1) on the left
        drawCards(canvas, dumpOne, playerOne, -1)
        # draw player 2 cards on the right and create space for their dump cards. (the computer)
        drawCards(canvas, dumpTwo, playerTwo, 1)

        canvas.update()
        time.sleep(2)


        # if this IS true, it IS a war situation, so more cards need to be appended before comparing the dump decks.
        if len(dumpOne) > 1 and len(dumpOne) % 3 != 0:
            canvas.delete('war')
            canvas.update()



        else:
            checkPoint = (compareCards(gameVersion, playerOne, playerTwo, dumpOne, dumpTwo, found))
            canvas.delete('count')
            canvas.delete('dump')

            if checkPoint < 3:
                canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/3, font='Arial 20 bold', text=f'Player {checkPoint} wins this round.', tags='round')
                canvas.update()

            # redraw the canvas for user (player 1) on the left
            drawCards(canvas, dumpOne, playerOne, -1)

            # draw player 2 cards on the right and create space for their dump cards. (the computer)
            drawCards(canvas, dumpTwo, playerTwo, 1)

            canvas.update()
            time.sleep(2)



            if checkPoint == 3:
                warText = "It's WAR! Dump a card from your hand."
                canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, font='Arial 20 bold', text=warText, tags='war')
                canvas.update()
                time.sleep(2)
                # canvas.delete('war')

        canvas.delete('round')
        canvas.update()

    if len(playerOne) == 0 or len(playerTwo) == 0:
        winner = endGame(playerOne, playerTwo)
        canvas.delete('play')
        canvas.create_text(CANVAS_WIDTH / 2, (CANVAS_HEIGHT / 2), font='Arial 40 bold', text=f'Player {winner} won!',
                           tags='win')
        canvas.update()
        time.sleep(2)



# Game Play Functions go here


def pickCard(gameVersion=None, m=None):
    """pick from first 4 cards in the player's hand"""
    if gameVersion < 3:
        return 0
    else:
        getCardLocation = {0: 0, 1: 0, 3: 1, 5: 2, 7: 3}
        return getCardLocation[m[0]]



def playGame(gameVersion=None, playerOne=None, playerTwo=None, dumpOne=None, dumpTwo=None):
    """play the game: for the terminal or for the histogram gameVersions. returns winning player # """

    while len(playerOne) and len(playerTwo) > 0:

        # requires user input
        revealCards(gameVersion, playerOne, playerTwo, dumpOne, dumpTwo)
        if gameVersion == 1:
            # print(f'Your cards are: {playerOne}')
            print(f"You played a {dumpOne[-1][1]} of {dumpOne[-1][0]}")
            print(f'Player Two played a {dumpTwo[-1][1]} of {dumpTwo[-1][0]}')

        # compare the value of these cards: * display results: winner/ tie: append all cards to winner
        compareCards(gameVersion, playerOne, playerTwo, dumpOne, dumpTwo)
        if gameVersion == 1:
            print(f'You now have {len(playerOne)} cards.')
            print(f'Player Two now has {len(playerTwo)} cards.')

        # Ends the game once a player has run out of cards
    if len(playerOne) == 0 or len(playerTwo) == 0:
        endGame(playerOne, playerTwo)
    return endGame(playerOne, playerTwo)


def endGame(a, b):
    """End the game and declare a winner. returns winning player #"""
    if len(a) > len(b):
        return 1
    else:
        return 2


# Debated making revealCards a bool but it doesn't really matter because I would still have to pull in all the card lists
def compareCards(gameVersion=None, playerOne=None, playerTwo=None, dumpOne=None, dumpTwo=None, m=None):
    """checks dump, compares cards in the dump at index -1 to each other. return 1 if player 1 wins, 2 if player 2 wins, and 3 if it is WAR"""
    # Player 1's card is higher (order of pop doesn't matter) Dump 1's list appended first
    if dumpOne[-1][1] > dumpTwo[-1][1]:
        for i in range(len(dumpOne)):
            playerOne.append(dumpOne.pop())
        for i in range(len(dumpTwo)):
            playerOne.append(dumpTwo.pop())
        return 1

    # Player 2's card is higher (order of pop doesn't matter) Dump 2's list appended first
    elif dumpTwo[-1][1] > dumpOne[-1][1]:
        for i in range(len(dumpTwo)):
            playerTwo.append(dumpTwo.pop())
        for i in range(len(dumpOne)):
            playerTwo.append(dumpOne.pop())
        return 2

    # War
    else:
        # it's war
        if gameVersion == 1:
            print(f"It's War! You dump a card.")

        # If there is a tie but either player can't play war, end game by setting losing player's cards to 0
        if len(playerOne) < 3:
            for i in range(len(playerOne)):
                dumpOne.append(playerOne.pop())
            return 4

        elif len(playerTwo) < 3:
            for i in range(len(playerTwo)):
                dumpTwo.append(playerTwo.pop())
            return 4


        # in war, each player dumps one card face down: return to revealCard function.
        else:
            if gameVersion < 3:
                # append to dump from "top" of player lists
                dumpTwo.append(playerTwo.pop(pickCard( 0)))
                dumpOne.append(playerOne.pop(pickCard(gameVersion, m)))
            else:
                return 3




def revealCards(gameVersion=None, playerOne=None, playerTwo=None, dumpOne=None, dumpTwo=None, m=None):
    """ player selects card to play: default first in the list"""
    # change this to canvas eventually
    # Update, never mind, I'm moving all the canvas functions to their own place
    if gameVersion == 1:
        action = input(f'hit enter to turn over your card.')
    if gameVersion ==2:
        action = ''
    if gameVersion == 3:
        while m is None:
            action = 'none'
            # print('case one none')
        if m is not None:
            action = ''

    if action == '':
        # print(pickCard(gameVersion, m))
        dumpOne.append(playerOne.pop(pickCard(gameVersion, m)))
        dumpTwo.append(playerTwo.pop(pickCard(0)))


def splitDeck(playerOne, playerTwo, deck):
    """split the created deck of cards between player 1 and 2"""
    # Assign Player 1 cards
    for i in range(0, int(len(deck)/2)):
        playerOne.append(deck.pop())
    # Assign Player 2 cards
    for i in range(0, len(deck)):
        playerTwo.append(deck.pop())


"""https://stackoverflow.com/questions/6454894/reference-an-element-in-a-list-of-tuples/45724236 reference index of a list of tuples"""
def createDeck(suits, values):
    """builds a new deck and shuffles it"""
    cardDeck = []
    for i in range(0, len(suits)):
        for k in range(1, values+1):
            cardDeck.append((suits[i], k))
    random.shuffle(cardDeck)
    return cardDeck


if __name__ == '__main__':
    main()