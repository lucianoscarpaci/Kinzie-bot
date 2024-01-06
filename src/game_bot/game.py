from easyAI import TwoPlayerGame, AI_Player, Negamax
import emoji


class HowManyWubbies(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.num_wubbies = 5
        self.current_player = 1

    def possible_moves(self):
        bear_emoji = "🐻"
        max_bear_emojis = 1  # Maximum number of bear emojis that can be sent as a move
        return [bear_emoji * i for i in range(1, min(max_bear_emojis + 1, self.num_wubbies + 1))]

    def make_move(self, move):
        bear_emoji = "🐻"
        num_bear_emojis = move.count(bear_emoji)
        # old code
        self.num_wubbies -= num_bear_emojis

    def win(self):
        return self.num_wubbies <= 0

    def scoring(self):
        return -100 if self.win() else 0

    def is_over(self):
        return self.win()

    def show(self):

        for i in range(self.num_wubbies):
            print(" " * (self.num_wubbies - i) +
                  emoji.emojize(":bear:") * (1 * i + 1))

    @staticmethod
    def player_start():
        ai_algo = Negamax(8)
        game = HowManyWubbies([AI_Player(ai_algo), AI_Player(ai_algo)])
        game.current_player = 2
        result = game.play()
        print("Game Over " + emoji.emojize(":ghost:") +
              " No more Wubbies " + emoji.emojize(":bear:"))


if __name__ == "__main__":
    HowManyWubbies.player_start()
