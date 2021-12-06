import vals


class Population:
    def __init__(self, individuals):
        self.individuals = individuals

    def __str__(self):
        return '-' * vals.DASH_NUM + '\n' + \
               f'Population individuals: \n\n' + \
               ''.join([f'{ind}\n' for ind in self.individuals]) + \
               f'\nPopulation size: {len(self.individuals)}\n' + \
               '-' * vals.DASH_NUM
