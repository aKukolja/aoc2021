

limit = 21


distribution = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

def how_many_win(solutions, p1, p2, ps1, ps2, player1_plays):
    # print(p1,p2,ps1,ps2,player1_plays)
    known = solutions[p1][p2][ps1][ps2][player1_plays]
    if known is not None:
        return known
    if ps1 >= limit:
        solutions[p1][p2][ps1][ps2][player1_plays] = (1, 0)
        return (1, 0)
    if ps2 >= limit:
        solutions[p1][p2][ps1][ps2][player1_plays] = (0, 1)
        return (0, 1)
    " games is not won and we have not calculated this solution "
    " we have to store this information "
    argument_wins = 0, 0
    for movement, universe_count in distribution.items():
        if player1_plays == 0:
            " player 1 plays "
            new_p1 = (p1 + movement) % 10
            new_ps1 = ps1 + new_p1 + 1
            " there are <universe_count> universes which lead to this position "
            next_wins = how_many_win(solutions, new_p1, p2, new_ps1, ps2, 1)
            next_wins = next_wins[0] * universe_count, next_wins[1] * universe_count
            argument_wins = argument_wins[0] + next_wins[0], argument_wins[1] + next_wins[1]
        else:
            " player 2 plays "
            new_p2 = (p2 + movement) % 10
            new_ps2 = ps2 + new_p2 + 1
            new_p1w, new_p2w = how_many_win(solutions, p1, new_p2, ps1, new_ps2, 0)
            new_p1w, new_p2w = new_p1w * universe_count, new_p2w * universe_count
            argument_wins = argument_wins[0] + new_p1w, argument_wins[1] + new_p2w
    assert(solutions[p1][p2][ps1][ps2][player1_plays] == None)
    solutions[p1][p2][ps1][ps2][player1_plays] = argument_wins
    return argument_wins


if __name__ == "__main__":
    
    p1 = 2 - 1
    p2 = 7 - 1
    ps1 = 0
    ps2 = 0
    player1_turn = 0

    solutions = [
        [
            
                [
                    [
                        [
                            None for _ in range(2) # player1_plays
                        ]
                        for _ in range(31) # ps2
                    ]
                    for _ in range(31) # ps1
                ]
                for _ in range(10) # p2
            
        ]
        for _ in range(10) # p1
    ]

    p1_wins, p2_wins = how_many_win(solutions, p1, p2, ps1, ps2, player1_turn)
    print("Player 1 wins" if p1_wins > p2_wins else "Player 2 wins")
    print("Player 1:", p1_wins)
    print("Player 2:", p2_wins)



