import csv
import time
from collections import deque, defaultdict

def read_csv(path):
    graph = defaultdict(list)
    with open(path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)
        for row in reader:
            pass
            try:
                _, start, end = row
                graph[start.replace('/c/en/', '')].append(end.replace('/c/en/', ''))
            except UnicodeDecodeError as e:
                print(f"Error decoding line: {row}")
    return graph


def bfs(graph, term, targets, verbose=False, max_depth=3):
    start_time = time.time()
    queue = deque([(term, [term], 0)])
    visited = set()
    edges_traversed = 0
    
    while queue:
        current_term, path, depth = queue.popleft()
        
        if current_term in visited:
            continue
        
        visited.add(current_term)
        
        if depth < max_depth:
            for neighbor in graph[current_term]:
                edges_traversed += 1
                if neighbor in targets:
                    end_time = time.time()
                    if verbose:
                        print(f"Edges traversed: {edges_traversed}")
                        print(f"Time taken: {end_time - start_time:.4f} seconds")
                    return [neighbor, path + [neighbor]]
                else:
                    queue.append((neighbor, path + [neighbor], depth + 1))
    
    end_time = time.time()
    if verbose:
        print(f"Edges traversed: {edges_traversed} in {end_time - start_time:.8f} seconds")
    return [None, None]

path = "csk_kbs/conceptnet/assertions_contexts.csv"
ccn_g = read_csv(path)
rooms = ["kitchen", "bedroom"]


def find_item_location(term):
    return bfs(ccn_g, term, rooms, False)


def find_context_location(terms):
    locs = []
    for term in terms:
        locs.append(find_item_location(term)[0])
    return max(set(locs), key=locs.count)
