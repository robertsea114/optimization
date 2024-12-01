import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import minimize


def hash_table(elements, a=1, b=0,m =6, load_factor = 0.75):
    #create a table for the hashing and initialize number and how many rehashes
    table = [[] for _ in range(m)]
    num = 0
    rehash_number = 0

    def rehash():
        #make these varibales global
        nonlocal table, m, num, rehash_number
        old_table = table
        m*=2
        #create new table
        table = [[] for _ in range(m)]
        num = 0
        #update rehash number
        rehash_number += 1
        #for loop to check through old table
        for z in old_table:
            for key in z:
                index = hash_function(key, a, b ,m)
                table[index].append(key)
                num +=1
    collision = 0
    #calculate collisions
    #check element to rehash if needed
    for element in elements:
        if element[0] == "insert":
            key = element[1]
            if num / m > load_factor:
                rehash()
            index = hash_function(key, a, b, m)
            if len(table[index])>0:
                collision +=1
            table[index].append(key)
            num +=1
    return collision, rehash_number


def evaluate_fitness(a,b,m,cost):
    #pull collisions and rehash from the hash table
    collisions, rehash = hash_table([("insert", x) for x in cost], a, b, m)
    return collisions + rehash




                          
def hill_climbing(cost, m, steps = 50):
    #randomize a nd b variables
    a = random.randint(1,10)
    b = random.randint(1,10)
    fitness = evaluate_fitness(a,b,m,cost)
    # for loop iteraters through steps
    for _ in range(steps):
        #gets new a and b values to test
        new_a = a + random.randint(-1,1)
        new_b = b + random.randint(-1,1)
        new_fitness = evaluate_fitness(new_a,new_b,m,cost)
        #check which fitness is better
        if new_fitness < fitness:
            a, b = new_a, new_b
            fitness = new_fitness

    return a, b, fitness

def simulated_annealing(cost, m, steps = 50, initial_temp = 100, cooling_rate =0.95):
    #randomize numbers for a and b
    a = random.randint(1,10)
    b = random.randint(1,10)
    # get the fitness number for those variables
    fitness = evaluate_fitness(a,b,m,cost)
    current_temp = initial_temp
    # for loop iterates through steps to retrive new a and b variables
    for _ in range(steps):
        new_a = a + random.randint(-1,1)
        new_b = b + random.randint(-1,1)
        #calculate new fitness
        new_fitness = evaluate_fitness(new_a,new_b,m,cost)
        # check which fitness is better and update a,b, and finess
        if new_fitness < fitness or np.random.rand() < np.exp(-(new_fitness - fitness) / current_temp):
            a, b = new_a, new_b
            fitness = new_fitness
        # update current temp
        current_temp += cooling_rate
    return a,b,fitness



def nelder_mead(cost,m):
    #objective gets a and b and returns the evaluate fitnnes function
    def objective_function(x):
        a,b = int(x[0]), int(x[1])
        return evaluate_fitness(a,b,m,cost)
    #define the array for initial guess
    initial_guess = [1,0]
    # minimize the objective function with the initial guess using nelder mead
    result = minimize(objective_function,initial_guess, method="Nelder-Mead")
    a, b = int(result.x[0]), int(result.x[1])
    return a,b, result.fun

def compare_optimization(cost, m):
    #Gets numbers from Hill climbing
    hc_a, hc_b, hc_fitness = hill_climbing(cost,m)
    #gets numbers from simualted annealing
    sa_a, sa_b, sa_fitness = simulated_annealing(cost,m)
    #gets numbers from nelder mead
    nm_a, nm_b, nm_fitness = nelder_mead(cost,m)

    print("Hill Climbing: a= ",hc_a, " b= ",hc_b, " fitness= ", hc_fitness )
    print("Simulated Annealing: a= ",sa_a, " b= ",sa_b, " fitness= ", sa_fitness )
    print("Nelder Mead: a= ",nm_a, " b= ",nm_b, " fitness= ", nm_fitness )





# this returns the hash function
def hash_function(x, a, b,m):
    return(a * x +b) % m


# create cost variable to test
cost = [random.randint(0,50) for _ in range(25)]
compare_optimization(cost, m=8)
