import constants
from game.scripting.action import Action

class TimerAction(Action):
    """A thing that is done.
    
    The responsibility of action is to do somthing that is integral or important in the game. Thus,
    it has one method, execute(), which should be overridden by derived classes.
    """
    def __init__(self, cast):
        """Constructs a new TimerAction."""
        self._active = True
        timer = cast.get_first_actor("timer")
        self._minutes = timer._requested_minutes
        self._seconds = timer._requested_seconds
        self._temp = 0

    def execute(self, cast, script):
        """Executes the timer action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if self._active:
            self._add_temp(cast)
            self._set_text(cast)

    def _add_temp(self, cast):
        self._temp += 1

        if self._temp == constants.TICS:
            self._compare_time(cast)
            self._temp = 0

    def _compare_time(self, cast):

        if self._seconds == 0 and self._minutes > 0:
            self._seconds = 60
            self._minutes -= 1

        self._seconds -= 1
        timer = cast.get_first_actor("timer")

        # Compare if the timer is over
        if self._minutes == 0 and self._seconds == 0:
            timer._active = False
            self._active = False

    def _set_text(self, cast):
        
        timer = cast.get_first_actor("timer")

        text = f"{self._minutes:02d}:{self._seconds:02d}"
        timer.set_text(text)