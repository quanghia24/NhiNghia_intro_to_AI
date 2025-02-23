import random as rndm
import time

#  define genes and chromosomes
def make_gene(initial=None): # make shuffed row, prefilled values remain in place
    if initial is None:
        initial = [0] * 9 # [0,0,0,0,0,0,0,0,0]
    mapp = {} # position of each number in gene
    gene = list(range(1, 10))
    rndm.shuffle(gene)
    for i in range(9):
        mapp[gene[i]] = i

    for i in range(9):
        if initial[i] != 0 and gene[i] != initial[i]:
            # swapping gene[i] with initial[i]
            temp = gene[i], gene[mapp[initial[i]]]
            gene[mapp[initial[i]]], gene[i] = temp
            mapp[initial[i]], mapp[temp[0]] = i, mapp[initial[i]]
    return gene

def make_chromosome(initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    chromosome = []
    for i in range(9):
        chromosome.append(make_gene(initial[i]))
    return chromosome

# make the first generation
# count == number of child (chromosome) in the first generation
def make_population(count, initial=None): 
    if initial is None:
        initial = [[0] * 9] * 9
    population = []
    for _ in range(count):
        population.append(make_chromosome(initial))
    return population


# fitness function 
'''
The fitness function calculates how "fit" a chromosome (puzzle) is based on:
- For each column: Subtract (number of times a number is seen) - 1 from the fitness for that number
- For each 3x3 square: Subtract (number of times a number is seen) - 1 from the fitness for that number 
- The higher the fitness, the closer the puzzle is to being solved.
'''

def get_fitness(chromosome): # Calculate the fitness of a chromosome (aka a whole puzzle)
    fitness = 0
    for i in range(9): # For each column
        seen = {}
        for j in range(9): # Check each cell in the column
            if chromosome[j][i] in seen:
                seen[chromosome[j][i]] += 1
            else:
                seen[chromosome[j][i]] = 1
        for key in seen: # Subtract fitness for repeated numbers
            fitness -= (seen[key] - 1)
    for m in range(3): # For each 3x3 square
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):  # Check cells in 3x3 square
                for j in range(3 * m, 3 * (m + 1)):
                    if chromosome[j][i] in seen:
                        seen[chromosome[j][i]] += 1
                    else:
                        seen[chromosome[j][i]] = 1
            for key in seen: # Subtract fitness for repeated numbers
                fitness -= (seen[key] - 1)
    return fitness


# chr = make_chromosome() # generate a puzzle
# print(get_fitness(chr))


def print_chr(chr):
    for i in range(9):
        for j in range(9):
            print(chr[i][j], end=" ")
        print("")


# Crossover and Mutation -> to determine the next generation.



# Crossover
def crossover(chr1, chr2):
    new_child_1 = []
    new_child_2 = []
    for i in range(9):
        x = rndm.randint(0, 1)
        if x == 1:
            new_child_1.append(chr1[i])
            new_child_2.append(chr2[i])
        elif x == 0:
            new_child_2.append(chr1[i])
            new_child_1.append(chr2[i])
    return new_child_1, new_child_2

# Mutation
'''
Mutation randomly alters a row (gene) of a chromosome (Sudoku grid) with a certain probability.
This prevents the algorithm from getting stuck in a local minimum and encourages diversity.
The mutation probability (pm) determines how often mutations happen.
'''
def mutation(ch, pm, initial):
    for i in range(9):  # Iterate through all 9 rows (genes)
        x = rndm.randint(0, 100)  # Generate a random number from 0 to 100
        if x < pm * 100:  # If the number is less than the mutation probability (converted to percentage)
            ch[i] = make_gene(initial[i])  # Mutate this row by regenerating it
    return ch



# Implementing The Genetic Algorithm
def read_puzzle(address):
    puzzle = []
    f = open(address, 'r')
    for row in f:
        temp = row.split()
        puzzle.append([int(c) for c in temp])
    return puzzle


def r_get_mating_pool(population): # using random method
    fitness_list = []
    pool = []
    for chromosome in population: # get fitness of each child
        fitness = get_fitness(chromosome)
        fitness_list.append((fitness, chromosome))

    fitness_list.sort() # ascending order (higher is better)

    # rank selection
    weight = list(range(1, len(fitness_list) + 1)) # assign selection weights (better chromosomes have higher selection probabilities)

    for _ in range(len(population)):
        ch = rndm.choices(fitness_list, weight)[0]  # select the first selected chromosome
        pool.append(ch[1])
    return pool

def get_offsprings(population, initial, pm, pc):
    new_pool = []
    i = 0
    while i < len(population):
        ch1 = population[i]
        ch2 = population[(i + 1) % len(population)]
        x = rndm.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = crossover(ch1, ch2)
        new_pool.append(mutation(ch1, pm, initial))
        new_pool.append(mutation(ch2, pm, initial))
        i += 2
    return new_pool

# Population size
POPULATION = 1000

# Number of generations
REPETITION = 1000

# Probability of mutation
PM = 0.1

# Probability of crossover
PC = 0.95

# Main genetic algorithm function
def genetic_algorithm(initial_file):
    initial = read_puzzle(initial_file)
    print_chr(initial)
    population = make_population(POPULATION, initial)
    for _ in range(REPETITION):
        mating_pool = r_get_mating_pool(population)
        rndm.shuffle(mating_pool)
        population = get_offsprings(mating_pool, initial, PM, PC)
        fit = [get_fitness(c) for c in population]
        m = max(fit)
        if m == 0:
            return population
    return population

if __name__ == '__main__':
    start = time.time()
    print("start processing")
    r = genetic_algorithm("./sample_sudoku/Test1.txt")
    end = time.time()
    print("time_taken: ", end - start)
    fit = [get_fitness(c) for c in r]
    m = max(fit)
    print(max(fit))

    # Print the chromosome with the highest fitness
    for c in r:
        if get_fitness(c) == m:
            print_chr(c)
            break
