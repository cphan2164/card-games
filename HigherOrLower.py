from DeckOfCards import DeckOfCards
from copy import deepcopy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
import sys
import subprocess
"""""
This is the Higher Or Lower GUI. It contains only one class, which is the HigherOrLowerGUI class.
This class is the playable game higher or lower.
For more information on the game itself go to Help and Info/How to Play Higher Or Lower.txt
Or in the game itself, go to help and click how to play.

@author: Conor Phan
Made in 2021
"""""

#Score, deckCount, and highscore are started as 0 to make them available to the class and easily to manipulate
class HigherOrLowerGUI(QMainWindow):
    global deck
    deck = DeckOfCards()
    score = 0
    deckCount = 0
    highscore = 0
    
    #Creates the initial GUI visible and calls all functions to build the GUI
    def __init__(self, parent = None):
        super().__init__(parent)
        self.generalLayout = QVBoxLayout()
        self.setWindowTitle('Higher or Lower')
        self.setFixedSize(1500,1000)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createMenuBar()
        self._createDisplay()
        self._createButtons()
        self._createFooter()
        self._firstCard()

    #Creates the Score and Highscore labels seen at the top of the screen.
    def _createDisplay(self):
        header = QHBoxLayout()
        label = QLabel("Score: " + str(self.score))
        label.setFont(QFont("Times", 90))
        self.display = label
        self.display.setFixedHeight(200)
        self.display.setAlignment(Qt.AlignCenter)
        header.addWidget(self.display, 2)
        self.highscoreLabel = QLabel("Highscore: " + str(self.highscore))
        self.highscoreLabel.setFont(QFont("Times", 30))
        self.highscoreLabel.setAlignment(Qt.AlignRight)
        header.addWidget(self.highscoreLabel)

        self.generalLayout.addLayout(header)

    #Creates the deck image, cards placements, and higher or lower buttons
    def _createButtons(self):
        self.buttonsLayout = QGridLayout()
        
        #This is the deck image
        deckLabel = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        deckLabel.setPixmap(pixmap)
        self.buttonsLayout.addWidget(QLabel(), 0,0 )
        self.buttonsLayout.addWidget(deckLabel, 0, 1, 0, 2)

        #This is the image of the card to the left of the buttons
        #This acts as the 1st card, which is the one that "users" compare.
        self.card1Image = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card1Image.setPixmap(pixmap)
        self.buttonsLayout.addWidget(self.card1Image, 0, 3, 0, 4)

        #This is the Up Arrow Button
        buttonUp = QPushButton(self)
        buttonUp.setIcon(QIcon('Cards/UpArrow.png'))
        buttonUp.setIconSize(QSize(200,200))
        buttonUp.clicked.connect(self._clickUp)
        self.buttonsLayout.addWidget(buttonUp, 0, 8)

        #This is the Down Arrow Button
        buttonDown = QPushButton(self)
        buttonDown.setIcon(QIcon('Cards/DownArrow.png'))
        buttonDown.setIconSize(QSize(200,200))
        buttonDown.clicked.connect(self._clickDown)
        self.buttonsLayout.addWidget(buttonDown, 1, 8)

        #This the image of the card to the right of the buttons
        #This acts as the 2nd card, which is the one that was just compared.
        self.card2Image = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card2Image.setPixmap(pixmap)
        self.buttonsLayout.addWidget(self.card2Image, 0, 10, 0, 11)

        #Creates a label to go on top of the deck image, stating the number of cards left.
        #Made to show it is a full deck and "users" could count cards if they wanted to do so.
        self.labelE = QLabel("     Cards Left: " + str(deck._numberOfCards() - 1))
        self.labelE.setFont(QFont("Times", 25))
        self.buttonsLayout.addWidget(self.labelE, 0 , 1, 0, 2)
        self.generalLayout.addLayout(self.buttonsLayout)

    #Creates the bottom of the page, which consists of the five previous cards compared
    #This is made as a request to make it easier to keep track of cards to make better guesses.
    #All five cards are blank to start the game.
    def _createFooter(self):
        footerlayout = QHBoxLayout()

        #Creates a deck label that shows how many decks the user has gone through.
        #Only used to see how long a user has been playing.
        self.labelF = QLabel("Deck Count: " + str(self.deckCount))
        self.labelF.setFont(QFont("Times", 20))
        self.labelF.setAlignment(Qt.AlignLeft)
        footerlayout.addWidget(self.labelF)

        #Five Blank Cards placed at the bottom of the screen
        self.bottom1 = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(228)
        pixmap = pixmap.scaledToWidth(149)
        self.bottom1.setPixmap(pixmap)
        footerlayout.addWidget(self.bottom1)

        self.bottom2 = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(228)
        pixmap = pixmap.scaledToWidth(149)
        self.bottom2.setPixmap(pixmap)
        footerlayout.addWidget(self.bottom2)

        self.bottom3 = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(228)
        pixmap = pixmap.scaledToWidth(149)
        self.bottom3.setPixmap(pixmap)
        self.bottom3.setAlignment(Qt.AlignCenter)
        footerlayout.addWidget(self.bottom3)

        self.bottom4 = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(228)
        pixmap = pixmap.scaledToWidth(149)
        self.bottom4.setPixmap(pixmap)
        self.bottom4.setAlignment(Qt.AlignCenter)
        footerlayout.addWidget(self.bottom4)

        self.bottom5 = QLabel(self)
        pixmap = QPixmap('Cards/blue_back.png')
        pixmap = pixmap.scaledToHeight(228)
        pixmap = pixmap.scaledToWidth(149)
        self.bottom5.setPixmap(pixmap)
        self.bottom5.setAlignment(Qt.AlignCenter)
        footerlayout.addWidget(self.bottom5)

        self.generalLayout.addLayout(footerlayout)

    #Updates the Score and Highscore that are displayed at the top of the program.
    def _changeDisplay(self):
        self.display.setText("Score: " + str(self.score))
        if self.score > self.highscore:
            self.highscore = self.score
            self.highscoreLabel.setText("Highscore: " + str(self.highscore))

    #This updates the footer. It takes the 2nd card and moves it to the first footer card.
    #This takes each used card spot from the one before until it is the 5th used card, then which it disappears.
    def _usedCards(self):
        self.bottom5.setPixmap(self.bottom4.pixmap())
        self.bottom4.setPixmap(self.bottom3.pixmap())
        self.bottom3.setPixmap(self.bottom2.pixmap())
        self.bottom2.setPixmap(self.bottom1.pixmap())

        #Re-formats the most recently compared to card to fit the same size as the other "used cards".
        pixmap = QPixmap(self.card2.image)
        pixmap = pixmap.scaledToHeight(228)
        pixmap = pixmap.scaledToWidth(149)
        self.bottom1.setPixmap(pixmap)


    #Updates the label to state how many cards are left
    #The -1 is to take into account the card being currently compared.
    def _checkCards(self):
        self._usedCards()
        self.labelE.setText("     Cards Left: " + str(deck._numberOfCards() - 1))

        #If there are no cards left the deck shuffles and the deck count label is updated.
        if deck._numberOfCards() - 1 <= 0:
            deck._shuffleDeck()
            self.deckCount = self.deckCount + 1
            self.labelF.setText("Deck Count: " + str(self.deckCount))

    #This is the function the Up Arrow button calls
    def _clickUp(self):
        self._checkCards()
        #Moves the card being compared to the 2nd card spot
        self.card2 = deepcopy(self.card1)
        pixmap = QPixmap(self.card2.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card2Image.setPixmap(pixmap)

        #Shows the next card in the deck to the 1st card spot
        self.card1 = deepcopy(deck._drawCard())
        pixmap = QPixmap(self.card1.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card1Image.setPixmap(pixmap)

        #Compares the 2nd card to the first
        # Since this is click up it compares whether the value of the next card
        # is higher or not then the current card value and updates the display accordingly
        if self.card1.value > self.card2.value:
            self.score = self.score + 1
            self._changeDisplay()
        elif self.card1.value == self.card2.value:
            self.score = self.score
            self._changeDisplay()
        else:
            self.score = 0
            self._changeDisplay()

    #This is the function the Down Arrow button calls.
    def _clickDown(self):
        self._checkCards()

        # Moves the card being compared to the 2nd card spot
        self.card2 = deepcopy(self.card1)
        pixmap = QPixmap(self.card2.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card2Image.setPixmap(pixmap)

        # Shows the next card in the deck to the 1st card spot
        self.card1 = deepcopy(deck._drawCard())
        pixmap = QPixmap(self.card1.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card1Image.setPixmap(pixmap)

        # Compares the 2nd card to the first
        # Since this is click down it compares whether the value of the next card
        # is lower or not then the current card value and updates the display accordingly
        if self.card1.value < self.card2.value:
            self.score = self.score + 1
            self._changeDisplay()
        elif self.card1.value == self.card2.value:
            self.score = self.score
            self._changeDisplay()
        else:
            self.score = 0
            self._changeDisplay()

    #Creates the first card to compare at the beginning of the game.
    #Makes the second card blank, because there were no previous comparisons.
    def _firstCard(self):
        self.card1 = deepcopy(deck._drawCard())
        pixmap = QPixmap(self.card1.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card1Image.setPixmap(pixmap)
        self.card2 = deepcopy(self.card1)
        self.card2.image = 'Cards/blue_back.png'

    #Creates the menu bar for the GUI.
    def _createMenuBar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

    #Creates the back to menu action, which when triggered calls the connected function,
    # which is in the manager class in Menu.py
        menu = QMenu("&Menu", self)
        menuBar.addMenu(menu)
        self.close1 = QAction("Back To Menu", self)
        menu.addAction(self.close1)

    #Creates the help tab and gives two options info and how to play
        helpMenu = QMenu("&Help", self)
        menuBar.addMenu(helpMenu)
        info = QAction("Info", self)
        info.triggered.connect(self._info)

        howToPlay = QAction("How to Play", self)
        howToPlay.triggered.connect(self._help)

        helpMenu.addAction(info)
        helpMenu.addAction(howToPlay)

    #Calls a txt with the info of the project. This is the same info page for all 4 GUIs.
    def _info(self):
        subprocess.call(['notepad.exe', 'Help and Info/Info.txt'])

    #Calls a txt with the information on how to play the current game.
    def _help(self):
        subprocess.call(['notepad.exe', 'Help and Info/How To Play Higher Or Lower.txt'])

    #When the Back To Menu is triggered this function is called
    #It  resets the page to look like when you first clicked on the game, it also shuffles the deck.
    #Except the highscore stays
    def _resetAll(self):
        deck._shuffleDeck()
        self.card1 = deepcopy(deck._drawCard())
        self.deckCount = 0
        self.score = 0

        #Updates deck count and card count in the GUI
        self.labelF.setText("Deck Count: " + str(self.deckCount))
        self.labelE.setText("     Cards Left: " + str(deck._numberOfCards() - 1))

        #Makes the card 2 slot blank again, like when the game is first started.
        self.card2.image = 'Cards/blue_back.png'
        pixmap = QPixmap(self.card2.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card2Image.setPixmap(pixmap)

        #Reveals the 1st card just like when the game is first clicked.
        pixmap = QPixmap(self.card1.image)
        pixmap = pixmap.scaledToHeight(528)
        pixmap = pixmap.scaledToWidth(345)
        self.card1Image.setPixmap(pixmap)

        #Resets the "Used Cards", which is the cards at the footer, to all be blank again.
        i = 0
        while i < 5:
            self._usedCards()
            i = i + 1

        #Updates score of game back to 0, but does not update highscore
        self._changeDisplay()


#Allows the program to be ran individually without the Menu, mainly for testing purposes.
if __name__ == '__main__':
    global window1
    app = QApplication(sys.argv)
    window1 = HigherOrLowerGUI()
    window1.show()
    sys.exit(app.exec())







