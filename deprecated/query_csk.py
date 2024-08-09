import requests
import json
import pandas as pd

def query_conceptnet(concept):
    url = f"https://api.conceptnet.io/c/en/{concept}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for edge in data['edges']:
            start_label = edge['start']['label'] if 'label' in edge['start'] else 'unknown'
            rel_label = edge['rel']['label'] if 'label' in edge['rel'] else 'unknown'
            end_label = edge['end']['label'] if 'label' in edge['end'] else 'unknown'
            results.append([start_label, rel_label, end_label])
        return results
    else:
        return None

def query_candle(inp):
    data = []
    with open('candle_dataset_v1.jsonl', 'r', encoding='utf-8') as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data[:5]

def query_ascent(inp):
    df = pd.read_csv('ascentpp.csv')
    filtered_df = df[df['primary_subject'] == inp]
    result = [(row['primary_subject'], row['relation'], row['tail']) for _, row in filtered_df.iterrows()]
    return result


def query(inp, mdl='conceptnet'):
    if mdl == 'conceptnet':
        return query_conceptnet(inp)
    elif mdl == 'candle':
        return query_candle(inp)
    elif mdl == 'ascent':
        return query_ascent(inp)
    else:
        return None

print(query("pear", 'conceptnet'))