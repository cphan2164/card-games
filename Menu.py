import RideTheBus
import HigherOrLower
import ScrewTheDealer
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QAction
from PyQt5.QtGui import  QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
import subprocess
"""""
This is the Menu for the small project. The menu has two classes. One class acts as the Menu for GUI. 
The other class connects the menu class to the three playable card games.

@author: Conor Phan
Made in 2021
"""""

#Is the GUI displayed when the application is started. Acts as a homepage
class menu(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.generalLayout = QVBoxLayout()
        self.setWindowTitle('Main Menu')
        self.setFixedSize(1500,1000)
        self.backToMain = False
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createHeader()
        self._createMenu()
        self._createFooter()
        self._createMenuBar()


    #Creates the main menu frame with buttons for each game and a help button
    def _createMenu(self):
        self.selection = QVBoxLayout(self)

        self.higherOrLower = QPushButton('Higher Or Lower')
        self.higherOrLower.setFont(QFont("Times", 90))
        self.higherOrLower.setIcon(QIcon('Cards/upAndDown.png'))
        self.higherOrLower.setIconSize(QSize(500, 300))
        self.selection.addWidget(self.higherOrLower)

        self.screwTheDealer = QPushButton('Screw The Dealer')
        self.screwTheDealer.setFont(QFont("Times", 90))
        self.screwTheDealer.setIcon(QIcon('Cards/screwTheDealer.png'))
        self.screwTheDealer.setIconSize(QSize(400, 200))
        self.selection.addWidget(self.screwTheDealer)

        self.rideTheBus = QPushButton('Ride The Bus')
        self.rideTheBus.setFont(QFont("Times", 90))
        self.rideTheBus.setIcon(QIcon('Cards/rideTheBus.png'))
        self.rideTheBus.setIconSize(QSize(400, 200))
        self.selection.addWidget(self.rideTheBus)

        help = QPushButton('Help')
        help.setFont(QFont("Times", 65))
        help.clicked.connect(self._help)
        self.selection.addWidget(help)

        self.generalLayout.addLayout(self.selection)

    #Calls the txt document to help "users" who struggle with understanding the application
    def _help(self):
        subprocess.call(['notepad.exe', 'Help and Info/HelpMenu.txt'])

    #Creates the Main Menu Title at the top of the screen
    def _createHeader(self):
        header = QLabel("Main Menu")
        header.setFont(QFont("Times", 70))
        header.setAlignment(Qt.AlignCenter)
        self.generalLayout.addWidget(header)

    #Creates the signature at the bottom of the page
    def _createFooter(self):
        signature = QLabel("Made By Conor Phan")
        signature.setFont(QFont("Times", 30))
        signature.setAlignment(Qt.AlignCenter)
        self.generalLayout.addWidget(signature)

    #Creates the Info button on the menu bar at the top of the screen
    def _createMenuBar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

        info = QAction("&Info",self)
        info.triggered.connect(self._info)
        helpMenu = QMenu("&Info", self)
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(info)

    #Calls info, which is a txt document
    def _info(self):
       subprocess.call(['notepad.exe', 'Help and Info/Info.txt'])


#Connects the Menu GUI to each of the three games
class manager:
    def __init__(self):
        #Creates each program, but only shows the main menu
        self.menu = menu()
        self.rideTheBus = RideTheBus.RideTheBus()
        self.screwTheDealer = ScrewTheDealer.ScrewTheDealer()
        self.highOrLow = HigherOrLower.HigherOrLowerGUI()
        self.menu.show()

        #Connects the button in class Menu to opening and closing the games
        #Also connects the "Back to Menu" trigger in the menu bar of each of the games.
        self.menu.higherOrLower.clicked.connect(self._higherOrLower)
        self.highOrLow.close1.triggered.connect(self._close)

        self.menu.rideTheBus.clicked.connect(self._rideTheBus)
        self.rideTheBus.close1.triggered.connect(self._close)

        self.menu.screwTheDealer.clicked.connect(self._screwTheDealer)
        self.screwTheDealer.close1.triggered.connect(self._close)

    #Shows the class HigherOrLower and hides the menu
    #The if statement should never be called, but is there as a safety measure.
    def _higherOrLower(self):
        if self.highOrLow.isVisible():
            self.highOrLow.hide()
        else:
            self.highOrLow.show()
            self.menu.hide()

    # Shows the class RideTheBus and hides the menu
    # The if statement should never be called, but is there as a safety measure.
    def _rideTheBus(self):
        if self.rideTheBus.isVisible():
            self.rideTheBus.hide()
        else:
            self.rideTheBus.show()
            self.menu.hide()

    # Shows the class ScrewTheDealer and hides the menu
    # The if statement should never be called, but is there as a safety measure.
    def _screwTheDealer(self):
        if self.screwTheDealer.isVisible():
            self.screwTheDealer.hide()
        else:
            self.screwTheDealer.show()
            self.menu.hide()

    #This function closes all windows that are open except for menu
    #This one function works as to close all three game GUIs
    #It is called when "Back To Menu" in the menu bar is triggered
    def _close(self):
        self.menu.show()
        if self.highOrLow.isVisible():
            self.highOrLow.hide()
            self.highOrLow._resetAll()
        if self.rideTheBus.isVisible():
            self.rideTheBus.hide()
            self.rideTheBus._resetAll()
        if self.screwTheDealer.isVisible():
            self.screwTheDealer.hide()
            self.screwTheDealer._resetAll()


if __name__ == '__main__':
    global window
    app = QApplication(sys.argv)
    window = manager()
    sys.exit(app.exec())

