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
        original_number = card_input.split()[-1]
        assert result[-4:] == original_number[-4:]
        # Разделяем результат на части
        parts = result.split()
        # Проверяем название карты (первые элементы)
        card_name = " ".join(parts[:-4])  # все элементы, кроме последних 4 (номера)
        expected_name = " ".join(card_input.split()[:-1])
        assert card_name == expected_name
        # Извлекаем замаскированный номер (последние 4 части)
        masked_number_parts = parts[-4:]
        masked_number = " ".join(masked_number_parts)
        # Проверяем полную длину замаскированного номера (с пробелами)
        assert len(masked_number) == 19
        # Проверки структуры маски
        # Первые 4 цифры должны совпадать
        assert masked_number_parts[0] == original_number[:4]
        # Следующие 2 цифры + ** должны совпадать
        assert masked_number_parts[1] == original_number[4:6] + "**"
        # Средняя часть должна быть ****
        assert masked_number_parts[2] == "****"
        # Последние 4 цифры должны совпадать
        assert masked_number_parts[3] == original_number[-4:]


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
        assert result.startswith("Счет ") or result.startswith("Счёт ")
        mask_number = result.split(" ", 1)[1]
        original_number = account_input.split()[-1]

        assert mask_number[-4:] == original_number[-4:]
        if len(mask_number) > 4:
            assert mask_number[:-4].startswith("**")

        assert mask_number[-4:].isdigit()


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
    with pytest.raises(ValueError, match="Номер счета содержит не менее 4 цифр."):
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
