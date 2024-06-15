import random
from LightStrip import RED, YELLOW, BLUE, WHITE

class AlienBase:
    def __init__(self, color=None):
        """
        Initialize the alien base with a given color or a random color if none is provided.
        """
        if color:
            self._color = color
        else:
            # Randomly select a color for the alien base
            c = random.randint(1, 4)
            self._color = RED if c == 1 else YELLOW if c == 2 else BLUE if c == 3 else WHITE

    def getColor(self):
        """
        Return the color of the alien base.
        """
        return self._color