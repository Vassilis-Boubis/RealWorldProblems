import sys
import argparse
import random
from collections import deque

def parse_arguments():
    parser = argparse.ArgumentParser(description='Maximize influence in a social network.')
    parser.add_argument('graph', type=str, help='The file containing the graph edges.')
    parser.add_argument('k', type=int, help='The number of seed nodes to select.')
    parser.add_argument('algorithm', choices=['greedy', 'max_degree'], help='The algorithm to use for seed selection.')
    parser.add_argument('probability', type=float, help='The probability of influence between connected nodes.')
    parser.add_argument('mc', type=int, help='The number of Monte Carlo simulations to run.')
    parser.add_argument('-r', '--random_seed', type=int, help='The random seed for reproducibility.')
    return parser.parse_args()

def read_graph(file):
    graph = {}
    with open(file, 'r') as f:
        for line in f:
            u, v = map(int, line.strip().split())
            if u not in graph:
                graph[u] = []
            graph[u].append(v)
            if v not in graph:
                graph[v] = []
    return graph

def independent_cascade(graph, seeds, p):
    active = set(seeds)
    new_active = deque(seeds)
    while new_active:
        node = new_active.pop()
        for neighbor in graph.get(node, []):
            if neighbor not in active:
                if random.random() < p:
                    active.add(neighbor)
                    new_active.append(neighbor)
    return active

def select_seeds_max_degree(graph, k):
    node_degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    sorted_nodes = sorted(node_degrees.keys(), key=lambda x: (-node_degrees[x], x))  
    return sorted_nodes[:k]


def select_seeds_greedy(graph, k, p, mc):
    seeds = []
    for _ in range(k):
        best_node = None
        best_spread = 0
        for node in set(graph.keys()).difference(seeds):
            total_spread = 0
            for _ in range(mc):
                spread = independent_cascade(graph, seeds + [node], p)
                total_spread += len(spread)
            avg_spread = total_spread / mc
            if avg_spread > best_spread:
                best_node = node
                best_spread = avg_spread
        seeds.append(best_node)
    return seeds

def maximize_influence(graph, k, p, mc, algorithm):
    if algorithm == 'max_degree':
        return select_seeds_max_degree(graph, k)
    elif algorithm == 'greedy':
        return select_seeds_greedy(graph, k, p, mc)

def main():
    args = parse_arguments()
    
    if args.random_seed is not None:
        random.seed(args.random_seed)
    
    graph = read_graph(args.graph)
    
    seeds = maximize_influence(graph, args.k, args.probability, args.mc, args.algorithm)
    
    influences = []
    for i in range(1, len(seeds) + 1):
        total_influence = 0
        for _ in range(args.mc):
            influenced_nodes = independent_cascade(graph, seeds[:i], args.probability)
            total_influence += len(influenced_nodes)
        average_influence = total_influence / args.mc
        influences.append(average_influence)
    
    print("Seeds", seeds)
    print("Influences", influences)

if __name__ == '__main__':
    main()