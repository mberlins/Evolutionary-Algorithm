import numpy as np
import random
import sys
import os
import statistics
import math
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vals
from ga.individual import Individual
from ga.population import Population


class GeneticAlgorithm:
    def __init__(self,
                 pop_size=vals.DEFAULT_POP_SIZE,
                 generations_num=vals.DEF_GENERATIONS_NUM,
                 init_pop_lower_lim=vals.DEF_INIT_POP_LOWER_LIM,
                 init_pop_upper_lim=vals.DEF_INIT_POP_UPPER_LIM,
                 crossover_prob=vals.DEF_MUTATION_PROB,
                 mutation_prob=vals.DEF_MUTATION_PROB,
                 expected_val=vals.DEF_EXP_VAL,
                 stand_dev=vals.DEF_STAND_DEV,
                 fitness_func=vals.INPUT_FUNCTIONS[vals.DEF_FITNESS_FUNC_NUM].formula):
        self.pop_size = pop_size
        self.generations_num = generations_num
        self.init_pop_lower_lim = init_pop_lower_lim
        self.init_pop_upper_lim = init_pop_upper_lim
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.expected_val = expected_val
        self.stand_dev = stand_dev
        self.fitness_func = fitness_func

    def create_individual(self):
        ind_coords = [random.uniform(self.init_pop_lower_lim, self.init_pop_upper_lim) for _ in range(2)]
        return Individual(ind_coords[0], ind_coords[1])

    def init_population(self):
        individuals = [self.create_individual() for _ in range(self.pop_size)]
        return Population(individuals)

    def calculate_fitness(self, population):
        for individual in population.individuals:
            individual.fitness = self.fitness_func(individual.x, individual.y)

    @staticmethod
    def get_weighted_rand_probs(individuals):
        # for minimisation
        fitness = [1 / ind.fitness for ind in individuals]
        fitness_sum = sum(fitness)
        return [fit / fitness_sum for fit in fitness]

    # @staticmethod
    # def roulette_choice(population, odds):
    #     pop_copy = [ind.cumulative_sum for ind in population.individuals]
    #     pop_copy.append(odds)
    #     pop_copy.sort()
    #     return pop_copy.index(odds)

    # roulette wheel selection
    @staticmethod
    def selection(population):
        crossover_probs = GeneticAlgorithm.get_weighted_rand_probs(population.individuals)
        selected = list(np.random.choice(population.individuals,
                                         size=len(population.individuals),
                                         p=crossover_probs))
        return selected

        # another solution

        # fitness_sum = sum([ind.fitness for ind in population.individuals])
        # for ind in population.individuals:
        #     ind.normalized_fitness = ind.fitness / fitness_sum
        # population.individuals.sort(key=lambda ind: ind.normalized_fitness)
        # population.individuals[0].cumulative_sum = population.individuals[0].normalized_fitness
        # for i in range(1, len(population.individuals)):
        #     population.individuals[i].cumulative_sum = population.individuals[i-1].cumulative_sum + \
        #                                                population.individuals[i].normalized_fitness
        #
        # selected_idxs = []
        # for x in range(len(population.individuals) // 2):
        #     selected_idxs.append(GeneticAlgorithm.roulette_choice(population, random()))
        # selected = [population.individuals[selected_idx] for selected_idx in selected_idxs]
        # return selected

    def pair(self, selected):
        parents = []
        for _ in range(int(len(selected) * self.crossover_prob // 2)):
            parent1 = np.random.choice(selected)
            selected.remove(parent1)
            parent2 = np.random.choice(selected)
            selected.remove(parent2)
            parents.append([parent1, parent2])
        return parents, selected

    # exchange of coordinates of points
    @staticmethod
    def mate(parents):
        offsprings = []
        for pair in parents:
            offsprings.append(Individual(pair[0].x, pair[1].y))
            offsprings.append(Individual(pair[1].x, pair[0].y))
        return offsprings

    def mutate(self, offsprings):
        offs_indxs = list(range(len(offsprings)))
        offs_to_mutate_indxs = np.random.choice(offs_indxs, size=round(len(offsprings) * self.mutation_prob))
        for i in offs_to_mutate_indxs:
            gene_num = random.randint(0, 1)
            if gene_num == 0:  # x coordinate
                offsprings[i].x += np.random.normal(self.expected_val, self.stand_dev)
            elif gene_num == 1:  # y coordinate
                offsprings[i].y += np.random.normal(self.expected_val, self.stand_dev)
        return offsprings

    def find_best_individual(self, population):
        best_index = -1
        best_fitness = sys.maxsize
        counter = 0
        for individual in population:
            if individual.fitness < best_fitness:
                best_index = counter
                best_fitness = individual.fitness
            counter = counter + 1

        return population[best_index]

    def find_worst_individual_index(self, population):
        worst_index = -1
        worst_fitness = 0
        counter = 0
        for individual in population.individuals:
            if individual.fitness > worst_fitness:
                worst_index = counter
                worst_fitness = individual.fitness
            counter = counter + 1

        return worst_index

    def eliminate_individual(self, population, index):
        population.individuals.pop(index)
        return population

    def centerpoint_mean(self, population):
        individuals_coors = [0, 0]
        for individual in population.individuals:
            individuals_coors[0] += individual.x
            individuals_coors[1] += individual.y

        individuals_coors[0] = individuals_coors[0] / len(population.individuals)
        individuals_coors[1] = individuals_coors[1] / len(population.individuals)

        centerpoint = Individual(individuals_coors[0], individuals_coors[1])
        centerpoint.fitness = self.fitness_func(centerpoint.x, centerpoint.y)
        return centerpoint

    def centerpoint_median(self, population):
        individuals_coors = [[], []]
        for individual in population.individuals:
            individuals_coors[0].append(individual.x)
            individuals_coors[1].append(individual.y)

        centerpoint_x = statistics.median(individuals_coors[0])
        centerpoint_y = statistics.median(individuals_coors[1])

        centerpoint = Individual(centerpoint_x, centerpoint_y)
        centerpoint.fitness = self.fitness_func(centerpoint.x, centerpoint.y)

        return centerpoint

    def mean_without_worst_part(self, population, worst_part_share):
        counter = len(population.individuals) / (1/worst_part_share)
        for i in range(0, int(counter)):
            worst_index = self.find_worst_individual_index(population)
            population = self.eliminate_individual(population, worst_index)

        return self.centerpoint_mean(population)

    def median_without_worst_part(self, population, worst_part_share):
        counter = len(population.individuals) / (1/worst_part_share)
        for i in range(0, int(counter)):
            worst_index = self.find_worst_individual_index(population)
            population = self.eliminate_individual(population, worst_index)

        return self.centerpoint_median(population)

    def run(self):
        population = self.init_population()
        for g_num in range(self.generations_num):
            self.calculate_fitness(population)
            print(f'Generation number: {g_num + 1}')
            print(population)
            selected = self.selection(population)
            parents, not_paired = self.pair(selected)
            offsprings = self.mate(parents) + not_paired
            population = Population(self.mutate(offsprings))

            if g_num % 2 == 0:
                centerpoint = self.centerpoint_mean(population)
                print(f'X: {centerpoint.x}, Y: {centerpoint.y}, Value: {centerpoint.fitness}')
                centerpoint = self.centerpoint_median(population)
                print(f'X: {centerpoint.x}, Y: {centerpoint.y}, Value: {centerpoint.fitness}')
                temporary_population = copy.deepcopy(population)
                centerpoint = self.mean_without_worst_part(temporary_population, 0.25)
                print(f'X: {centerpoint.x}, Y: {centerpoint.y}, Value: {centerpoint.fitness}')
                temporary_population = copy.deepcopy(population)
                centerpoint = self.median_without_worst_part(temporary_population, 0.25)
                print(f'X: {centerpoint.x}, Y: {centerpoint.y}, Value: {centerpoint.fitness}')




