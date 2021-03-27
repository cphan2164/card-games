from DeckOfCards import DeckOfCards
from copy import deepcopy
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QMenu, QMenuBar
from PyQt5.QtWidgets import QGridLayout, QAction
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QSize, Qt
from functools import partial
from PyQt5.QtTest import QTest
import sys
import subprocess
"""""
This is the Ride The Bus GUI. It contains only one class, which is the RideTheBus class.
This class is the playable game ride the bus.

For more information on how to play ride the bus go to Help and Info/ How to Play Ride The Bus.txt
Or in the game itself, go to help and click how to play.

@author: Conor Phan
Made in 2021
"""""

#All 4 cards are stated as None to begin, allowing them to be easily used and manipulated throughout the class
class RideTheBus(QMainWindow):
    deck = DeckOfCards()
    card1 = None
    card2 = None
    card3 = None
    card4 = None

    # Creates the initial GUI visible and calls all functions to build the GUI
    def __init__(self, parent = None):
        super().__init__(parent)
        self.generalLayout = QHBoxLayout()
        self.setWindowTitle('Ride The Bus')
        self.setFixedSize(1500,1000)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createCards()
        self._choiceOne()
        self._createMenuBar()

    #Creates 4 blank cards that will reveal the 4 cards in the game itself.
    def _createCards(self):
        self.cardsLayout1 = QVBoxLayout()
        self.card1Img = QLabel(self)

        #Since same pixmap will be used for all 4 cards in the beginning only have to create it once then apply to each card.
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(475)
        pixmap = pixmap.scaledToWidth(310)
        self.card1Img.setPixmap(pixmap)
        self.cardsLayout1.addWidget(self.card1Img)

        self.card3Img = QLabel(self)
        self.card3Img.setPixmap(pixmap)
        self.cardsLayout1.addWidget(self.card3Img)

        self.generalLayout.addLayout(self.cardsLayout1)

        self.cardsLayout2 = QVBoxLayout()
        self.card2Img = QLabel(self)
        self.card2Img.setPixmap(pixmap)
        self.cardsLayout2.addWidget(self.card2Img)

        self.card4Img = QLabel(self)
        self.card4Img.setPixmap(pixmap)
        self.cardsLayout2.addWidget(self.card4Img)

        self.generalLayout.addLayout(self.cardsLayout2)

    #The first choice in the game is choosing either red or black card is going to be next card.
    def _choiceOne(self):
        self.choices = QGridLayout()

        #Create the buttons with icons of a red and black card to click on thie right side of the GUI
        self.choice1Red = QPushButton(self)
        self.choice1Red.setFixedSize(320,500)
        self.choice1Red.setIcon(QIcon('Cards/red_back.png'))
        self.choice1Red.setIconSize(QSize(310,475))
        self.choice1Red.clicked.connect(partial(self._choiceOneClick, 0))
        self.choices.addWidget(self.choice1Red, 0, 0, 1, 0)

        self.orLabel = QLabel("    OR")
        self.orLabel.setFont(QFont("Times", 70))
        self.choices.addWidget(self.orLabel, 0 ,1)

        self.choice1Black = QPushButton(self)
        self.choice1Black.setFixedSize(320,500)
        self.choice1Black.setIcon(QIcon('Cards/gray_back.png'))
        self.choice1Black.setIconSize(QSize(310, 475))
        self.choice1Black.clicked.connect(partial(self._choiceOneClick, 1))
        self.choices.addWidget(self.choice1Black, 0, 2, 1, 2)

        self.generalLayout.addLayout(self.choices, stretch=2)

    #This function gets called no matter the decision on _choiceOne. If click was red a 0 will be the parameter
    #If click was black a 1 will be the parameter
    def _choiceOneClick(self, choice):
        self.card1 = deepcopy(self.deck._drawCard())

        #Reveals the first card in the top left slot
        pixmap = QPixmap(self.card1.image)
        pixmap = pixmap.scaledToHeight(475)
        pixmap = pixmap.scaledToWidth(310)
        self.card1Img.setPixmap(pixmap)

        #Checks the suit with the choice the user gave. #If choice was red and it was Hearts or Diamonds it clears
        #If choice was black and it was clucs or spades it clears. Otherwise the game resets.
        if choice == 0 and (self.card1.suit == 'H' or self.card1.suit == 'D'):
            self._choiceTwo()
        elif choice == 1 and (self.card1.suit == 'S' or self.card1.suit == 'C'):
            self._choiceTwo()
        else:
            self._defeat()
            self._reset()

    #This function is called when choice one was picked correctly
    #Choice two is whether the next card will be higher or lower than the first card
    def _choiceTwo(self):
        self._clearLayout()

        self.choices.addWidget(self.orLabel, 1,0)

        #Created up and down arrow buttons, with pictures of a up and down arrow.
        higherButton = QPushButton(self)
        higherButton.setIcon(QIcon('Cards/UpArrow.png'))
        higherButton.setIconSize(QSize(250,250))
        higherButton.clicked.connect(partial(self._choiceTwoClick, 0))
        self.choices.addWidget(higherButton, 0,0)

        lowerButton = QPushButton(self)
        lowerButton.setIcon(QIcon('Cards/DownArrow.png'))
        lowerButton.setIconSize(QSize(250, 250))
        lowerButton.clicked.connect(partial(self._choiceTwoClick, 1))
        self.choices.addWidget(lowerButton, 2, 0)

        self.generalLayout.addLayout(self.choices)

    #This function is called no matter the decision of choiceTwo
    #If the button pressed was higher it will be passed with a 0, if lower it will be passed with a 1
    def _choiceTwoClick(self, pick):
        self.card2 = deepcopy(self.deck._drawCard())

        #Reveal card 2 in the top right position
        pixmap = QPixmap(self.card2.image)
        pixmap = pixmap.scaledToHeight(475)
        pixmap = pixmap.scaledToWidth(310)
        self.card2Img.setPixmap(pixmap)

        #If higher and the next card is higher than the first, calls choiceThree. If lower and
        #the next card is lower than the first, callls choiceThree. Else the game resets to question 1.
        #If the 2nd card is the same value as first card game resets
        if pick == 0 and self.card2.value > self.card1.value:
            self._choiceThree()
        elif pick == 1 and self.card2.value < self.card1.value:
            self._choiceThree()
        else:
            self._defeat()
            self._reset()

    #This function is called when choice two was picked succesfully.
    #Choice three is if the next card is in between or outside the 1st and 2nd card values.
    def _choiceThree(self):
        self._clearLayout()

        self.choices.addWidget(self.orLabel, 2, 0)

        #Creates in between and outside buttons that call _choicethreeclick with a different number in the parameter.
        inBetween = QPushButton("In Between")
        inBetween.setFont(QFont("Times", 90))
        inBetween.clicked.connect(partial(self._choiceThreeClick, 0))
        self.choices.addWidget(inBetween, 1, 0)

        outside = QPushButton("Outside")
        outside.setFont(QFont("Times", 90))
        outside.clicked.connect(partial(self._choiceThreeClick, 1))
        self.choices.addWidget(outside, 3, 0)

        fillerLabel = QLabel()
        fillerLabel2 = QLabel()
        self.choices.addWidget(fillerLabel, 0,0)
        self.choices.addWidget(fillerLabel2, 4, 0)

        self.generalLayout.addLayout(self.choices)

    #Function called with the buttons from choiceThree
    #Parameter inOrOut is used to know users decision
    def _choiceThreeClick(self, inOrOut):
        self.card3 = deepcopy(self.deck._drawCard())

        #Reveals the third card in the bottom left spot
        pixmap = QPixmap(self.card3.image)
        pixmap = pixmap.scaledToHeight(475)
        pixmap = pixmap.scaledToWidth(310)
        self.card3Img.setPixmap(pixmap)

        #Checks to see if value is in between or outside and if user's decision corresponds with that.
        #If  card 3 is the same as card 1 or card 2 it is an auto lose
        #To check outside see if value of card 3 is lower than the other two values or higher than the other two values
        #To check inbetween see if value of card 3 is in between the other two values.
        if inOrOut == 0 and ((self.card3.value > self.card1.value and self.card3.value < self.card2.value) or
                             (self.card3.value > self.card2.value and self.card3.value < self.card1.value)):
            self._choiceFour()
        elif inOrOut == 1 and ((self.card3.value > self.card1.value and self.card3.value > self.card2.value) or
                               (self.card3.value < self.card1.value and self.card3.value < self.card2.value)):
            self._choiceFour()
        #If choice wrong the game resets to the first question
        else:
            self._defeat()
            self._reset()

    #This function is only called when the user chooses choice 3 correctly.
    #Choice four question is what is the suit of the next card
    def _choiceFour(self):
        self._clearLayout()

        #Created four buttons each with a picture of a suit on them.
        #Suits are H for Hearts, D for Diamonds, S for Spades, and C for Clubs.
        # Corresponding pictures can be found in the Cards folder
        hearts = QPushButton()
        hearts.setIcon(QIcon('Cards/Hearts.png'))
        hearts.setIconSize(QSize(279, 427))
        hearts.clicked.connect(partial(self._choiceFourClick, 'H'))
        self.choices.addWidget(hearts, 0, 0)

        diamonds = QPushButton()
        diamonds.setIcon(QIcon('Cards/Diamonds.png'))
        diamonds.setIconSize(QSize(279, 427))
        diamonds.clicked.connect(partial(self._choiceFourClick, 'D'))
        self.choices.addWidget(diamonds, 0, 2)

        clubs = QPushButton()
        clubs.setIcon(QIcon('Cards/Clubs.png'))
        clubs.setIconSize(QSize(279, 427))
        clubs.clicked.connect(partial(self._choiceFourClick, 'C'))
        self.choices.addWidget(clubs, 2, 0)

        spades = QPushButton()
        spades.setIcon(QIcon('Cards/Spades.png'))
        spades.setIconSize(QSize(279, 427))
        spades.clicked.connect(partial(self._choiceFourClick, 'S'))
        self.choices.addWidget(spades, 2, 2)

        self.generalLayout.addLayout(self.choices)

    #Function is called with the character of the button chosen passed as a parameter.
    def _choiceFourClick(self, suit):
        self.card4 = deepcopy(self.deck._drawCard())

        #Reveals the fourth card in the bottom right position
        pixmap = QPixmap(self.card4.image)
        pixmap = pixmap.scaledToHeight(475)
        pixmap = pixmap.scaledToWidth(310)
        self.card4Img.setPixmap(pixmap)

        #Checks if suit of 4th cards equals the suit guess. Otherwise the game resets to question 1
        if suit == self.card4.suit:
            self._victory()
        else:
            self._defeat()
            self._reset()

    #Victory screen if all four choices are chosen correctly
    #Placed on a timer so it only lasts for 2.5 seconds. Then game resets to question 1
    def _victory(self):
        self._clearLayout()

        #Creates win label to place on screen
        win = QLabel(self)
        pixmap = QPixmap('Cards/win.png')
        pixmap = pixmap.scaledToWidth(800)
        pixmap = pixmap.scaledToHeight(550)
        win.setPixmap(pixmap)
        self.choices.addWidget(win)
        self.generalLayout.addLayout(self.choices)
        #Creates a pause for 2.5 seconds before reseetting the game
        QTest.qWait(2500)

        self._reset()

    #This is the call when any of the 4 choices are chosen incorrectly
    def _defeat(self):
        #Resets layout so no other choices can be chosen until game fully resets.
        self._clearLayout()

        #You Lose label displayed for a second so players have time to see card and know why they lost
        lose = QLabel('YOU LOSE')
        lose.setFont(QFont("Times", 120))
        lose.setStyleSheet("color: red")
        lose.setAlignment(Qt.AlignCenter)
        self.choices.addWidget(lose, 0 ,0)
        self.generalLayout.addLayout(self.choices)
        #One second delay
        QTest.qWait(1000)

    #This function is called anytime cards need to be reset, whether there was a victory or not.
    #This function calls functions that check the deck, clear choice and cards already revealed, and goes back to choice one
    def _reset(self):
        self._checkDeck()
        self._clearLayout()
        self._clearCards()
        self._createCards()
        self._choiceOne()

    #Removes all widgets on the right side of the GUI inside the choice grid.
    def _clearLayout(self):
        for i in reversed(range(self.choices.count())):
            self.choices.itemAt(i).widget().setParent(None)

    #Removes the two card layouts and takes away all widgets on the left side of the GUI in side the card layouts
    def _clearCards(self):
        for i in reversed(range(self.cardsLayout1.count())):
            self.cardsLayout1.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.cardsLayout2.count())):
            self.cardsLayout2.itemAt(i).widget().setParent(None)

    #Makes sure there is an adequate number of cards to play and if there is not it shuffles the deck
    #Tells the player if the deck is being "shuffled".
    def _checkDeck(self):
        if self.deck._numberOfCards() <= 4:
            self._clearLayout()
            shuffling = QLabel("SHUFFLING")
            shuffling.setStyleSheet("background-color: #d3d3d3;" "border: 7px solid black;" "color: black")
            shuffling.setFont(QFont("Times", 95))
            shuffling.setAlignment(Qt.AlignCenter)
            self.choices.addWidget(shuffling, 0, 1)
            self.generalLayout.addLayout(self.choices)
            self.deck._shuffleDeck()
            #A 1.5 second delay is added so the player can see the deck is being shuffled.
            QTest.qWait(1500)
            #If the deck was shuffled game resets with new deck
            self._reset()

    #Creates menu bar at the top of the GUI
    def _createMenuBar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

        #Creates menu with the back to menu function
        menu = QMenu("&Menu", self)
        menuBar.addMenu(menu)
        self.close1 = QAction("Back To Menu", self)
        menu.addAction(self.close1)

        #Creates help and info and how to play tabs
        helpMenu = QMenu("&Help", self)
        menuBar.addMenu(helpMenu)
        info = QAction("Info", self)
        info.triggered.connect(self._info)

        howToPlay = QAction("How to Play",self)
        howToPlay.triggered.connect(self._help)

        helpMenu.addAction(info)
        helpMenu.addAction(howToPlay)

    #Opens txt file with info on the program. Same for all 4 GUIs in the project
    def _info(self):
        subprocess.call(['notepad.exe', 'Help and Info/Info.txt'])

    #Opens txt file with info on how to play ride the bus
    def _help(self):
        subprocess.call(['notepad.exe', 'Help and Info/How To Play Ride The Bus.txt'])

    #Function is called from manager class in Menu.py, it happens when 'Back to Menu' from the menu is triggered.
    #Resets game with a new deck
    def _resetAll(self):
        self.deck._shuffleDeck()
        self._reset()

#This was made for testing and allows the game to be played without the use of Menu.py
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window1 = RideTheBus()
    window1.show()
    sys.exit(app.exec())

