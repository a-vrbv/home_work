def filter_by_state(list_state: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению поля 'state'.

    Args:
        list_state: список словарей, содержащих поле 'state'
        state: значение поля 'state' для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Список словарей, где 'state' равен заданному значению
    """
    result = []
    for item in list_state:
        if "state" in item and item["state"] == state:
            result.append(item)
    return result


def sort_by_date(list_date: list[dict], reverse=True) -> list[dict]:
    """
    Сортирует список словарей по дате в поле 'date'.

    Args:
        list_date: список словарей, содержащих поле 'date'
        reverse: порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Отсортированный список словарей
    """
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
