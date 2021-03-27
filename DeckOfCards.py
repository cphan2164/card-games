from random import shuffle
from copy import deepcopy
"""""
This is the Deck Of Cards, used in every game.
It has two classes, DeckOfCards and Cards.
These classes create the deck and give each "card" in the deck a value, name, suit and image.

Made by Conor Phan
"""""

#These are the available attributes given to each card.
cardValues = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
cardNames =('2','3','4','5','6','7','8','9','10','J','Q','K','A')
cardSuits = ('C','D', 'H', 'S')

#Creates the List where each card object is added to.
class DeckOfCards:
    global deckOfCards
    deckOfCards = []

    #Creates a deck whenever DeckOfCards is first initialized.
    def __init__(self, parent = None):
        self._createDeck()

    #Deletes the previous list for the deck if there is any
    #Creates the deck by first making every card in order with each card
    #recieving a cardValue and cardSuit, which are attributes in class Cards.
    #Then calls the shuffle function, which shuffles the intial in order deck.
    #shuffle is imported from the class Random
    def _createDeck(self):
        deckOfCards.clear()
        for x in cardValues:
            for y in cardSuits:
                deckOfCards.append(Cards(x, y))
        shuffle(deckOfCards)

    #Draws the top card of the list and then deletes the card from the deck list.
    def _drawCard(self):
        temp = deepcopy(deckOfCards[0])
        deckOfCards.pop(0)
        return temp

    #Basic function that calls for the current deck to be cleared and a new deck with a new order to be made.
    def _shuffleDeck(self):
        self._createDeck()

    #Basic getter, which returns the number of objects left in the list deckOfCards
    def _numberOfCards(self):
        return len(deckOfCards)

#Creates the objects that are put into the deck list
class Cards:
    #Value and suit are passed through and used to create the other two attributes.
    def __init__(self, value, suit, parent = None):
        #4 basic attributes
        self.value = value
        self.suit = suit

        #Found by taking the value and since 2 is the lowest value and is at index 0 of cardNames
        #all values must be lowered by 2 to get the card value equivalent to the card name
        self.name = cardNames[value - 2]

        #Takes the name of the card and suit, and creates the image name for each card.
        #This corresponds to the images in the Cards folder
        self.image = 'Cards/' + self.name + self.suit + '.png'



