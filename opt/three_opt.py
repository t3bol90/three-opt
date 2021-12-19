import copy
import numpy as np
import random


def distance_calc(Xdata, city_tour):
    distance = 0
    for k in range(0, len(city_tour[0])-1):
        m = k + 1
        distance = distance + Xdata[city_tour[0][k]-1, city_tour[0][m]-1]
    return distance


def euclidean_distance(x, y):
    distance = 0
    for j in range(0, len(x)):
        distance = (x[j] - y[j])**2 + distance
    return distance**(1/2)


def seed_function(Xdata):
    seed = [[], float("inf")]
    sequence = random.sample(list(range(1, Xdata.shape[0]+1)), Xdata.shape[0])
    sequence.append(sequence[0])
    seed[0] = sequence
    seed[1] = distance_calc(Xdata, seed)
    return seed


def build_coordinates(distance_matrix):
    a = distance_matrix[0, :].reshape(distance_matrix.shape[0], 1)
    b = distance_matrix[:, 0].reshape(1, distance_matrix.shape[0])
    m = (1/2)*(a**2 + b**2 - distance_matrix**2)
    w, u = np.linalg.eig(np.matmul(m.T, m))
    s = (np.diag(np.sort(w)[::-1]))**(1/2)
    coordinates = np.matmul(u, s**(1/2))
    coordinates = coordinates.real[:, 0:2]
    return coordinates


def distance_matrix(coordinates):
   a = coordinates
   b = a.reshape(np.prod(a.shape[:-1]), 1, a.shape[-1])
   return np.sqrt(np.einsum('ijk,ijk->ij',  b - a,  b - a)).squeeze()


def run_2opt(Xdata, city_tour):
    city_list = copy.deepcopy(city_tour)
    best_route = copy.deepcopy(city_list)
    seed = copy.deepcopy(city_list)
    for i in range(0, len(city_list[0]) - 2):
        for j in range(i+1, len(city_list[0]) - 1):
            best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))
            best_route[0][-1] = best_route[0][0]
            best_route[1] = distance_calc(Xdata, best_route)
            if (best_route[1] < city_list[1]):
                city_list[1] = copy.deepcopy(best_route[1])
                for n in range(0, len(city_list[0])):
                    city_list[0][n] = best_route[0][n]
            best_route = copy.deepcopy(seed)
    return city_list


def run(Xdata, city_tour, recursive_seeding=-1):
    if (recursive_seeding < 0):
        count = recursive_seeding - 1
    else:
        count = 0
    city_list = copy.deepcopy(city_tour)
    city_list_old = city_list[1]*2
    iteration = 0
    while (count < recursive_seeding):
        best_route = copy.deepcopy(city_list)
        best_route_1 = run_2opt(Xdata, best_route)
        best_route_2 = [[], 1]
        best_route_3 = [[], 1]
        best_route_4 = [[], 1]
        best_route_5 = [[], 1]
        seed = copy.deepcopy(city_list)
        for i in range(0, len(city_list[0]) - 3):
            for j in range(i+1, len(city_list[0]) - 2):
                for k in range(j+1, len(city_list[0]) - 1):
                    best_route_2[0] = best_route[0][:i+1]+best_route[0][j +
                                                                        1:k+1]+best_route[0][i+1:j+1]+best_route[0][k+1:]
                    best_route_2[1] = distance_calc(Xdata, best_route_2)
                    best_route_3[0] = best_route[0][:i+1]+list(reversed(best_route[0][i+1:j+1]))+list(
                        reversed(best_route[0][j+1:k+1]))+best_route[0][k+1:]
                    best_route_3[1] = distance_calc(Xdata, best_route_3)
                    best_route_4[0] = best_route[0][:i+1]+list(
                        reversed(best_route[0][j+1:k+1]))+best_route[0][i+1:j+1]+best_route[0][k+1:]
                    best_route_4[1] = distance_calc(Xdata, best_route_4)
                    best_route_5[0] = best_route[0][:i+1]+best_route[0][j+1:k+1] + \
                        list(
                            reversed(best_route[0][i+1:j+1]))+best_route[0][k+1:]
                    best_route_5[1] = distance_calc(Xdata, best_route_5)

                    if(best_route_1[1] < best_route[1]):
                        best_route = copy.deepcopy(best_route_1)
                    elif(best_route_2[1] < best_route[1]):
                        best_route = copy.deepcopy(best_route_2)
                    elif(best_route_3[1] < best_route[1]):
                        best_route = copy.deepcopy(best_route_3)
                    elif(best_route_4[1] < best_route[1]):
                        best_route = copy.deepcopy(best_route_4)
                    elif(best_route_5[1] < best_route[1]):
                        best_route = copy.deepcopy(best_route_5)

                if (best_route[1] < city_list[1]):
                    city_list = copy.deepcopy(best_route)
                best_route = copy.deepcopy(seed)
        count = count + 1
        iteration = iteration + 1
        # print('Iteration = ', iteration, '-> Distance =', city_list[1])
        if (city_list_old > city_list[1] and recursive_seeding < 0):
            city_list_old = city_list[1]
            count = -2
            recursive_seeding = -1
        elif(city_list[1] >= city_list_old and recursive_seeding < 0):
            count = -1
            recursive_seeding = -2
    # print(city_list)
    return city_list
