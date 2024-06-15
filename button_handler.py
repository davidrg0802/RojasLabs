import time
from LightStrip import LightStrip, WHITE, RED, YELLOW, BLUE, BLACK
from Buzzer import PassiveBuzzer
from Displays import LCDDisplay
from Button import Button
from Counters import SoftwareTimer
from StateModel import StateModel, BTN1_PRESS, BTN1_RELEASE, BTN2_PRESS, BTN2_RELEASE, BTN3_PRESS, BTN3_RELEASE, BTN4_PRESS, BTN4_RELEASE, TIMEOUT
from alien_base import AlienBase
from player_score import PlayerScore
from starfield import Starfield

class ButtonHandler:
    def __init__(self, size=8, initsize=0):
        """
        Initialize the button handler with various components and game parameters.
        """
        self._size = size
        self._alien_bases = [AlienBase() for _ in range(initsize)]
        self._lights = LightStrip(pin=2, numleds=size, brightness=1)
        self._buz = PassiveBuzzer(17)
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)
        self._timer = SoftwareTimer(handler=self)
        self._button1 = Button(21, 'white', buttonhandler=self)
        self._button2 = Button(20, 'red', buttonhandler=self)
        self._button3 = Button(19, 'yellow', buttonhandler=self)
        self._button4 = Button(18, 'blue', buttonhandler=self)
        self._buttons = [self._button1, self._button2, self._button3, self._button4]
        self._playing = False
        self._score = PlayerScore()
        self._welcome_displayed = False
        self._starfield = Starfield(size)
        
        # Initialize the state model with 4 states and set up transitions
        self._model = StateModel(4, self, debug=True)
        for button in self._buttons:
            self._model.addButton(button)
        self._model.addTimer(self._timer)
        
        # Define state transitions for the state model
        self._model.addTransition(0, [BTN1_PRESS, BTN2_PRESS, BTN3_PRESS, BTN4_PRESS], 1)
        self._model.addTransition(1, [BTN1_PRESS, BTN2_PRESS, BTN3_PRESS, BTN4_PRESS], 2)
        self._model.addTransition(2, [TIMEOUT], 1)
        self._model.addTransition(1, [TIMEOUT], 3)
        self._model.addTransition(3, [BTN1_PRESS, BTN2_PRESS, BTN3_PRESS, BTN4_PRESS], 0)

    def shoot(self, color):
        """
        Handle the shooting mechanism based on the color of the shot.
        """
        if len(self._alien_bases) > 0:
            topbase = self._alien_bases[-1]
            if topbase.getColor() == color:
                # Correct shot: animate the light strip and update score
                for x in range(0, self._size - len(self._alien_bases) + 1):
                    self._lights.setPixel(x, color)
                    time.sleep(0.05)
                    self._lights.setPixel(x, BLACK)
                self._buz.play(500)
                topbase.takeDamage(100)
                if topbase.isDestroyed():
                    self._alien_bases.pop()
                    self._score.addScore(1)
                time.sleep(0.2)
                self._buz.stop()
                self._display.showText(f'Score: {self._score.getScore()}', 0, 3)
            else:
                # Incorrect shot: animate the light strip and play error sound
                for x in range(0, self._size - len(self._alien_bases)):
                    self._lights.setPixel(x, color)
                    time.sleep(0.05)
                    self._lights.setPixel(x, BLACK)
                self._buz.play(600)
                time.sleep(0.2)
                self._buz.stop()

    def buttonPressed(self, name):
        """
        Handle button press events and start the game if not already started.
        """
        if not self._playing:
            self._playing = True
            self._timer.start(0.5)
        elif name == 'white':
            self.shoot(WHITE)
            self._model.processEvent(BTN1_PRESS)
        elif name == 'red':
            self.shoot(RED)
            self._model.processEvent(BTN2_PRESS)
        elif name == 'yellow':
            self.shoot(YELLOW)
            self._model.processEvent(BTN3_PRESS)
        else:
            self.shoot(BLUE)
            self._model.processEvent(BTN4_PRESS)

    def buttonReleased(self, name):
        """
        Handle button release events.
        """
        if name == 'white':
            self._model.processEvent(BTN1_RELEASE)
        elif name == 'red':
            self._model.processEvent(BTN2_RELEASE)
        elif name == 'yellow':
            self._model.processEvent(BTN3_RELEASE)
        else:
            self._model.processEvent(BTN4_RELEASE)

    def timeout(self):
        """
        Handle timeout events by adding a new alien base and updating the display.
        """
        self._alien_bases.append(AlienBase())
        self.refresh()
        if len(self._alien_bases) == self._size:
            self._display.showText('GAME OVER', 1, 3)
            self._timer.cancel()
            time.sleep(3)  # Wait for 3 seconds before restarting the game
            self.reset_game()
            return
        self._timer.start(1)

    def check(self):
        """
        Check the status of the timer.
        """
        self._timer.check()

    def refresh(self):
        """
        Refresh the display to show the current state of the alien bases.
        """
        for x in range(0, len(self._alien_bases)):
            b = self._alien_bases[x]
            if b is not None:
                self._lights.setPixel(self._size - x - 1, b.getColor(), show=False)
        self._lights.show()

    def display_welcome_message(self):
        """
        Display a welcome message at the start of the game.
        """
        self._display.clear()
        self._display.showText(" *STAR INVADER*  ARE YOU READY?")
        time.sleep(2)  # Display welcome message for 2 seconds
        self._display.clear()  # Clear the welcome message
        time.sleep(2)  # Wait for 2 seconds before starting the game

    def run(self):
        """
        Main game loop: display welcome message, refresh display, and run the state model.
        """
        if not self._welcome_displayed:
            self.display_welcome_message()
            self._welcome_displayed = True
            self._playing = True
            self._timer.start(0.5)
        self.refresh()
        self.check()
        self._model.run()

    def clear_lights(self):
        """
        Clear the light strip display.
        """
        for x in range(self._size):
            self._lights.setPixel(x, BLACK)
        self._lights.show()

    def reset_game(self):
        """
        Reset the game state: clear lights, reset alien bases and score, and refresh display.
        """
        self.clear_lights()
        self._alien_bases = [AlienBase() for _ in range(1)]
        self._score.reset()
        self._playing = False
        self._welcome_displayed = False
        self.refresh()