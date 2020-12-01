import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme()
# DONTBELIKEZOE
# GameVersion == 0:
# flip first card
# win: append to back

# GameVersion == CHEAT
# win! if any card in either dump > 7 : put the dump on top of the deck
# I'm not going to get too granular with this version because IMO putting cards on top is cheating, so it won't be included in the final game.

# Strategy == 1
# access to first 4 cards
# Play highest card always

# Strategy == 2
# access to first 4 cards
# play highest card EXCEPT if war: play lowest


# GameVersion == 3
# access to first 4 cards
# vs Play highest card always (Unless cards in hand are all less than 7 OR Unless War (play lowest)

# set up game:
# turn game version into strategy version?
# build with print before saving to csv


def main():
    # Strategy for player 2
    z = 0

    # Strategy for player 1
    x = 0

    # change to "c" if you want to add the cheating variable
    k = ''
    emptyList = []
    Player1Strategy = [1, x, k]
    Player2Strategy = [2, z, '']
    
    # If set to 0, when run, plotStuff() will run (assuming the csv of game stats has been downloaded: see Game_of_War_Strategy_Data with wars.csv)
    times = 0

    # how many rounds to play per game before ending game
    limit = 52*50
    for t in range(0, times):
        suits = ['diamonds','spades', 'clubs', 'hearts']
        values = 13
        One = []
        Two = []
        dumpOne = []
        dumpTwo = []

        # Create the deck
        deck = createDeck(suits, values)
        # split deck
        splitDeck(One, Two, deck)

        # Example Deck
        # One = [("pink", 13), ("pink", 12), ("red", 12), ("white", 10), ("pink", 8)]
        # Two = [("pink", 12), ("red", 10), ("pink", 9), ("white", 2), ("pink", 13)]

        # for i in range(0, 4):
            # for k in range(0, i + 1):
                # playerOne = One.copy()
                # playerTwo = Two.copy()
                # print(i)
                # print(k)
                # Player1Strategy = [1, i, '']
                # Player2Strategy = [2, k, '']
                # p= playGame(Player1Strategy,Player2Strategy,playerOne,playerTwo,dumpOne,dumpTwo)
                # emptyList.append(p)
                # print(emptyList)
        p = playGame(Player1Strategy, Player2Strategy, One, Two,dumpOne ,dumpTwo, limit)
        emptyList.append(p)

    createCSV(x,z,k,emptyList, times)

    plotStuff()



def plotStuff():
    """Danny suggested using Pandas for this, so I did a LOT of googling: I mostly used the following:"""
    """https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-pandas-dataframe and https://365datascience.com/bar-chart-python-matplotlib/"""
    """https://matplotlib.org/3.1.1/gallery/units/bar_unit_demo.html"""
    # read csv
    gowcsv = pd.read_csv('Game_of_War_Strategy_Data with wars.csv')
    # remove empty cells
    gowcsv = gowcsv.dropna(axis="rows", how="any")

    gowcsv['Strategy 1'] = gowcsv['Strategy 1'].astype(str)
    gowcsv.sort_values('Strategy 1', ascending=True)
    # print(gowcsv['Strategy 1'])


    # print(gowcsv['Strategy 1'].value_counts())

    # concat strategy 1 and strategy 2 columns:
    gowcsv['Strategy'] = gowcsv['Strategy 2'].astype(str) + '/' + gowcsv['Strategy 1']
    gowcsv.sort_values('Strategy', ascending=True)
    # print(gowcsv)

    # count number of times the strategy was simulated)
    sumplay = gowcsv.groupby(['Strategy'])['winner'].count().reset_index(name="count")
    # sum1 = gowcsv.groupby(['Strategy'])['winner'].value_counts().reset_index(name="sum 1")

    Player1Wins = gowcsv[gowcsv.winner == 1.0].groupby(['Strategy']).count()
    Player2Wins = gowcsv[gowcsv.winner == 2.0].groupby(['Strategy']).count()
    print(gowcsv)
    print(Player1Wins)

    # create pivot table w/ strategy and mean of # cards played and # of wars
    newdf = gowcsv.pivot_table(index=['Strategy'], values=['# cards played','wars'],aggfunc=np.mean)
    # newdf['Player 1'] = newdf[Player1Wins]


    # all my "calculations"!
    nai= sumplay.merge(newdf, left_on='Strategy', right_on='Strategy')

    nai = nai.merge(Player1Wins['Strategy 1'], left_on='Strategy', right_on='Strategy')
    nai = nai.merge(Player2Wins['Strategy 2'], left_on='Strategy', right_on='Strategy')
    # print(nai)
    # print(gowcsv.groupby(['Strategy', '# cards played']).mean())

    # print(gowcsv)
    # fig, ax = plt.subplots()

    # xind = 20
    # width = 0.35
    # s1 = ax.bar(xind, nai['Strategy 1'], width)
    # s2 = ax.bar(xind + width, nai['Strategy 2'], width)


    # plt.bar(x=gowcsv['Strategy'], height=gowcsv['# cards played'])
    # plt.bar(x=gowcsv['Strategy'], height=)
    # ax.set_title('Player Wins per Strategy')
    # labels= ax.set_xticklabels(nai['Strategy'])
    # ax.set_xticklabels(labels, rotation=45)
    # ax.autoscale_view()
    # ax.legend((s1[0], s2[0]), ('Player 1', 'Player 2'))

    colors = ['mediumvioletred', 'lightseagreen']
    nai[['Strategy', 'Strategy 2', 'Strategy 1']].plot.bar(x='Strategy', rot=70, title='Games Won Per Strategy Variation',
                                                           xlabel='Strategy: Player 2 v Player 1', ylabel='Games Won',
                                                           color= colors, figsize=(9,7.5))
    # plt.show()



    plt.show()

    # print(gowcsv)
    # count the number of times 1 appears for Strategy
    # count the number of times 2 appears for Strategy
    # count the number of times cards played == 2600 for Strategy


    pass

def createCSV(x, z, k, emptyList, times):
    if times == 0:
        pass
    gowcsv = open('Game_of_War_Strategy_Data with wars.csv', 'a')
    # headers = ['Strategy 1', 'Strategy 2', 'winner', '# cards played', 'wars']

    # write headers
    # for i in range(len(headers)):
        # gowcsv.writelines(f'{headers[i]},')

    # write data: create new line at beginning of for loop
    for j in range(len(emptyList)):
        gowcsv.writelines(f'\n{x} {k},')
        gowcsv.writelines(f'{z},')
        gowcsv.writelines(f'{emptyList[j][0]},')
        gowcsv.writelines(f'{emptyList[j][1]},')
        gowcsv.writelines(f'{emptyList[j][2]}')

    gowcsv.close()


    # play game
def playGame(Player1Strategy=None,Player2Strategy=None, One=None, Two=None,dumpOne=None,dumpTwo=None, limit=None):
    """returns integer of winning player, number of cards played, number of wars"""
    playerOne = One
    playerTwo = Two
    countCards = 0
    numwar = 0
    while len(playerOne) and len(playerTwo) > 0 and countCards < limit:

        # play picks card to play : EDIT FOR STRATEGY:
        # should return dump one return playerOne
        # print(f'playerOne {playerOne}')
        revealCards(Player1Strategy, playerOne, dumpOne)

        # should return dump two return playerTwo
        # print(f'playerTwo {playerTwo}')
        revealCards(Player2Strategy, playerTwo, dumpTwo)
        countCards += 1
        # print(f' p1 cards: {playerOne} and p2 cards: {playerTwo}')

        # compare the value of these cards: * display results: winner/ tie: append all cards to winner
        if dumpOne[-1][1] > dumpTwo[-1][1]:

            compareCards(Player1Strategy, playerOne, playerTwo, dumpOne, dumpTwo)
        elif dumpTwo[-1][1] > dumpOne[-1][1]:

            compareCards(Player2Strategy, playerOne, playerTwo, dumpOne, dumpTwo)
        else:
            if len(playerOne) < 3:
                for i in range(len(playerOne)):
                    dumpOne.append(playerOne.pop())
            elif len(playerTwo) < 3:
                for i in range(len(playerTwo)):
                    dumpTwo.append(playerTwo.pop())

            else:
                print("it's war!")
                numwar += 1
                war(Player1Strategy, playerOne, dumpOne)
                war(Player2Strategy, playerTwo, dumpTwo)

        #
        # compareCards(Player1Strategy, Player2Strategy, playerOne, playerTwo, dumpOne, dumpTwo)

        # Ends the game once a player has run out of cards
    if len(playerOne) == 0 or len(playerTwo) == 0 or countCards == limit :
        endGame(playerOne, playerTwo)
        return endGame(playerOne, playerTwo), countCards, numwar
    # return endGame(playerOne, playerTwo)


def war(strategy=None, player=None, dump=None):
    """There is one action (dumping a card) and three ways it can be completed. 0) dump top card. 1) dump highest card 3) dump lowest card"""
    # If there is a tie but either player can't play war, end game by setting losing player's cards to 0
    # in war you can dump your highest card, dump your lowest card, or dump the top card in your hand

    # in war, each player dumps one card face down: return to revealCard function.
    # strategy 0: always play first card
    if strategy[1] == 0:
        dump.append(player.pop(0))
        # print(f'(strategy {strategy[1]}) Player {strategy[0]} dumped {dump[-1]}')

    # strategy 1: always play highest card
    if strategy[1] == 1:
        c = max(x[1] for x in player[0:4])
        highest = ([y[1] for y in player].index(c))
        dump.append(player.pop(highest))
        print(f'(strategy {strategy[1]}) Player {strategy[0]} dumped {dump[-1]}')

    # strategy 2: in war play lowest card
    if 3 >= strategy[1] >= 2:
        c = min(x[1] for x in player[0:4])
        lowest = ([y[1] for y in player].index(c))
        dump.append(player.pop(lowest))
        # print(f'(strategy {strategy[1]}) Player {strategy[0]} dumped {dump[-1]}')


def revealCards(strategy=None, player=None, dump=None):
    """There are three strategies here: 0) play top card 1) play highest card 2) play highest card IF card is > 7, otherwise play lowest card."""
    # gameVersion 0
    if strategy[1] == 0:
        # In strategy 0, players can only play the "top" card in their "hand" #keep GOW classes?
        # action = input(f'strategy {strategy[1]} Player {strategy[0]} hit enter to play card')
        action = ''
        if action == '':
            dump.append(player.pop(0))
            print(f'strategy {strategy[1]} Player {strategy[0]} played {dump[-1]} player cards {player}')

    if 2 >= strategy[1] >= 1:
        # in strategy 1 players always play the highest card in their hand
        # print(f'(strategy 1 or 2) Player {strategy[0]} cards: {player}')
        # print(f'Player 2 cards:{playerTwo}')
        # action = input(f'Player {strategy[0]} hit enter to play card')
        action = ''
        a = max(x[1] for x in player[0:4])
        highest = ([y[1] for y in player].index(a))

        if action == '':
            dump.append(player.pop(highest))
            # dumpTwo.append(playerTwo.pop(GOWC.highest2))
        print(f'Player {strategy[0]} played {dump[-1]} player cards {player}')

    if strategy[1] == 3:
        # print(f'Player {strategy[0]} cards: {player}')
        # print(f'Player 2 cards:{playerTwo}')
        # action = input(f'Player {strategy[0]} hit enter to play card')
        action = ''
        a = max(x[1] for x in player[0:4])
        highest = ([y[1] for y in player].index(a))
        b = min(x[1] for x in player[0:4])
        lowest = ([y[1] for y in player].index(b))

        # if highest is greater than 7, play highest otherwise play the lowest
        if action == '':
            if a > 7:
                dump.append(player.pop(highest))
            else:
                dump.append(player.pop(lowest))
            # dumpTwo.append(playerTwo.pop(GOWC.highest2))
        print(f'Player {strategy[0]} played {dump[-1]}')


def compareCards(strategy=None, playerOne=None, playerTwo=None, dumpOne=None, dumpTwo=None, m=None):
    """checks dump, compares cards in the dump at index -1 to each other. return 1 if player 1 wins, 2 if player 2 wins, and 3 if it is WAR"""
    """returns playerOne cards, PlayerTwo cards, dumpOne cards, dumpTwo cards"""
    max1 = max(x[1] for x in dumpOne[0:])
    max2 = max(x[1] for x in dumpTwo[0:])
    # pulls in winning player's strategy:
    # if player 1 won
    if strategy[0] == 1:
        # checks strategy
        # in secret strategy, CHEAT and add cards to front of deck when you win if any card is > 7
        if strategy[2] != '':
            if max1 or max2 > 7:
                for i in range(len(dumpOne)):
                    playerOne.insert(0, dumpOne.pop())
                for i in range(len(dumpTwo)):
                    playerOne.insert(0, dumpTwo.pop())
                print(f"P1 won this round and added your cards to the TOP of your deck. You have {len(playerOne)} cards.")
            else:
                # otherwise append to the back
                for i in range(len(dumpOne)):
                    playerOne.append(dumpOne.pop())
                for i in range(len(dumpTwo)):
                    playerOne.append(dumpTwo.pop())
                # print(f"You won this round and added your cards to the bottom of your deck. You have {len(playerOne)} cards.")
        else:
            # otherwise append to the back
            for i in range(len(dumpOne)):
                playerOne.append(dumpOne.pop())
            for i in range(len(dumpTwo)):
                playerOne.append(dumpTwo.pop())
            print(f"Player 1 won this round and added your cards to the bottom of your deck. You have {len(playerOne)} cards.")

    if strategy[0] == 2:
        if strategy[2] != '':
        # in secret strategy, CHEAT and add cards to front of deck when you win if the either player just played a card > 7
            if max1 or max2 > 7:
                for i in range(len(dumpTwo)):
                    playerTwo.insert(0, dumpTwo.pop())
                for i in range(len(dumpOne)):
                    playerTwo.insert(0, dumpOne.pop())
                print( f" P2 won this round and added your cards to the TOP of your deck. You have {len(playerTwo)} cards.")
            else:
                # otherwise append to the back
                for i in range(len(dumpTwo)):
                    playerTwo.append(dumpTwo.pop())
                for i in range(len(dumpOne)):
                    playerTwo.append(dumpOne.pop())
                # print( f"You won this round and added your cards to the bottom of your deck. You have {len(playerTwo)} cards.")
        else:
            # otherwise append to the back
            for i in range(len(dumpTwo)):
                playerTwo.append(dumpTwo.pop())
            for i in range(len(dumpOne)):
                playerTwo.append(dumpOne.pop())
            print( f"Player 2 won this round and added your cards to the bottom of your deck. Your have {playerTwo} cards.")





def endGame(a, b):
    """End the game and declare a winner. returns winning player #"""
    if len(a) > len(b):
        return 1
    else:
        return 2


def createDeck(suits, values):
    """builds a new deck and shuffles it"""
    cardDeck = []
    for i in range(0, len(suits)):
        for k in range(1, values+1):
            cardDeck.append((suits[i], k))
    random.shuffle(cardDeck)
    return cardDeck

def splitDeck(playerOne=None, playerTwo=None, deck=None):
    """split the created deck of cards between player 1 and 2"""
    # Assign Player 1 cards
    for i in range(0, int(len(deck)/2)):
        playerOne.append(deck.pop())
    # Assign Player 2 cards
    for i in range(0, len(deck)):
        playerTwo.append(deck.pop())



if __name__ == '__main__':
    main()
