
from itertools import cycle


class Game:

    def __init__(self, p1, p2):
        self._p1 = (p1 - 1, 0)
        self._p2 = (p2 - 1, 0)
        self._dice = cycle(range(1, 101))
        self._thrown = 0
        self._winner = None

    def _get_roll(self):
        a = next(self._dice)
        b = next(self._dice)
        c = next(self._dice)
        self._thrown += 3
        return a, b, c

    def play(self):
        while True:
            " player 1 "
            pos, score =self._p1
            rolls = self._get_roll()
            pos += sum(rolls)
            pos = pos % 10
            print("player 1 rolls", rolls, "and moves to space", pos+1)
            score += pos + 1
            self._p1 = pos, score
            if score >= 1000:
                self._winner = 1
                break

            " player 2 "
            pos, score =self._p2
            pos += sum(self._get_roll())
            pos = pos % 10
            print("player 2 rolls", rolls, "and moves to space", pos+1)
            score += pos + 1
            self._p2 = pos, score
            if score >= 1000:
                self._winner = 2
                break

    def __str__(self):
        if self._winner == 1:
            return str(self._thrown * self._p2[1])
        elif self._winner == 2:
            return str(self._thrown * self._p1[1])
        else:
            raise Exception()


if __name__ == "__main__":
    game = Game(2, 7)
    game.play()
    print(game)


        


