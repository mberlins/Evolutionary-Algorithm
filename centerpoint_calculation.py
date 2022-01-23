import numpy as np
import random
import statistics
import math
import vals
from ga.individual import Individual
from ga.population import Population
import commands.visualize_input as vi


def sum_wages(wages):
    wages_sum = 0
    for i in range(len(wages)):
        wages_sum += wages[i]

    return wages_sum


class CenterpointCalculation:
    def __init__(self,
                 fitness_func=vals.INPUT_FUNCTIONS[vals.DEF_FITNESS_FUNC_NUM].formula):
        self.fitness_func = fitness_func
        self.centerpoint_wins = [0, 0, 0, 0, 0, 0]
        self.bestpoint_wins = [0, 0, 0, 0, 0, 0]
        self.draws = [0, 0, 0, 0, 0, 0]

    def compare_centerpoint_with_bestpoint(self, centerpoint, bestpoint, method):
        if centerpoint.fitness < bestpoint.fitness:
            self.centerpoint_wins[method] += 1
        elif centerpoint.fitness > bestpoint.fitness:
            self.bestpoint_wins[method] += 1
        else:
            self.draws[method] += 1

    def calculate_centerpoint(self, population, individuals_coors):
        individuals_coors[0] = individuals_coors[0] / len(population.individuals)
        individuals_coors[1] = individuals_coors[1] / len(population.individuals)

        centerpoint = Individual(individuals_coors[0], individuals_coors[1])
        centerpoint.fitness = self.fitness_func(centerpoint.x, centerpoint.y)
        return centerpoint

    def centerpoint_mean(self, population):
        individuals_coors = [0, 0]
        for individual in population.individuals:
            individuals_coors[0] += individual.x
            individuals_coors[1] += individual.y

        return self.calculate_centerpoint(population, individuals_coors)

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
        counter = len(population.individuals) / (1 / worst_part_share)
        for i in range(0, int(counter)):
            worst_index = population.find_worst_individual_index()
            population = population.eliminate_individual(worst_index)

        return self.centerpoint_mean(population)

    def median_without_worst_part(self, population, worst_part_share):
        counter = len(population.individuals) / (1 / worst_part_share)
        for i in range(0, int(counter)):
            worst_index = population.find_worst_individual_index()
            population = population.eliminate_individual(worst_index)

        return self.centerpoint_median(population)

    def trimmed_mean(self, population, c):
        best_individual = population.find_best_individual()
        wages = [[], []]
        for individual in population.individuals:
            difference = math.sqrt((individual.x - best_individual.x) ** 2 + (individual.y - best_individual.y) ** 2)
            if abs(difference) >= c:
                wages[0].append(0)
                wages[1].append(0)
            else:
                wages[0].append(1)
                wages[1].append(1)

        return self.mean_with_wages(population, wages)

    def mean_with_wages(self, population, wages):
        individuals_coors = [0, 0]
        counter = 0
        for individual in population.individuals:
            individuals_coors[0] += wages[0][counter] * individual.x
            individuals_coors[1] += wages[1][counter] * individual.y
            counter += 1

        individuals_coors[0] = individuals_coors[0] / sum_wages(wages[0])
        individuals_coors[1] = individuals_coors[1] / sum_wages(wages[1])

        centerpoint = Individual(individuals_coors[0], individuals_coors[1])
        centerpoint.fitness = self.fitness_func(centerpoint.x, centerpoint.y)
        return centerpoint

    def hubers_metric(self, population, c):
        best_individual = population.find_best_individual()
        wages = [[], []]
        for individual in population.individuals:
            difference = math.sqrt((individual.x - best_individual.x) ** 2 + (individual.y - best_individual.y) ** 2)
            if abs(difference) >= c:
                wages[0].append(c * (2 * abs(individual.x) - c))
                wages[1].append(c * (2 * abs(individual.y) - c))
            else:
                wages[0].append(individual.x ** 2)
                wages[1].append(individual.y ** 2)

        return self.mean_with_wages(population, wages)
