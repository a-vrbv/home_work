def filter_by_state(list_state: list[dict], state: str = "EXECUTED")-> list[dict]:
    result = []
    for item in list_state:
        if 'state' in item and item['state'] == state:
            result.append(item)
    return result



