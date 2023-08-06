from random import choice, randint, seed

from pyroulette import (
    FEASIBLE_MOVES,
    Bet,
    Placement,
    Player,
    Strategy,
    expected,
    generate_players,
    init_spread,
    interpret_bet,
    place_bet,
    play_roulette,
    simulate_random_strategy,
)

if __name__ == "__main__":

    bet = Bet()
    # bet = place_bet(bet, 21, 20)
    print(bet[21])
    # bet = interpret_bet("red", 36, bet)
    # bet = interpret_bet("25-36", 1, bet)
    # bet = interpret_bet("street-1", 3, bet)
    # bet = interpret_bet("street-10", 3, bet)
    # bet = interpret_bet("col-1", 12, bet)

    # james bond
    bet = place_bet(bet, 0, 1)
    for n in range(13, 19):
        bet = place_bet(bet, n, 5)
    bet = interpret_bet("19-36", 14, bet)

    # print(bet[21])

    print("bond")
    print(bet)
    print(expected(bet))
    print()
    print("unknown")
    bet = Bet()
    bet = interpret_bet("1-12", 15, bet)
    bet = interpret_bet("13-24", 15, bet)
    bet = interpret_bet("corner-26-27-29-30", 5, bet)
    bet = interpret_bet("corner-32-33-35-36", 5, bet)
    print(bet)
    print(expected(bet))
    print()
    print("singles")
    bet = Bet()
    bet = place_bet(bet, 21, 40)
    # bet = place_bet(bet, 1, 1)
    print(expected(bet))
    print()
    print("stupid")
    bet = Bet()
    bet = interpret_bet("odd", 18, bet)
    bet = interpret_bet("even", 18, bet)
    # bet = place_bet(bet, -1, 1)
    # bet = place_bet(bet, 0, 1)
    print(expected(bet))

    min_games = randint(1, 10)
    print(
        min_games,
        Player(
            200, simulate_random_strategy(min_num_games=min_games, total_budget=200)
        ),
    )
    # create a list of random Placements

    placements = [
        Placement(randint(1, 10), 1, choice(list(FEASIBLE_MOVES))) for _ in range(10)
    ]

    strategy = Strategy.generate_random(50)

    strategy.print_all()

    # define the minimum number of games that you want players to play

    # print the total sum of all the placements
    print("SUM")
    print(sum([p.value for p in placements]))

    # place the bets
    bet = Strategy.place_bets(placements)

    print(bet)

    # set a random seed
    seed(42)
    # generate players and print them out
    players = generate_players(num_players=3, min_num_games=4, total_budget=200)
    players[0] = player = Player(
        id=0,
        budget=200.0,
        strategy=Strategy(
            budget=50,
            placements=[
                Placement(num=2, amt=5, on="triple-00"),
                Placement(num=1, amt=10, on="col-1"),
                Placement(num=60, amt=0.25, on="corner-23-24-26-27"),
                Placement(num=10, amt=1, on="14"),
                Placement(num=1, amt=5, on="street-2"),
            ],
        ),
    )
    for p in sorted(players):
        print(p, "\n")

    print("======================")
    print("SIMULATING GAMES")
    # simulate 10 games
    # seed(59)
    players = play_roulette(players, games=100000)

    for p in sorted(players):
        print(p, "\n")

    print(player.strategy.get_bet())

    # use sum to add up a list of lists
