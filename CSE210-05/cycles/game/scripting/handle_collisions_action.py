import constants
import random
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._counter = 0

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_rainbow_color(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        """Updates the score nd moves the food if the snake collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score1 = cast.get_first_actor("score1")
        score2 = cast.get_first_actor("score2")
        coin = cast.get_first_actor("coin")
        cycle1 = cast.get_first_actor("cycle1")
        cycle2 = cast.get_first_actor("cycle2")
        head1 = cycle1.get_head()
        head2 = cycle2.get_head()

        if head1.get_position().equals(coin.get_position()):
            points = coin.get_points()
            score1.add_points(points)
            coin.reset()

        if head2.get_position().equals(coin.get_position()):
            points = coin.get_points()
            score2.add_points(points)
            coin.reset()

    def _handle_addition_segments(self, cast):
        """Updates the snake and adds 
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        cycle1 = cast.get_first_actor("cycle1")
        cycle2 = cast.get_first_actor("cycle2")

        cycle1.grow_trail(1)
        cycle2.grow_trail(1)

    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # Player 1
        cycle1 = cast.get_first_actor("cycle1")
        head1 = cycle1.get_segments()[0]
        segments1 = cycle1.get_segments()[1:]
        score1 = cast.get_first_actor("score1")
        # Player 2
        cycle2 = cast.get_first_actor("cycle2")
        head2 = cycle2.get_segments()[0]
        segments2 = cycle2.get_segments()[1:]
        score2 = cast.get_first_actor("score2")
        
        # Player 1 collision with self
        for segment in segments1:
            if head1.get_position().equals(segment.get_position()):
                self._is_game_over = True
                score2.add_points(1)
        # Player 1 collision with opponent
        for segment in segments2:
            if head1.get_position().equals(segment.get_position()):
                self._is_game_over = True
                score2.add_points(1)
        # Player 2 collision with self
        for segment in segments2:
            if head2.get_position().equals(segment.get_position()):
                self._is_game_over = True
                score1.add_points(1)   
        # Player 2 collision with opponent
        for segment in segments1:
            if head2.get_position().equals(segment.get_position()):
                self._is_game_over = True
                score1.add_points(1)
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycle1 = cast.get_first_actor("cycle1")
            segments1 = cycle1.get_segments()
            cycle2 = cast.get_first_actor("cycle2")
            segments2 = cycle2.get_segments()

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments1:
                segment.set_color(constants.WHITE)
            for segment in segments2:
                segment.set_color(constants.WHITE)

    def _handle_rainbow_color(self, cast):
        
        coin = cast.get_first_actor("coin")
        if coin.get_points() == 8:
            coin.set_text(constants.SPECIAL_COIN_SYMBOL)
            coin.set_rainbow_color()
            if self._counter % 10 == 0:
                coin.set_random_velocity()
            else:
                coin.reset_velocity()
            self._counter += 1
            #print(self._counter)
            
        else:
            coin.set_text(constants.COIN_SYMBOL)
            coin.reset_velocity()
            coin.set_color(constants.COIN_COLOR)
