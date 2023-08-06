from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import reduce
from random import choice, randint
from statistics import mean, stdev
from typing import Dict, List, Optional

SINGLE_BETS = {str(i) for i in range(-1, 37)}

FEASIBLE_MOVES = sorted(
    {
        *[f"street-{i}" for i in range(1, 14)],
        *[f"col-{i}" for i in range(1, 4)],
        *[f"corner-{i}-{i+1}-{i+3}-{i+4}" for i in range(1, 33) if (i - 1) % 3 < 2],
        *["1-12", "13-24", "25-36", "1-18", "19-36", "even", "odd", "red", "black"],
        *["triple-0", "triple-00"],
        *SINGLE_BETS,
    }
)


ALIASES = {
    "reds",
    "blacks",
    "evens",
    "odds",
    "first-half",
    "last-half",
    "second-half",
    "first-18",
    "last-18",
    "second-18",
}

CHIP_VALUES = {0.25, 0.5, 1, 5, 10, 25, 50, 100}


def init_spread() -> Dict[int, float]:
    """
    Initializes a bet with all individual placements set to 0.

    Returns
    -------
    Bet
        A dictionary representing the bet.
    """
    D = {i: 0 for i in range(-1, 37)}
    return D


@dataclass
class Bet:
    """A class for representing a bet."""

    spread: Dict[int, float] = field(default_factory=init_spread)

    @property
    def __nonzeros__(self) -> Dict[int, float]:
        nonzeros = dict(filter(lambda x: x[1] > 0, self.spread.items()))
        nonzeros = {k: round(v, 2) for k, v in nonzeros.items()}
        if -1 in nonzeros:
            nonzeros["00"] = nonzeros.pop(-1)
        return nonzeros

    def __repr__(self) -> str:
        """Return a string representation of the bet."""
        return f"Bet({self.__nonzeros__})"

    # define the appearance when using print
    def __str__(self) -> str:
        return json.dumps(self.__nonzeros__, indent=4)

    def __dict__(self) -> Dict[int, float]:
        """Return the bet as a dictionary."""
        return self.spread

    def __add__(self, other: Bet) -> Bet:
        """Combine two bets."""
        return Bet({k: self[k] + other[k] for k in set(self) | set(other)})

    def __setitem__(self, __name: int, __value: float) -> None:
        """Set the value of a placement."""
        self.spread[__name] = __value

    def __getitem__(self, __name: int) -> float:
        """Get the value of a placement."""
        return self.spread.get(__name, 0)

    def copy(self) -> Bet:
        """Return a copy of the bet."""
        return Bet(self.spread.copy())

    def __iter__(self):
        return iter(self.spread.keys())

    def get(self, __name: int) -> float:
        return self.spread.get(__name, 0)


@dataclass
class Placement:
    """
    Defines a bet based on the number of chips and value of each chip.

    Attributes
    ----------
    num : int
        The number of chips to bet.
    amt : float
        The value of each chip.
    on : str
        The type of bet to place for which the chips are being used.

    """

    num: int
    amt: float
    on: str

    def __post_init__(self):
        assert (self.on in FEASIBLE_MOVES) or (self.on in ALIASES), (
            f"Bet `{self.on}` not understood."
            + f"Choose from feasible moves:\n {FEASIBLE_MOVES}"
        )

    def __gt__(self, other):
        return self.amt > other.amt

    def __add__(self, other):
        assert self.on == other.on, "Cannot add placements of different types."
        assert self.amt == other.amt, "Cannot add placements of different values."
        return Placement(self.num + other.num, self.amt, self.on)

    def __eq__(self, other):
        return self.amt == other.amt and self.on == other.on

    @property
    def value(self):
        """
        Returns the value of the bet.
        """
        return self.num * self.amt

    def bet(self, bet=None) -> Bet:
        """
        Places a bet on the wheel based on the bet type.
        """
        return interpret_bet(self.on, self.num * self.amt, bet)


@dataclass
class Strategy:
    """
    A strategy is a list of placements, each of which is a bet on a
    particular number or group of numbers.

    Attributes
    ----------
    budget : float
        The amount of money to spend on the strategy.
    placements : List[Placement]
        A list of placements the player will make.

    """

    budget: float = 200
    placements: List[Placement] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"Strategy(budget={self.budget},"
            + f"value={self.value}, placements={self.placements})"
        )

    @property
    def value(self):
        return sum([p.value for p in self.placements])

    @classmethod
    def generate_random(cls, budget: float, max_placements: int = 10) -> Strategy:
        """
        Generates a random strategy.

        Parameters
        ----------
        budget : float
            The amount of money to spend on the strategy.
        max_placements : int, optional
            The maximum number of placements to include in the strategy.
            (default is 10)

        Returns
        -------
        Strategy
            A random strategy.

        """
        placements = []
        initial_budget = budget
        num_placements = 0

        while (budget > 0) and (num_placements < max_placements):
            amt = choice([v for v in CHIP_VALUES if v <= budget])
            # guarantees the max bet cannot exceed budget:
            # 4 is the max number of chips bc you might as well use a higher chip value.
            num = randint(1, min(budget // amt, 4))
            # select random bet type
            # TODO: consider if this is the logic you want...
            # really let's define a player's profile / psychological disposition.
            # if randint(0, 1) == 0:
            #     on = choice(list(FEASIBLE_MOVES))
            # else:
            #     on = choice(list(SINGLE_BETS))
            on = choice(
                list(FEASIBLE_MOVES)
            )  # TODO: make a parameter, allow for just single bets.
            placement = Placement(num, amt, on)
            placements.append(placement)
            budget -= placement.value
            num_placements += 1

        return Strategy(budget=initial_budget, placements=placements)

    def print_all(self) -> None:
        for p in self.placements:
            print(p)

    def get_bet(self):
        return self.place_bets(self.placements)

    def get_placements(self):
        return self.placements

    @staticmethod
    def place_bets(placements: List[Placement]) -> Bet:
        """
        Places a list of bets on the wheel given a list of Placements.

        Parameters
        ----------
        placements : List[Placement]
            A list of Placements to place on the wheel.

        Returns
        -------
        Bet
            A dictionary representing the bet.
        """
        return sum([p.bet() for p in placements], Bet())


@dataclass
class Player:
    """
    A player of the game.

    Attributes
    ----------
    budget : float
        The amount of money the player starts with.
    strategy : Strategy
        The strategy the player uses to place bets.
    id: int
        The id of the player.
        (default: random int of length 8)
    wallet : float
        The amount of money the player has left.
        (default: budget)
    """

    budget: float
    strategy: Strategy
    id: int = field(default_factory=lambda: randint(1e8, 1e9 - 1))

    def __post_init__(self):
        self.wallet: float = self.budget

    def __repr__(self) -> str:
        _nl = "\n\t"  # custom newline character
        return (
            f"Player(id={self.id}, budget={self.budget}, wallet={self.wallet}, "
            + f"num_placements={len(self.strategy.placements)}, "
            + f"strategy_budget={self.strategy.budget}, "
            + f"strategy_cost={self.strategy.value}"
            + f"\nstrategy:{_nl}{_nl.join(map(str, sorted(self.strategy.placements)))}"
            + "\n)"
        )

    def __lt__(self, other):
        return self.wallet < other.wallet


def expected(bet: Bet) -> float:
    """
    Returns the expected value of a bet.

    Parameters
    ----------
    bet : Bet
        The bet to calculate the expected value of.

    Returns
    -------
    float
        The expected value of the bet.
    """
    bets = list(bet.spread.values())
    cond_bets = filter(lambda x: x > 0, bets)
    amt = sum(bets)
    payout = amt * 36 / 38
    print(
        f"bet: {amt:.2f}, expected: {payout:.2f}: {payout/amt:2.4f}"
        + f"with std {stdev(bets*36)} mean win of"
        + f"{36*mean(cond_bets)} {sum(filter(lambda x: x > 0, bets))}/38 times."
    )
    return payout


def place_bet(bet: Bet, on: int, amount: float) -> Bet:
    """
    Places a bet on a number.

    Parameters
    ----------
    bet : Bet
        The bet to place.
    on : int
        The number to bet on.
    amount : float
        The amount to bet.

    Returns
    -------
    Bet
        A dictionary representing the bet with the new bet placed.
    """
    bet = bet.copy()
    bet[on] += amount
    return bet


def interpret_bet(on="red", amount=0, bet=Optional[Bet]) -> Bet:
    """
    Interprets a bet and returns a dictionary representing the bet.

    Parameters
    ----------
    on : str
        The type of bet to place.
    amount : float
        The amount to bet.
    bet : Bet
        The bet to add to.
        (default is None, which creates a new bet)

    Returns
    -------
    Bet
        A dictionary representing the bet.
    """
    assert (on in FEASIBLE_MOVES) or (
        on in ALIASES
    ), f"Bet `{on}` not understood. Choose from feasible moves:\n {FEASIBLE_MOVES}"
    if bet is None:
        bet = Bet()
    else:
        bet = bet.copy()
    REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    BLACKS = set(range(37)) - REDS
    NUMS = {}
    on = on.strip().replace(" ", "-")
    div = 18
    if on in ("red", "reds"):
        NUMS = REDS
    if on in ("black", "blacks"):
        NUMS = BLACKS
    if on in ("odd", "odds"):
        NUMS = {i for i in range(1, 37) if i % 2 == 0}
    if on in ("even", "evens"):
        NUMS = {i for i in range(1, 37) if i % 2}
    if on in ("1-18", "first-18", "first-half"):
        NUMS = set(range(1, 19))
    if on in ("19-36", "last-18", "last-half", "second-half", "second-18"):
        NUMS = set(range(19, 37))
    if on in ("1-12", "13-24", "25-36"):
        low, high = on.split("-")
        NUMS = set(range(int(low), int(high) + 1))
        div = 12
    if on in ["triple-0", "triple-00"]:
        NUMS = {0, 1, 2} if on == "triple-0" else {-1, 2, 3}
        div = 3
    if not NUMS:
        other_bet = on.split("-")
        if other_bet[0] == "street":
            street = int(other_bet[1]) - 1
            assert street in list(range(13))
            NUMS = {i for i in range(street + 1, street + 4)}
            div = 3
        elif other_bet[0] == "col":
            col = int(other_bet[1]) - 1
            assert col in list(range(0, 3))
            NUMS = {i for i in range(1, 37) if (i - 1) % 3 == col}
            div = 12
        elif (
            other_bet[0] == "split"
        ):  # TODO: validate choices, for now we disallow these.
            num_1, num_2 = int(other_bet[1]), int(other_bet[2])
            NUMS = {num_1, num_2}
            div = 2
        elif other_bet[0] == "corner":
            num_1, num_2 = int(other_bet[1]), int(other_bet[2])
            num_3, num_4 = int(other_bet[3]), int(other_bet[4])
            NUMS = {num_1, num_2, num_3, num_4}
            div = 4
        else:
            try:
                NUMS = {int(on)}
                div = 1
            except ValueError as e:
                raise e(
                    f"Bet `{on}` not understood."
                    + f"Choose from feasible moves:\n {set(range(-1, 37))}"
                )

    bet = reduce(lambda bet, num: place_bet(bet, num, amount / div), NUMS, bet)

    return bet


def simulate_random_strategy(min_num_games=1, total_budget=200) -> Strategy:
    """
    Simulates a random strategy based on the minimum number of games that
    the player wants to play and the total budget that the player has.

    Parameters
    ----------
    min_num_games : int, optional
        The minimum number of games that the player wants to play.
        (default is 1)
    total_budget : float, optional
        The total budget that the player has.
        (default is 200)

    Returns
    -------

    """
    strategy_budget = total_budget // min_num_games
    return Strategy.generate_random(strategy_budget)


def generate_players(num_players=10, min_num_games=1, total_budget=200) -> List[Player]:
    """
    Generates a list of players with random strategies.

    Parameters
    ----------
    num_players : int
        The number of players to generate.
    min_num_games : int
        The minimum number of games each player wants to play
        given their strategy and budget.
    total_budget : float
        The total budget for each player.

    Returns
    -------
    List[Player]
    """
    players = [
        Player(
            budget=total_budget,
            strategy=simulate_random_strategy(
                min_num_games=min_num_games, total_budget=total_budget
            ),
        )
        for i in range(num_players)
    ]

    # if a player has placements with identical `amt` and `on` values,
    # combine them into a single placement
    for player in players:
        placements = []
        for placement in player.strategy.placements:
            if placement in placements:
                placements[placements.index(placement)] += placement
            else:
                placements.append(placement)
        player.strategy.placements = placements
    return players


def spin_wheel(players, verbose=False) -> List[float]:
    """
    Simulates a single game of roulette.

    Parameters
    ----------
    players : List[Player]
        The players in the game.
    verbose : bool
        Whether to print the winning number.

    Returns
    -------
    List[float]

    """
    # pick a random number
    num = randint(-1, 36)
    if verbose:
        print("WINNER:", num)
    # for each player, place their bets on the wheel
    bets = [p.strategy.get_bet() for p in players]
    # for each player, calculate their winnings
    winnings = [36 * bet.get(num) for bet in bets]
    # for each player, calculate their expected winnings
    return winnings


def play_roulette(players: List[Player], games: int = 10) -> List[Player]:
    """
    Simulates playing multiple games of roulette.

    Parameters
    ----------
    players : List[Player]
        The players in the game.
    games : int
        The number of games to play.

    Returns
    -------
    List[Player]
        The players after playing the games.
    """
    losers = []
    for g in range(games):
        if not players:
            break
        # print(f"GAME {g}")
        winnings = spin_wheel(players)
        new_losers = []
        for i, p in enumerate(players):
            p.wallet -= p.strategy.value
            p.wallet += winnings[i]
            # TODO: reinvestment logic goes here.
            # maybe add "reinvest" as a player attribute?
            # if a player runs out of money to keep using their strategy,
            # remove them from the list of players and add them to losers.
            if p.wallet < p.strategy.value:
                new_losers.append(p)
        for losing_player in new_losers:
            players.remove(losing_player)
        losers.extend(new_losers)

    return players + losers
