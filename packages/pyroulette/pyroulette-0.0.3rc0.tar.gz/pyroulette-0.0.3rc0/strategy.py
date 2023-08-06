from pyroulette.roulette import Bet, Placement, Strategy

if __name__ == "__main__":
    print(Bet({-1: 1}).__repr__())  # this should print with 00
    print("get test")
    print(Bet({0: 1})[21])
    print(Bet({21: 1})[21])
    print("sum test")
    print(Bet({0: 1}) + Bet({0: 1}))
    print(Bet({0: 1}) + Bet())
    # this should return 1's in everything but 0 and -1.
    print(
        Strategy(
            placements=[Placement(18, 1, "red"), Placement(18, 1, "black")]
        ).get_bet()
    )
