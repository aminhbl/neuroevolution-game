import copy

from player import Player
from random import *
import numpy as np


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)

        players = sorted(players, key=lambda player: player.fitness, reverse=True)

        print(players[0].fitness)

        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)
        # TODO (Additional: Learning curve)
        return players[: num_players]

        # selected = []
        # for i in range(num_players):
        #     selected.append(Q_tournament(players))
        # return selected

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:

            # TODO ( Parent selection and child generation )
            shuffle(prev_players)
            next_gen = []
            i = 0
            while i < num_players:

                # Q tournament
                parent1 = Q_tournament(prev_players)
                parent2 = Q_tournament(prev_players)

                # parent1 = choice(prev_players)
                # parent2 = choice(prev_players)

                child1 = self.clone_player(parent1)
                child2 = self.clone_player(parent2)

                chromosome1, chromosome2 = crossover(child1, child2)

                chromosome1 = mutate(chromosome1)
                chromosome2 = mutate(chromosome2)

                child1.nn.reconstruct_weights(chromosome1)
                child2.nn.reconstruct_weights(chromosome2)

                next_gen.append(child1)
                next_gen.append(child2)

                i += 2

            return next_gen

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player


def crossover(child1, child2):
    chromosome1 = flat(child1.nn.weights)
    chromosome2 = flat(child2.nn.weights)

    for index in range(len(chromosome1)):
        if random() < 0.5:
            chromosome1[index], chromosome2[index] = chromosome2[index], chromosome1[index]

    return chromosome1, chromosome2


# def mutate(chromosome):
#     chromosome[randint(0, len(chromosome) - 1)] = np.random.randn()
#     return chromosome

def mutate(chromosome):
    for index in range(len(chromosome)):
        if random() < (1 / len(chromosome)):
            chromosome[index] = np.random.randn()
    return chromosome


def flat(weights):
    flattened = []
    for w in weights:
        flatten = weights[w].flatten()
        flattened.extend(flatten)

    return flattened


def Q_tournament(players):
    c1 = choice(players)
    c2 = choice(players)
    if c1.fitness > c2.fitness:
        return c1
    else:
        return c2
