from DeckOfCards import DeckOfCards
from copy import deepcopy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import QLabel, QMenu, QMenuBar
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
import math
import sys
from functools import partial
import subprocess
"""""
This is the Screw The Dealer GUI. It contains only one class, which is the ScrewTheDealer class.
This class is the playable card game Screw The Dealer.

For more information on how to play ride the bus go to Help and Info/ How to Play Screw The Dealer.txt
Or in the game itself, go to help and click how to play.

@author: Conor Phan
Made in 2021
"""""

#games starts at 1 because as soon as the first game starts it counts as being in a game.
# This makes more sense with the score given after a win
class ScrewTheDealer(QMainWindow):
    deck = DeckOfCards()
    card1 = None
    click = 0
    score = 0
    games = 1

    #Creates the initial GUI visible and calls all functions to build the GUI
    def __init__(self, parent = None):
        super().__init__(parent)
        self.generalLayout = QVBoxLayout()
        self.setWindowTitle('Screw The Dealer')
        self.setFixedSize(1500,1000)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createHeader()
        self._createButtons()
        self._createFooter()
        self._createMenuBar()

    #Creats the header, which is the three blank cards and a box that can be used to send information to the user.
    def _createHeader(self):
        self.header = QHBoxLayout()
        self.header.setSpacing(50)

        #Creates three blank cards
        self.card1Img = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(297)
        pixmap = pixmap.scaledToWidth(194)
        self.card1Img.setPixmap(pixmap)
        self.header.addWidget(self.card1Img)

        self.card2Img = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(297)
        pixmap = pixmap.scaledToWidth(194)
        self.card2Img.setPixmap(pixmap)
        self.header.addWidget(self.card2Img)

        self.card3Img = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(297)
        pixmap = pixmap.scaledToWidth(194)
        self.card3Img.setPixmap(pixmap)
        self.header.addWidget(self.card3Img)

        #Creates a Label that can be adjusted to send information to the user.
        self.helper = QLabel("Pick A Card")
        self.helper.setFont(QFont("Arial", 100))
        self.helper.setAlignment(Qt.AlignCenter)
        self.helper.setStyleSheet("background-color: #87ceeb;" "border: 7px solid black;")
        self.helper.setFixedSize(700, 150)
        self.header.addWidget(self.helper)
        self.header.addWidget(QLabel())

        self.generalLayout.addLayout(self.header)

    #Creates 13 buttons one for each card. This allows user to pick a card
    def _createButtons(self):
        #Created two button line to make sure cards are separated well and can easily be identified
        buttonLine1 = QHBoxLayout()
        buttonLine2= QHBoxLayout()
        buttons1 = {2, 3, 4, 5, 6, 7, 8}
        for x in buttons1:
            button = QPushButton()
            button.setFixedSize(200, 250)
            #Spades is chosen as suit, but this is arbitrary and suits have nothing to do with the game
            button.setIcon(QIcon('Cards/' + str(x) + 'S.png'))
            button.setIconSize(QSize(146, 222))
            button.clicked.connect(partial(self._controller, x))
            buttonLine1.addWidget(button)

        buttons2 ={9, 10, 11, 12, 13, 14}
        for x in buttons2:
            button = QPushButton()
            button.setFixedSize(200, 250)
            button.setIcon(QIcon('Cards/' + str(x) + 'S.png'))
            button.setIconSize(QSize(146, 222))
            button.clicked.connect(partial(self._controller, x))
            buttonLine2.addWidget(button)

        self.generalLayout.addLayout(buttonLine1)
        self.generalLayout.addLayout(buttonLine2)

    #This manages the game
    def _controller(self, value):
        #If click is 6 this means all 3 cards have been shown and two guess for each card have happened
        #This is how the user loses and this will reset the dealer's hand
        if self.click == 6:
            self.games = self.games + 1
            self._reset()
        #If the click is either 0, 2, or 4, this means it is the first guess and a hint should be given
        #on whether the card the dealer has is higher or lower than the card chosen.
        if self.click%2 == 0:
            self.card1 = deepcopy(self.deck._drawCard())
            self.click = self.click + 1
            #If guessed card is lower than dealer's card
            if value < self.card1.value:
                self._higher()
            #If guessed card is higher than dealer's card
            elif value > self.card1.value:
                self._lower()
            #If guessed card equals the dealer's card
            else:
                self._win()
        #If click is odd, this means the user guessed, a hint was given, and the user guessed again.
        else:
            self.click = self.click + 1
            #If guessed card equals the dealer's card
            if value == self.card1.value:
                self._win()
            #If 2nd guess still does not equal dealer's card
            else:
                self._lose(value)

    #This function is called if the 2nd guess was still not the dealer's card
    #This reveals the card in a specific slot based off, which click it is
    #It also tells the user in the box next to the card how far off the card was from the card they chose.
    def _lose(self, value):
        self.helper.setStyleSheet("background-color: #87ceeb;" "border: 7px solid black;" "color: black")
        #Reveals card and adds it to the used card list at the bottom
        self._revealCard()
        off = abs(value - self.card1.value)
        self.helper.setText("Off By " + str(off))

    #This function is called if the user guesses the dealer's card either on the first or second attempt
    #By winning the box will show how many games the player has won vs. how many games the user has played.
    def _win(self):
        self.helper.setStyleSheet("background-color: #87ceeb;" "border: 7px solid black;" "color: black")
        self.score = self.score + 1
        self.helper.setText("Score: " + str(self.score) + "/" + str(self.games))
        #The card is revelaed and added to the used card list
        self._revealCard()
        #This resets the cards at the top upon next click.
        self.click = 6

    #This function resets the cards at the top and the box at the the top right, which helps the user.
    def _reset(self):
        self.click = 0
        self.helper.setText("New Round")
        self.helper.setStyleSheet("background-color: #87ceeb;" "border: 7px solid black;" "color: black")

        #Sets 3 cards at top back to blank cards.
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(297)
        pixmap = pixmap.scaledToWidth(194)
        self.card1Img.setPixmap(pixmap)
        self.card2Img.setPixmap(pixmap)
        self.card3Img.setPixmap(pixmap)
        self._checkDeck()

        #This function is called when 'Back To Menu' is triggered
        #Resets the game along with the score and starts over with a new deck and no used cards.
    def _resetAll(self):
        self._reset()
        self.score = 0
        self.games = 1
        self.deck._shuffleDeck()
        for i in reversed(range(self.footer.count())):
            self.footer.itemAt(i).widget().setParent(None)
        self._createFooter()

    #This functio makes sure there is enough cards left in the deck to play another round
    #If not then the deck is shuffled and used card list gets deleted
    def _checkDeck(self):
        if self.deck._numberOfCards() <=3:
            self.deck._shuffleDeck()
            for i in reversed(range(self.footer.count())):
                self.footer.itemAt(i).widget().setParent(None)
            self._createFooter()

    #This function is used to have the helper box in the top right of the GUI to help the user in making their second guess
    #In this case it tells the dealer's the next card is lower.
    def _lower(self):
        self.helper.setStyleSheet("background-color: #87ceeb;" "border: 7px solid black;" "color: red")
        self.helper.setText("LOWER")

    # This function is used to have the helper box in the top right of the GUI to help the user in making their second guess
    # In this case it tells the user the dealer's card is higher.
    def _higher(self):
        self.helper.setStyleSheet("background-color: #87ceeb;" "border: 7px solid black;" "color: green")
        self.helper.setText("HIGHER")

    #This reveals the card in the correct position based off of what click it was on
    def _revealCard(self):
        #Slot represents the slot the revealed card should go to.
        # Minus 1 is used because the second guess makes the click one higher than what slot it should go to.
        slot = int(math.floor((self.click - 1) / 2))
        self._addToFooter()
        #First card slot, for when self.clicks = 1 or 2
        if slot == 0:
            card = QPixmap(self.card1.image)
            card = card.scaledToHeight(297)
            card = card.scaledToWidth(194)
            self.card1Img.setPixmap(card)
        #Second card slot, for when self.clicks = 3 or 4
        elif slot == 1:
            card = QPixmap(self.card1.image)
            card = card.scaledToHeight(297)
            card = card.scaledToWidth(194)
            self.card2Img.setPixmap(card)
        #Third card slot, for when self.clicks = 5, 6
        elif slot == 2:
            card = QPixmap(self.card1.image)
            card = card.scaledToHeight(297)
            card = card.scaledToWidth(194)
            self.card3Img.setPixmap(card)
        #Safety measure in case some how the clicks are wrong the game will reset.
        else:
            self._reset()

    #This creates the bottom where all the used cards will be placed
    def _createFooter(self):
        self.footer = QHBoxLayout()
        blankCard = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(148)
        pixmap = pixmap.scaledToWidth(97)
        blankCard.setPixmap(pixmap)
        self.footer.addWidget(blankCard)
        self.generalLayout.addLayout(self.footer)

    #Adds the card that was just revealed to the bottom footer
    def _addToFooter(self):
        usedCard = QLabel(self)
        pixmap = QPixmap(self.card1.image)
        pixmap = pixmap.scaledToHeight(148)
        pixmap = pixmap.scaledToWidth(97)
        usedCard.setPixmap(pixmap)
        usedCard.setAlignment(Qt.AlignLeft)
        self.footer.addWidget(usedCard)
        self.generalLayout.addLayout(self.footer)

    #Creates the menu bar for the GUI.
    def _createMenuBar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

    #Creates menu with the back to menu function
        menu = QMenu("&Menu", self)
        menuBar.addMenu(menu)

        # Creates the back to menu action, which when triggered calls the connected function,
        # which is in the manager class in Menu.py
        self.close1 = QAction("Back To Menu", self)
        menu.addAction(self.close1)

        # Creates help and info and how to play tabs
        helpMenu = QMenu("&Help", self)
        menuBar.addMenu(helpMenu)
        info = QAction("Info", self)
        info.triggered.connect(self._info)

        howToPlay = QAction("How to Play", self)
        howToPlay.triggered.connect(self._help)

        helpMenu.addAction(info)
        helpMenu.addAction(howToPlay)

    # Opens txt file with info on the program. Same for all 4 GUIs in the project
    def _info(self):
        subprocess.call(['notepad.exe', 'Help and Info/Info.txt'])

    # Calls a txt with the information on how to play the current game.
    def _help(self):
        subprocess.call(['notepad.exe', 'Help and Info/How To Play Screw The Dealer.txt'])


#Allows the program to be ran individually without the Menu, mainly for testing purposes.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScrewTheDealer()
    window.show()
    sys.exit(app.exec())


