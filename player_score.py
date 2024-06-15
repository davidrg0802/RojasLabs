class PlayerScore:
    def __init__(self):
        """
        Initialize the player's score to zero.
        """
        self._score = 0

    def addScore(self, points):
        """
        Add points to the player's score.
        """
        self._score += points

    def getScore(self):
        """
        Return the current score of the player.
        """
        return self._score

    def reset(self):
        """
        Reset the player's score to zero.
        """
        self._score = 0