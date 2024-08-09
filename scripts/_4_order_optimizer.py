def optimize_order(obj_dict, reach=0.55):

    ignore = [item_id for item_id, attributes in obj_dict.items() if any(attributes['gpt_attributes'][key] == 1 for key in ['size', 'weight', 'value'])]

    threshold = reach
    ranking_close = []
    ranking_far = []

    for item_id, attributes in obj_dict.items():
        if item_id not in ignore:
            if attributes['gpt_attributes']['distance'] <= threshold:
                ranking_close.append((item_id, attributes))
            else:
                ranking_far.append((item_id, attributes))

    def sorting_key(item):
        attributes = item[1]['gpt_attributes']
        sharpness = attributes['sharpness']
        weight = attributes['weight']
        size = attributes['size']
        distance = attributes['distance']
        return (
            -1 if sharpness >= 0.8 else 0,
            -1 if weight > 0.5 or size > 0.5 else 0,
            -1 if 0.4 < sharpness < 0.8 else 0,
            distance
        )

    ranking_close.sort(key=sorting_key)
    ranking_far.sort(key=sorting_key)

    ranking_close_ids = [item[0] for item in ranking_close]
    ranking_far_ids = [item[0] for item in ranking_far]
    
    return (ranking_close_ids, ranking_far_ids, ignore)





def optimize_order2(obj_dict, reach=0.55):

    ignore = [item_id for item_id, attributes in obj_dict.items() if any(attributes['gpt_attributes'][key] == 1 for key in ['size', 'weight', 'value'])]

    threshold = reach
    ranking_close = []
    ranking_far = []

    for item_id, attributes in obj_dict.items():
        if item_id not in ignore:
            if attributes['gpt_attributes']['distance'] <= threshold:
                ranking_close.append((item_id, attributes))
            else:
                ranking_far.append((item_id, attributes))

    def sorting_key(item):
        attributes = item[1]['gpt_attributes']
        size = attributes['size']
        weight = attributes['weight']
        average_size_weight = (size + weight) / 2
        return -average_size_weight

    ranking_close.sort(key=sorting_key)
    ranking_far.sort(key=sorting_key)

    ranking_close_ids = [item[0] for item in ranking_close]
    ranking_far_ids = [item[0] for item in ranking_far]
    
    return (ranking_close_ids, ranking_far_ids, ignore)
