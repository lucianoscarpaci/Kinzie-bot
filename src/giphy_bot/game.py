# !/usr/bin/env python3
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import emoji


class HowManyWubbies(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.num_wubbies = 20
        self.current_player = 1

    def possible_moves(self):
        return [str(i) for i in range(1, min(4, self.num_wubbies + 1))]

    def make_move(self, move):
        self.num_wubbies -= int(move)

    def win(self):
        return self.num_wubbies <= 0

    def scoring(self):
        return -100 if self.win() else 0 

    def is_over(self):
        return self.win()

    def show(self):
        print(emoji.emojize(":bear:") * self.num_wubbies)

    @staticmethod
    def player_start():
        ai_algo = Negamax(8)
        game = HowManyWubbies([Human_Player(), AI_Player(ai_algo)])
        game.current_player = 2
        result = game.play()
        print("Game Over " + emoji.emojize(":ghost:") + " No more Wubbies " + emoji.emojize(":bear:"))


if __name__ == "__main__":
    HowManyWubbies.player_start()
