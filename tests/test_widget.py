import pytest

from src.widget import mask_account_card, get_date


# Фикстура для проверки корректной маскировки данных номера карт
@pytest.fixture()
def incorrect_card_input():
    """Фикстура для проверки ввода корректных данных с номерами карт.
    Возвращает список строк с данными - разные типы карт и корректные номера карт."""
    return [
        "Visa 1111222233334444",
        "Mastercard 4444333322221111",
        "Maestro 1000200030004000",
        "American Express 5511334466997788",
    ]


def test_mask_card_incorrect_input(incorrect_card_input):
    """Тест для проверки маскировки номеров карт из фикстуры.
    Проверяем результат - содержит названия карт, номер карты замаскирован, показывает
    первые 6 и последние 4 цифры."""
    for card_input in incorrect_card_input:
        result = mask_account_card(card_input)
        assert " " in result
        last_number = card_input.split()[-1]
        assert result[-4:] == last_number[-4:]
        mask_part = result.split()[-2]
        full_mask_part = " ".join(mask_part)
        assert len(full_mask_part) == 19
        assert full_mask_part[4] == " "
        assert full_mask_part[7:9] == "**"


@pytest.fixture()
def incorrect_account_input():
    """Фикстура для проверки ввода корректных данных
    с номерами счетов. Возвращает список строк - указывает 'Счет' или 'Счёт',
    номера счетов не менее 4 цифр."""
    return [
        "Счет 77778888999944445555",
        "Счёт 6666",
        " Счет 1234567890",
    ]


def test_mask_account_incorrect_input(incorrect_account_input):
    """Тест для проверки маскировки номера счета из фикстуры. Проверяем, что результат
    начинается со слова 'Счет', номер счета замаскирован и сохранены последние 4 цифры."""
    for account_input in incorrect_account_input:
        result = mask_account_card(account_input)
        assert result.startswith("Счет ")
        mask_number = result.split(" ")[1]

        assert len(mask_number) == 6
        assert mask_number[:2] == "**"
        assert mask_number[2:].isdigit()
        original_number = account_input.split()[-1]
        assert mask_number[-4:] == original_number[-4]


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa 7000800090001234", "Visa 7000 80** **** 1234"),
        ("Maestro 1234567891234567", "Maestro 1234 56** **** 4567"),
        ("Mastercard 9999777788884444", "Mastercard 9999 77** **** 4444"),
    ],
)
def test_mask_card_specific_cases(input_str, expected):
    """Тест для проверки конкретных случаев маскировки.
    Есть строка с типом карт и номером и ожидаемый результат."""
    result = mask_account_card(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Счет 7894561237894561", "Счет **4561"),
        ("Счёт 3333", "Счет **3333"),
        ("Счет 1234567890", "Счет **7890"),
    ],
)
def test_mask_account_specific_cases(input_str, expected):
    """Тест на проверку конкретных случаев маскировки.
    Есть строка со словом 'Счет' и ожидаемый результат."""
    result = mask_account_card(input_str)
    assert result == expected


def test_incorrect_account_length():
    """Тест на проверку корректной длины счета менее 4 символов.
    Выбрасывает ошибку, если менее 4 символов."""
    with pytest.raises(ValueError, match="Номер счета должен содержать 4 и более цифр."):
        mask_account_card("Счет 147")


@pytest.fixture
def incorrect_date_inputs():
    """
    Фикстура для предоставления корректных строк с датами.

    Возвращает список строк в формате ISO (YYYY‑MM‑DDTHH:MM:SS.microseconds).
    Используем для проверки корректного преобразования в формат ДД.ММ.ГГГГ.
    """
    return [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59.999999",
        "2000-01-01T00:00:00.000000",
    ]


def test_get_date_incorrect_inputs(incorrect_date_inputs):
    """
    Тест для проверки преобразования валидных дат из фикстуры.
    """
    expected_results = [
        "11.03.2024",
        "31.12.2023",
        "01.01.2000",
    ]

    for date_input, expected in zip(incorrect_date_inputs, expected_results):
        result = get_date(date_input)
        assert result == expected, f"Ожидалось {expected}, но получено {result} для даты {date_input}"
