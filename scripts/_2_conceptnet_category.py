import csv
import time
from collections import deque, defaultdict
import os
import sys

def clean_node_name(node):
    return node.replace('/c/en/', '').split('/')[0]

def read_csv(path):
    graph = defaultdict(list)
    with open(path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)
        for row in reader:
            pass
            try:
                _, start, end = row
                graph[clean_node_name(start)].append(clean_node_name(end))
            except UnicodeDecodeError as e:
                print(f"Error decoding line: {row}")
    return graph

def is_correct_context(target_category, neighbor_list, ):
    if target_category == 'container':
        if 'food' in neighbor_list or 'liquid' in neighbor_list:
            return True
        else:
            return False
    else:
        return True

def modified_bfs(graph, term, targets, verbose=False, max_depth=5):
    start_time = time.time()
    queue = deque([(term, [term], 0)])
    visited = set()
    edges_traversed = 0
    found_targets = []
    paths = []
    
    while queue:
        current_term, path, depth = queue.popleft()
        
        if current_term in visited:
            continue
        
        visited.add(current_term)
        
        if depth < max_depth:
            for neighbor in graph[current_term]:
                edges_traversed += 1
                if neighbor in targets and is_correct_context(neighbor, graph[current_term]):
                    '''
                    if verbose:
                        print(f"Edges traversed: {edges_traversed}")
                        print(f"Time taken: {end_time - start_time:.4f} seconds")
                    return [neighbor, path + [neighbor]]
                    '''
                    found_targets.append(neighbor)
                    paths.append(path + [neighbor])
                    max_depth = depth + 1
                else:
                    queue.append((neighbor, path + [neighbor], depth + 1))
                    
    end_time = time.time()
    
    if verbose:
        print(f"Edges traversed: {edges_traversed} in {end_time - start_time:.8f} seconds")
    return [found_targets, paths]

def get_subfolders(folder_path):
    subfolders = [f.name.replace(' ','_') for f in os.scandir(folder_path) if f.is_dir()]
    return subfolders

path = "csk_kbs/conceptnet/assertions_categories.csv"
ccn_g = read_csv(path)
categories = ['container','utensil','decoration','furniture','cookware']

def find_item_category(term):
    return modified_bfs(ccn_g, term, categories, False)


def modalize(categories):
    return max(set(categories), key = categories.count)

# For if you run this file through another file
def get_categories(obj_dict):
    for id, item in obj_dict.items():
        result = find_item_category(item['type'])
        try:
            obj_dict[id]["category"] = modalize(result[0])
        except ValueError:
            obj_dict[id]["category"] = "decoration"
            print(f"Could not find category for {item['type']}")
    return obj_dict

# For if you run this file directly
def demo(terms):
    cats = []
    rels = []
    for term in terms:
        result = find_item_category(term)
        cats.append(f'{term} -> {modalize(result[0])}')
        rels.append(result[1])
    return cats, rels

def main():
    objects = get_subfolders("images/cache")
    categories, relations = demo(objects)
    #print(categories)
    
if __name__ == "__main__":
    main()
