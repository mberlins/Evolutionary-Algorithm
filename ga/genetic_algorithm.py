import numpy as np
import random
import sys
import os
import statistics
import math
import copy
import input
import vals
from ga.individual import Individual
from ga.population import Population
import commands.visualize_input as vi
from centerpoint_calculation import CenterpointCalculation

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

    def run(self):
        population = self.init_population()
        cc = CenterpointCalculation(fitness_func=self.fitness_func)

        total_distances = [0, 0, 0, 0, 0, 0]
        centerpoints = []

        for i in range(6):
            centerpoints.append(population.individuals[0])

        for it in range(10):
            for g_num in range(self.generations_num):
                self.calculate_fitness(population)
                # print(f'Generation number: {g_num + 1}')
                # print(population)
                selected = self.selection(population)
                parents, not_paired = self.pair(selected)
                offsprings = self.mate(parents) + not_paired
                population = Population(self.mutate(offsprings))

                # print(f'\n\n\n{g_num}')

                centerpoints[0] = cc.trimmed_mean(population, vals.DEF_TRIMMED_MEAN_COEFF)
                # print(f'Trimmed mean - X: {centerpoints[0].x}, Y: {centerpoints[0].y}, Value: {centerpoints[0].fitness}')
                cc.compare_centerpoint_with_bestpoint(centerpoints[0], population.find_best_individual(), 0)

                centerpoints[1] = cc.hubers_metric(population, vals.DEF_HUBERS_METRIC_COEFF)
                # print(f'Huber\'s metric - X: {centerpoints[1].x}, Y: {centerpoints[1].y}, Value: {centerpoints[1].fitness}')
                cc.compare_centerpoint_with_bestpoint(centerpoints[1], population.find_best_individual(), 1)

                centerpoints[2] = cc.centerpoint_mean(population)
                # print(f'Regular mean - X: {centerpoints[2].x}, Y: {centerpoints[2].y}, Value: {centerpoints[2].fitness}')
                cc.compare_centerpoint_with_bestpoint(centerpoints[2], population.find_best_individual(), 2)

                centerpoints[3] = cc.centerpoint_median(population)
                # print(f'Regular median - X: {centerpoints[3].x}, Y: {centerpoints[3].y}, Value: {centerpoints[3].fitness}')
                cc.compare_centerpoint_with_bestpoint(centerpoints[3], population.find_best_individual(), 3)

                temporary_population = copy.deepcopy(population)
                centerpoints[4] = cc.mean_without_worst_part(temporary_population, vals.DEF_MEAN_WORST_PART_SHARE)
                # print(f'Mean without worst part - X: {centerpoints[4].x}, Y: {centerpoints[4].y}, Value: {centerpoints[4].fitness}')
                cc.compare_centerpoint_with_bestpoint(centerpoints[4], population.find_best_individual(), 4)

                temporary_population = copy.deepcopy(population)
                centerpoints[5] = cc.median_without_worst_part(temporary_population, vals.DEF_MEDIAN_WORST_PART_SHARE)
                # print(f'Median without worst part - X: {centerpoints[5].x}, Y: {centerpoints[5].y}, Value: {centerpoints[5].fitness}')
                cc.compare_centerpoint_with_bestpoint(centerpoints[5], population.find_best_individual(), 5)

                if g_num % vals.DEF_PRINTING_PERIOD == 0:
                    args = vi.parse_args()
                    x, y, results = input.create_function(args.min, args.max, args.step,
                                                          vals.INPUT_FUNCTIONS[args.function_num].formula)
                    # input.create_3D_figure(x, y, results, vals.INPUT_FUNCTIONS[args.function_num].name)
                    input.create_2D_figure(x, y, results, vals.INPUT_FUNCTIONS[args.function_num].name, population,
                                           centerpoints[0])

            best_individual = population.find_best_individual()
            total_distances[0] += centerpoints[0].fitness - best_individual.fitness
            total_distances[1] += centerpoints[1].fitness - best_individual.fitness
            total_distances[2] += centerpoints[2].fitness - best_individual.fitness
            total_distances[3] += centerpoints[3].fitness - best_individual.fitness
            total_distances[4] += centerpoints[4].fitness - best_individual.fitness
            total_distances[5] += centerpoints[5].fitness - best_individual.fitness

            print(f'\nBest individual fitness: {best_individual.fitness}\n')

        for i in range(6):
            print(f'Centerpoint wins: {cc.centerpoint_wins[i] / 10}')
            print(f'Bestpoint wins: {cc.bestpoint_wins[i] / 10}')
            print(f'Draws: {cc.draws[i] / 10}')
            print(f'Average distance to best point: {total_distances[i] / 10}\n')
