# makes a dict to look at the special cards, note this is a cummulative value
# e.g. for the first special card: 1 card = 1, 2 cards = 3, ...
complicationdict = {1: [1, 3, 7, 7], 2: [100, 4, 0, 0]}


# represents a card in the game
class card:
    def __init__(self, value, complicationorder=0):
        self._value = value
        self._complicationoreder = complicationorder

    def getvalue(self):
        return self._value

    def getcomplicationorder(self):
        return self._complicationoreder

    def clone(self):
        return card(self.getvalue(), self.getcomplicationorder())


# returns the valur of a set of card, note that this is not a function of the cards
# since the value of a card could depend on the amount of cards of that type there are
def returncardsvalue(cards):
    value = 0
    testforcomplicationlib = {}
    for card in cards:
        # check for default cards
        if card.getcomplicationorder() == 0:
            value += card.getvalue()

        # check for non default cards
        else:
            if not card.getcomplicationorder in testforcomplicationlib:
                testforcomplicationlib[card.getcomplicationorder()] = 1
            else:
                testforcomplicationlib[card.getcomplicationorder()] += 1
    for element in testforcomplicationlib:
        checklist = complicationdict.get(element, [0, 0, 0, 0])
        index = testforcomplicationlib.get(element) - 1
        value += checklist[index]

    return value

#object representing the gamespace
class gameState:
    def __init__(self, myhandcards, opponenthandcards, myplayedcards, opponentplayedcards):
        self._myhandcards = myhandcards
        self._opponenthandcards = opponenthandcards
        self._myplayedcards = myplayedcards
        self._opponentplayedcards = opponentplayedcards

    def clone(self):
        newmyhandcards = []
        newopponenthandcards = []
        newmyplayedcards = []
        newopponentplayedcards = []
        for card in self._myhandcards:
            if card != None:
                newmyhandcards.append(card.clone())
            else:
                newmyhandcards.append(None)
        for card in self._opponenthandcards:
            if card != None:
                newopponenthandcards.append(card.clone())
            else:
                newopponenthandcards.append(None)
        for card in self._myplayedcards:
            if card != None:
                newmyplayedcards.append(card.clone())
            else:
                newmyplayedcards.append(None)
        for card in self._opponentplayedcards:
            if card != None:
                newopponentplayedcards.append(card.clone())
            else:
                newopponentplayedcards.append(None)
        return gameState(newmyhandcards, newopponenthandcards, newmyplayedcards, newopponentplayedcards)

    def gamescore(self, difference):
        if difference == False:
            return [returncardsvalue(self._opponentplayedcards), returncardsvalue(self._myplayedcards)]
        return returncardsvalue(self._myplayedcards) - returncardsvalue(self._opponentplayedcards)

    def getmymoves(self):
        moveslist = []
        for cardindex in range(len(self._myhandcards)):
            if self._myhandcards[cardindex] != None:
                moveslist.append(cardindex)

        return moveslist

    def getopponentmoves(self):
        moveslist = []
        for cardindex in range(len(self._opponenthandcards)):
            if self._opponenthandcards[cardindex] != None:
                moveslist.append(cardindex)

        return moveslist

    def myplaycard(self, card_index):
        self._myplayedcards.append(self._myhandcards[card_index])
        self._myhandcards[card_index] = None

    def opponentplaycard(self, card_index):
        self._opponentplayedcards.append(self._opponenthandcards[card_index])
        self._opponenthandcards[card_index] = None

    def switch_hand(self):
        tempcardholder = self._myhandcards
        self._myhandcards = self._opponenthandcards
        self._opponenthandcards = tempcardholder

    def gameend(self):
        for card in self._myhandcards:
            if card != None:
                return False
        return True


def minimax(depth, testgame, maxTurn):
    # base case : targetDepth reached
    if (depth == 0):
        return [testgame.gamescore(True), -1]

    if maxTurn:
        tempmax = -10000
        possiblemoves = testgame.getmymoves()
        for move in possiblemoves:
            newgame = testgame.clone()
            newgame.myplaycard(move)
            score = minimax(depth - 1, newgame, False)[0]
            if score > tempmax:
                currmove = move
                tempmax = score
        return [tempmax,currmove]

    else:
        tempmin = 10000
        possiblemoves = testgame.getopponentmoves()
        for move in possiblemoves:
            newgame = testgame.clone()
            newgame.opponentplaycard(move)
            newgame.switch_hand()
            score = minimax(depth - 1, newgame, True)[0]
            if score < tempmin:
                currmove = move
                tempmin = score
        return [tempmin,currmove]


c1 = card(1)
c2 = card(2)
c3 = card(3)
c4 = card(4)
cs = card(0, 2)

mygame = gameState([c1.clone(), c1.clone(), c4.clone(), c3.clone()], [c1.clone(), cs.clone(), c4.clone(), c1.clone()],
                   [], [])

pleasewerk = minimax(8, mygame, True)
print(pleasewerk)
