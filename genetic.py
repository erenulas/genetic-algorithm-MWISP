import random

# method that is used to generate the initial population
# pop_size: size of population
# num_of_nodes: number of nodes that a graph has
def initial_population(pop_size, num_of_nodes):
    population = []
    for i in range(pop_size):
        tmp = []
        # generates a string whose length is equal to the number of nodes in the graph
        # each element of a string represents the existence of the corresponding node
        # if the element at 0th index is 0, it means that it is not included in the set
        # if it is 1, then it means that the node is included
        for j in range(num_of_nodes):
            rnd = random.randint(0,1)
            tmp.append(rnd)
        # after generating a set, it is added into the population list
        population.append(tmp)
    return population

# method that is used to repair the population
# graph: array representation of the graph read from file
# population: list of the current population
# num_of_nodes: number of nodes that a graph has
def repair(graph, population, num_of_nodes):
    for i in range(len(population)):
        # to repair a member of the population if takes the element of string
        # and checks if that element has an edge with the other remaining elements in the string
        # if there is an edge, then the element is removed
        # this whole process repeats for all the elements in the string and for all the strings in the population
        for j in range(num_of_nodes):
            if population[i][j] == 0:
                continue
            for k in range(j+1, num_of_nodes):
                if graph[j][k] == 1:
                    population[i][k] = 0

# method that is used to get the fitness values of the population
# weight: array that contains the weight values of nodes
# population: list of current population
# num_of_nodes: number of nodes that a graph has
def get_fitness(weight, population, num_of_nodes):
    fitness = []
    for i in range(len(population)):
        weighted_sum = 0
        # finds the summation of the weights of the nodes that are included in a set
        for j in range(num_of_nodes):
            weighted_sum += population[i][j]*weight[j]
        # the resulting sum is the fitness value so it is added to the list fitness
        fitness.append(weighted_sum)
    return fitness

# implementation of the roulette selection method
# fitness: list of fitness values of the population
# population: list of current population
# pop_size: size of the population
def selection(fitness, population, pop_size):
    selected = []
    ratios = []
    # ratio of each fitness value in the total sum is calculated
    for i in range(len(fitness)):
        ratio = (fitness[i]/sum(fitness))
        ratios.append(ratio)
    for i in range(pop_size):
        tmp = 0
        # random number between 0 and 1 is produced
        rnd = random.uniform(0,1)
        # starting from the ratio of the first population
        # we keep adding the ratios until we reach a point
        # where the result of addition is higher than the
        # generated random number
        # in this case, the corresponding set is added
        # to the selected list
        for j in range(len(ratios)):
            tmp += ratios[j]
            if tmp > rnd:
                selected.append(population[j])
                break
    return selected

# implementation of the crossover
# population: list of current population
# cross_prob: crossover probability
# num_of_nodes: size of the population
def crossover(population, cross_prob, num_of_nodes):
    cs_over = []
    ln = len(population)
    for i in range(0,ln,2):
        # random two sets are selected from the population
        rn = random.randint(0,len(population)-1)
        tmp1 = population.pop(rn)
        rn = random.randint(0,len(population)-1)
        tmp2 = population.pop(rn)
        # a random number is generated between 0 and 1
        cross_rand = random.uniform(0,1)
        # if generated random number is lower than the crossover probability
        if cross_rand < cross_prob:
            # a random crossover point is generated between number of nodes and 0
            cs_point = random.randint(0,num_of_nodes-1)
            # crossover happens
            tmp = tmp1[cs_point:]
            tmp1[cs_point:] = tmp2[cs_point:]
            tmp2[cs_point:] = tmp
        # two resulting sets after crossover are added to cs_over list to represent the resulting population
        cs_over.append(tmp1)
        cs_over.append(tmp2)
    return cs_over


# implementation of mutation function
# population: list of current population
# mutation_prob: mutation probability
def mutate(population, mutation_prob):
    for i in range(len(population)):
        j = 0
        # at each turn a random number is generated between 0 and 1
        # if this number is lower than the mutation probability
        # then another random integer is generated fo find a point for applying the mutation
        # the value at that point is flipped
        # this process repeats for 10 points and for for every member of the population
        while j < 10:
            mutate_rand_prob = random.uniform(0,1)
            if mutate_rand_prob < mutation_prob:
                rand_point = random.randint(0,len(population)-1)
                if population[i][rand_point] == 1:
                    population[i][rand_point] = 0
                else:
                    population[i][rand_point] = 1
            j += 1

# filename, generation size, population size, crossover probability, mutation probability are taken as inputs
filename = input("Enter filename: ")
gen_limit = int(input("Enter number of generations: "))
pop_size = int(input("Enter a population size: "))
cross_prob = float(input("Enter a crossover probability: "))
mutat_prob = float(input("Enter a mutation probability: "))

# an array to keep the weights of the nodes
weight = []
# a 2d array to represent the graph
graph = []
# keeps the number of generation
generation = 0

# reading input file
with open(filename, "r") as f:
    i = 0
    for line in f:
        # if this is the 1st line, it represents the number of nodes
        # a 2d array which will represent the graph is initialized
        if i==0:
            num_of_nodes = int(line)
            tmp = [0]*num_of_nodes
            for j in range(num_of_nodes):
                graph.append(list(tmp))
        # if it is the 2nd line, it represents the number of edges
        elif i == 1:
            line = line[:len(line)-1]
            num_of_edges = int(line[0])
        # if it is not the 1st and the 2nd line it means that we are reading the weights of nodes
        elif i < 1003:
            line = line.split()
            weight.append(float(line[1].replace(",", ".")))
        # if it is the remaining lines that it means we are reading the edges
        # if there is an edge between two nodes, then the corresponding cell's value is changed to 1
        else:
            line = line.split()
            graph[int(line[0])][int(line[1])] = 1
        i += 1

# initial population is generated
population = initial_population(pop_size, num_of_nodes)
# initial population is repaired
repair(graph, population, num_of_nodes)
while generation < gen_limit:
    # fitness values for the population is found
    fitness = get_fitness(weight, population, num_of_nodes)
    # line below can be used to observe the average fitness values
    # print(str(sum(fitness)/len(fitness)).replace(".", ","))
    # roulette selection method is applied
    population = selection(fitness, population, pop_size)
    # crossover is applied
    population = crossover(population, cross_prob, num_of_nodes)
    # mutation is applied
    mutate(population, mutat_prob)
    # resulting population is repaired
    repair(graph, population, num_of_nodes)
    generation += 1
# fitness values of the final population is found
fitness = get_fitness(weight, population, num_of_nodes)
# maximum of these fitness values which represents the maximum weight sum is printed as the output
print(max(fitness))
