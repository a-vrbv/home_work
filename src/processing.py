def filter_by_state(list_state: list[dict], state: str = "EXECUTED") -> list[dict]:
    result = []
    for item in list_state:
        if "state" in item and item["state"] == state:
            result.append(item)
    return result


def sort_by_date(list_date: list[dict], reverse=True) -> list[dict]:
    result_date = list(list_date)
    sorted_result = []

    while result_date:
        if reverse:
            item = max(result_date, key=lambda x: x["date"])
        else:
            item = min(result_date, key=lambda x: x["date"])

        sorted_result.append(item)
        result_date.remove(item)

    return sorted_result
