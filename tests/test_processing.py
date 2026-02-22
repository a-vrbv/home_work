import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """
    Фикстура для предоставления тестовых данных — списка транзакций с разными статусами.

    Возвращает список словарей с полями:
    - id: идентификатор транзакции;
    - state: статус (EXECUTED, CANCELLED, PENDING);
    - amount: сумма.

    Используется для проверки фильтрации по различным статусам.
    """
    return [
        {"id": 1, "state": "EXECUTED", "amount": 1000},
        {"id": 2, "state": "CANCELLED", "amount": 500},
        {"id": 3, "state": "EXECUTED", "amount": 2000},
        {"id": 4, "state": "PENDING", "amount": 750},
        {"id": 5, "state": "EXECUTED", "amount": 1500},
    ]


def test_filter_by_default_state(sample_transactions):
    """
    Тест для проверки фильтрации по статусу по умолчанию (EXECUTED).

    Использует фикстуру sample_transactions для получения тестовых данных.
    Проверяет, что:
    - возвращаются только транзакции со статусом EXECUTED;
    - количество результатов соответствует ожидаемому (3 в данном случае);
    - все возвращённые транзакции действительно имеют статус EXECUTED.

    Аргументы:
        sample_transactions (list): список транзакций от фикстуры
    """
    result = filter_by_state(sample_transactions)
    assert len(result) == 3
    for item in result:
        assert item["state"] == "EXECUTED"


@pytest.mark.parametrize(
    "filter_state,expected_count",
    [
        ("EXECUTED", 3),
        ("CANCELLED", 1),
        ("PENDING", 1),
        ("UNKNOWN", 0),  # случай отсутствия транзакций с указанным статусом
    ],
)
def test_filter_by_various_states(sample_transactions, filter_state, expected_count):
    """
    Параметризованный тест для проверки фильтрации по разным статусам.

    Параметры:
        filter_state: статус для фильтрации;
        expected_count: ожидаемое количество транзакций с этим статусом.

    Тест будет запущен 4 раза — для каждого статуса.
    В каждом запуске проверяется, что количество отфильтрованных транзакций соответствует ожидаемому.
    """
    result = filter_by_state(sample_transactions, filter_state)
    assert len(result) == expected_count


def test_empty_list():
    """
    Тест для проверки работы с пустым списком транзакций.

    Проверяет, что функция корректно обрабатывает пустой список и возвращает пустой результат.
    """
    result = filter_by_state([])
    assert result == []


def test_missing_state_field():
    """
    Тест для проверки обработки словарей без поля 'state'.

    Создаёт список транзакций, где некоторые словари не содержат поле 'state'.
    Проверяет, что такие транзакции игнорируются при фильтрации.
    """
    transactions = [
        {"id": 1, "amount": 1000},  # нет поля state
        {"id": 2, "state": "EXECUTED", "amount": 500},
        {"id": 3, "amount": 750},  # нет поля state
    ]
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


@pytest.fixture
def sample_transactions_with_dates():
    """
    Фикстура для предоставления тестовых данных с датами.

    Возвращает список транзакций с полем 'date' в формате ISO.
    Используется для проверки сортировки по датам.
    """
    return [
        {"id": 1, "date": "2024-03-11T02:26:18.671407", "amount": 1000},
        {"id": 2, "date": "2023-12-31T23:59:59.999999", "amount": 500},
        {"id": 3, "date": "2024-01-15T10:30:00.000000", "amount": 2000},
        {"id": 4, "date": "2024-03-11T02:26:18.671407", "amount": 750},  # та же дата, что у id 1
    ]


def test_sort_by_date_descending(sample_transactions_with_dates):
    """
    Тест для проверки сортировки по убыванию дат (reverse=True).
    """
    result = sort_by_date(sample_transactions_with_dates, reverse=True)
    # Самая поздняя дата — 2024-03-11
    assert result[0]["id"] in [1, 4]
    # Самая ранняя дата — 2023-12-31
    assert result[-1]["id"] == 2


def test_sort_by_date_ascending(sample_transactions_with_dates):
    """
    Тест для проверки сортировки по возрастанию дат (reverse=False).
    """
    result = sort_by_date(sample_transactions_with_dates, reverse=False)
    # Самая ранняя дата — 2023-12-31
    assert result[0]["id"] == 2
    # Самая поздняя дата — 2024-03-11
    assert result[-1]["id"] in [1, 4]


@pytest.mark.parametrize(
    "reverse,expected_first_id",
    [
        (True, 1),
        (False, 2),
    ],
)
def test_sort_with_parametrization(sample_transactions_with_dates, reverse, expected_first_id):
    """
    Параметризованный тест для проверки сортировки с разными параметрами reverse.
    """
    result = sort_by_date(sample_transactions_with_dates, reverse)
    assert result[0]["id"] == expected_first_id


def test_identical_dates(sample_transactions_with_dates):
    """
    Тест для проверки сортировки при одинаковых датах.
    """
    result = sort_by_date(sample_transactions_with_dates, reverse=True)
    ids_with_same_date = [item["id"] for item in result if item["date"] == "2024-03-11T02:26:18.671407"]
    assert ids_with_same_date[0] == 1
    assert ids_with_same_date[1] == 4


def test_empty_list_sort():
    """
    Тест для проверки работы с пустым списком транзакций.
    """
    result = sort_by_date([])
    assert result == []
