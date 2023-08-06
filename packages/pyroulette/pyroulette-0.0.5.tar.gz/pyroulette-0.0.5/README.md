# pyroulette

## Explanation

- A `Player` has a `Strategy` which is comprised of a list of `Placements`, which represent a collective `Bet`.
- The player will stick to their strategy.
- Winnings are re-invested (todo: allow specifying player's pyschology, e.g. pocket winnings of certain proportion)
- A player's placement cannot be too complicated (max is 10)
- A `Strategy` is formed at random based on exhausting the strategy budget, which is determined by considering the player's total budget and the minimum number of games they desire to play.
  - It is possible to have some money left over (either due to reaching the maximum number of placements or not having enough money to place a bet with the remaining available chips), meaning the strategy budget is less than the cost to play the strategy.
  - When players cannot play their strategy anymore, they leave the game, meaning they can end the simulation with some remaining money (e.g. `$100` to play a `$40` strategy that you lose twice in a row will leave you with `$20` remaining).

- When using `generate_players`, all players will have the same number of minimum games and budget.


# how to use

```
pip install pyroulette
```

```python
from pyroulette import generate_players, play_roulette

players = generate_players(
    num_players=50,
    min_num_games=min_games,
    total_budget=100
)

players = play_roulette(
    players=players,
    games=1000,
)

print("Results:")
for p in sorted(players, reverse=True):
    print("\n", p)

print("Statistics")
# get the wallet values for all players as a list
wallets = [player.wallet for player in players]

# calculate some statistics
avg_wallet = sum(wallets) / len(wallets)
median_wallet = sorted(wallets)[len(wallets) // 2]

# calculate winnings
winnings = [p.wallet - p.budget for p in players]

num_losers = len([w for w in winnings if w <= 0])
num_winners = len([w for w in winnings if w > 0])
num_bankrupt = len([l for l in wallets if l == 0])

# print the results
print(f"Average wallet value: {avg_wallet}\n")
print(f"Median wallet value: {median_wallet}\n")
print(f"Number of players who lost money: {num_losers}, proportion: {num_losers / len(players):.2f}")
print(f"Number of players who went bankrupt: {num_bankrupt}, proportion: {num_bankrupt / len(players):.2f}")
print()
print(f"Number of players who won more than they started with: {num_winners}, proportion: {num_winners / len(players):.2f}")

```
