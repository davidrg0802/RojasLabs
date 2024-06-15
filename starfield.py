class Starfield:
    def __init__(self, size):
        """
        Initialize the starfield with a given size and an empty list of elements.
        """
        self._size = size
        self._elements = []

    def addElement(self, element):
        """
        Add an element (e.g., alien base, player shot) to the starfield.
        """
        self._elements.append(element)

    def removeElement(self, element):
        """
        Remove an element from the starfield.
        """
        self._elements.remove(element)

    def display(self):
        """
        Display all elements in the starfield.
        """
        for element in self._elements:
            # Logic to display each element
            pass