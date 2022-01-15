import sys


class Population:
    def __init__(self, individuals):
        self.individuals = individuals

    def __str__(self):
        return f'Population individuals: \n\n' + \
               ''.join([f'{idx}. {ind}\n' for idx, ind in enumerate(self.individuals)]) + \
               f'\nPopulation size: {len(self.individuals)}\n' + \
               '-' * 200

    def find_best_individual(self):
        best_index = -1
        best_fitness = sys.maxsize
        counter = 0
        for individual in self.individuals:
            if individual.fitness < best_fitness:
                best_index = counter
                best_fitness = individual.fitness
            counter = counter + 1

        return self.individuals[best_index]

    def find_worst_individual_index(self):
        worst_index = -1
        worst_fitness = 0
        counter = 0
        for individual in self.individuals:
            if individual.fitness > worst_fitness:
                worst_index = counter
                worst_fitness = individual.fitness
            counter = counter + 1

        return worst_index

    def eliminate_individual(self, index):
        self.individuals.pop(index)
        return self
