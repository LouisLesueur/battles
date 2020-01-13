from dataclasses import dataclass
from typing import Callable
import random
import numpy as np
from colorama import Fore, Style

from delay import delay
from tools import tools


@dataclass
class Unit:
    """Basic unit structure.
    Combat attributes (annotations below).
    Elementary actions (move, attack) as delayed orders.
    """

    # todo : too many attributes ?

    side: int  # which side the unit is on (e.g. blue and red armies)
    coords: np.ndarray  # where the unit is (float)
    strategy: Callable = delay(lambda *args: None)  # decision taking
    _health: int = 5  # health remaining
    strength: int = 4  # how much damage inflicted through attacks
    _braveness: int = 100 # braveness of the unit
    reach: int = 1.5  # how far damage can be dealt
    speed: int = 1  # how far the unit can go at a time
    is_dead: bool = False
    is_fleeing: bool = False
    time_fleeing: int = 0
    is_centurion: bool = False

    @property
    def braveness(self):
        return self._braveness

    @braveness.setter
    def braveness(self, value):
        """If braveless falls to 0, unit stats fleeing"""
        self._braveness = max(value, 0)
        self.is_fleeing = self._braveness == 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        """If health falls to 0, unit is dead."""
        self._health = max(value, 0)
        self.is_dead = self._health == 0

    @delay
    def reset_braveness(self):
        """Resets braveness to its initial value"""
        self.braveness = 100
        self.time_fleeing = False

    @delay
    def moral_damage(self, value):
        """Decreases braveness by value"""
        self.braveness -= value

    @delay
    def moral_update(self, value):
        """Increases braveness by value"""
        self.braveness += value

    @delay
    def attack(self, target):
        """Inflict damage according to own strength."""
        target.health -= self.strength

    @delay
    @tools(log="{self.side} par là : {direction}")
    def move(self, direction):
        """Move according to own speed."""
        self.coords += self.speed * direction

    def decide(self, others):
        """Take decision according to own strategy."""
        return self.strategy(self, others)

    def __str__(self):
        """Print health with color code for side."""
        color_code = [Fore.BLUE, Fore.RED]
        return color_code[self.side] + str(self.health) + Style.RESET_ALL
