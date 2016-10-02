__author__ = 'ohodegaa'

import matplotlib.pyplot as plt
import random

class Player(object):




    def __init__(self, name):
        self.name = name
        self.score = 0
        self.history = []


    def choose_action(self, history):
        while True:
            action_input = input("Choose action (rock, paper, scissor): ")
            if Action.is_action(action_input):
                action = Action(action_input)
                self.history.append(action)
                return action
            else:
                print("Not a valid action. Try again.")


    def get_last_action(self):
        return self.history[-1]


    def get_history(self):
        return self.history

    def get_name(self):
        return self.name

    def get_random(self):
        return random.randint(0,2)



class Random(Player):
    def __init__(self):
        super().__init__("Random")


    def choose_action(self, history):
        action = Action(Action._ACTIONS_[self.get_random()])
        self.history.append(action)
        return action


class Sequential(Player):
    def __init__(self):
        super().__init__("Sequential")
        self.action_count = self.get_random()


    def choose_action(self, history):
        action = Action(Action._ACTIONS_[self.action_count])
        if self.action_count >= 2:
            self.action_count = 0
        else:
            self.action_count += 1

        self.history.append(action)
        return action

class MostCommon(Player):
    def __init__(self):
        super().__init__("MostCommon")


    def choose_action(self, history):
        if len(history) > 0:
            action_index = self.get_most_common_action_index(history)
        else:
            action_index = self.get_random()
        action = Action(Action._ACTIONS_DEFEATED_BY_[action_index])
        self.history.append(action)
        return action

    def get_most_common_action_index(self, history):
        action_count = [0,0,0]
        for action in history:
            if action == Action("rock"):
                action_count[0] += 1
            elif action == Action("paper"):
                action_count[1] += 1
            elif action == Action("scissor"):
                action_count[2] += 1
            else:
                raise ValueError

        return action_count.index(max(action_count))


class Historian(Player):

    remember = 1

    def __init__(self, remember):
        super().__init__("Historian")
        self.remember = remember

    def choose_action(self, history):
        if len(history) >= 2*self.remember:
            action_index = self.get_after_sequence_action_index(history)
        else:
            action_index = self.get_random()
        action = Action(Action._ACTIONS_DEFEATED_BY_[action_index])
        self.history.append(action)
        return action

    def get_after_sequence_action_index(self, history):
        action_count = [0, 0, 0]
        seq_index = 0
        sequence = history[len(history) - self.remember :]
        for i in range(len(history) - self.remember):
            if history[i] == sequence[seq_index]:
                seq_index += 1
            else:
                seq_index = 0
            if seq_index > self.remember - 1:
                action_count[Action._ACTIONS_.index((history[i+1]).action_str)] += 1
                seq_index = 0
        action_index = action_count.index(max(action_count))
        return action_index if action_count is not None else self.get_random()




class Action:

    _ACTIONS_ = ["rock", "paper", "scissor"]
    _ACTIONS_DEFEATED_BY_ = ["paper", "scissor", "rock"]


    action_str = None

    @staticmethod
    def is_action(action_str):
        return action_str in Action._ACTIONS_


    def __init__(self, action_type):
        if action_type not in self._ACTIONS_:
            raise ValueError
        self.action_str = action_type

    def __eq__(self, other):

        return self.action_str == other.action_str

    def __gt__(self, other):
        return self._ACTIONS_.index(self.action_str) != self._ACTIONS_DEFEATED_BY_.index(other.action_str)

    def __str__(self):
        return self.action_str




class RockPaperScissorGame:
    player1 = Historian(3)
    player2 = MostCommon()

    player1_points = []
    player2_points = []


    tie_points = 0

    def get_winner(self, p1_action, p2_action):
        if p1_action == p2_action:
            return None
        if p1_action > p2_action:
            return self.player1
        else:
            return self.player2

    def fire_points(self, winner):
        if winner is None:
            self.tie_points += 1
            self.player1.score += 0.5
            self.player2.score += 0.5
            return
        else:
            winner.score += 1

    def print_last_game_result(self, winner):
        print(self.player1.name, ":", self.player1.get_last_action())
        print(self.player2.name, ":", self.player2.get_last_action())
        if winner is not None:
            print("The winner is: " + winner.name)
        else:
            print("Tie game")

        print("Scoreboard:")
        for player in (self.player1, self.player2):
            print(player.name + ": " + str(player.score))
        print("Tie games:" + str(self.tie_points))
        print("\n\n")

    def play_game(self, games_count):
        for i in range(games_count):
            print("Game number: ", i + 1)
            winner = self.get_winner(self.player1.choose_action(self.player2.history),
                                     self.player2.choose_action(self.player1.history[0:-1]))
            self.fire_points(winner)
            self.print_last_game_result(winner)
            self.player1_points.append(self.player1.score / (i + 1))
            self.player2_points.append(self.player2.score / (i + 1))

        if self.player1.score > self.player2.score:
            game_winner = self.player1
        elif self.player1.score < self.player2.score:
            game_winner = self.player2
        else:
            game_winner = None

        if game_winner is not None:
            print("The winner of the game is: ", end="")
            print(game_winner.name + ", with " + str(game_winner.score) + " points")
        else:
            print("It's a tie! ")

        plt.plot(self.player1_points)
        plt.plot(self.player2_points)
        plt.show()



game = RockPaperScissorGame()

game.play_game(100)