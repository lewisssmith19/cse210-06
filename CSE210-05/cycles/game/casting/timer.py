from game.casting.actor import Actor

class Timer(Actor):
    """
    A timer to get track of the time. 
    
    The responsibility of Timer is to keep track of the minutes and seconds.

    Attributes:
        _points (int): The points earned in the game.
    """
    def __init__(self, position, minutes=0, seconds=30):
        super().__init__()
        self._requested_minutes = minutes
        self._requested_seconds = seconds
        self._active = True
        self._text = ""

        self.set_position(position)