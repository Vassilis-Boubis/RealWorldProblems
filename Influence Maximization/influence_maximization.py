import argparse
import random

parse = argparse.ArgumentParser()
parse.add_argument('-r', type=float, help='an optional float parameter r')
parse.add_argument('graph', help='the graph file')
parse.add_argument('k', type=int, help='an optional int parameter k')
parse.add_argument('mode', choices=['greedy', 'max_degree'], help='the mode of operation')
parse.add_argument('probability', type=float, help='an optional flaot parameter probability')
parse.add_argument('mc', type=int, help='an optional int parameter mc')


args = parse.parse_args()
random.seed(args.r)

with open(args.graph, 'r') as sms:
    g = sms.read()
    gr = g.split()

graph = []
m = 0
for i in range(0, len(gr), 2):
    graph.append([int(gr[i]), int(gr[i+1])])
    if m < int(gr[i]):
        m = int(gr[i])
    elif m < int(gr[i+1]):
        m = int(gr[i+1])

grouped_data = {}
for first, second in graph:
    if first not in grouped_data:
        grouped_data[first] = []
    grouped_data[first].append(second)

r = args.r
k = args.k
probability = args.probability
mode = args.mode
mc = args.mc

def bfs_influence(graph, seed, probability):
    influenced_count = len(seed)
    visited = seed.copy()
    queue = seed.copy()
    
    while queue:
        current_node = queue.pop(0)
        if current_node in graph:
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    if random.random() <= probability:
                        visited.append(neighbor)
                        queue.append(neighbor)
                        influenced_count += 1
        
                   
    return influenced_count

def max_degree():
    infl = [0 for i in range(m + 1)]
    for u, v in graph:
            infl[u] += 1

    seeds = []
    for i in range(max(infl), 0, -1):
        for j in range(len(infl)):
            if infl[j] == i and len(seeds) < k:
                seeds.append(j)

    influence = []
    for i in range(1, len(seeds) + 1):
        influence_sum = 0
        for j in range(mc):
            influence_sum = influence_sum + bfs_influence(grouped_data, seeds[:i].copy(), probability)
        influence.append(influence_sum/mc)

    return seeds, influence

def greedy():
    influence = []
    seeds = []
    unique = []
    for u, v in graph:
        if u not in unique:
            unique.append(u)
        elif v not in unique:
            unique.append(v)

    while len(seeds) < k:
        max_influence = []
        for i in unique:
            infl_sum = 0
            for j in range(mc):
                s = seeds.copy()
                s.append(i)
                infl_sum = infl_sum + bfs_influence(grouped_data, s, probability)
            max_influence.append([i, infl_sum/mc])
        
        max_influence = sorted(max_influence, key=lambda x: x[1], reverse=True)
        u, infl = max_influence[0]
        seeds.append(u)
        influence.append(infl)
        unique.remove(u)

    return seeds, influence

seeds = []
influence = []

if mode == "max_degree":
    seeds, influence = max_degree()
elif mode == "greedy":
    seeds, influence = greedy()

    influence = []
    for i in range(1, len(seeds) + 1):
        influence_sum = 0
        for j in range(mc):
            influence_sum = influence_sum + bfs_influence(grouped_data, seeds[:i].copy(), probability)
        influence.append(influence_sum/mc)

print("Seeds", seeds[:k])
print("Influences", influence)