class Population:
    def __init__(self, individuals):
        self.individuals = individuals

    def __str__(self):
        return f'Population individuals: \n\n' + \
               ''.join([f'{idx}. {ind}\n' for idx, ind in enumerate(self.individuals)]) + \
               f'\nPopulation size: {len(self.individuals)}\n' + \
               '-' * 200
