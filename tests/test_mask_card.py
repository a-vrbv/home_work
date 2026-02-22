import pytest

from src.masks import get_mask_card_number


# фикстура для корректных номеров карт
@pytest.fixture()
def correct_card_number():
    """Фикстура с номерами карт для тестирования. Возвращает список номеров карт, которые содержат 16 цифр
    и представлены в форматах строк и целых чисел."""
    return [
        "1234567890654321",
        1234567890654321,
        "4444555566667777",
        9999333377775555,
    ]


def test_correct_card_number_fixture(correct_card_number):
    """Тестируем маскировку корректных номеров карт. Используем фикстуру и проверяем, что результат имеет
    длину 19 символов - 16 цифр и 3 пробела после каждой 4ой цифры, маскировка выполнена верно и соответствует шаблону.
    """
    for card in correct_card_number:
        result = get_mask_card_number(card)
        assert len(result) == 19
        assert result[4] == " "
        assert result[7:9] == "**"
        assert result[10:14] == "****"
        assert result[14] == " "


@pytest.fixture()
def incorrect_card_length():
    """Фикстура для проверки длины номера карты. Содержит ошибки в длине карт: короткие, длинные,
    слишком длинные, пустая строка."""
    return [
        "12",
        "49500067",
        " ",
        "1234567891011123910",
    ]


def test_incorrect_card_length_fixture(incorrect_card_length):
    """Тестируем ввод длины карты и выброс ошибок при некорректных данных длины карты при вводе."""
    for card in incorrect_card_length:
        with pytest.raises(ValueError, match="Номер карты состоит из 16 цифр."):
            get_mask_card_number(card)


@pytest.mark.parametrize(
    "card_input,expected",
    [
        ("7777888855552222", "7777 88** **** 2222"),
        (7777888855552222, "7777 88** **** 2222"),
        ("9999888877776666", "9999 88** **** 6666"),
        (1111222233334444, "1111 22** **** 4444"),
    ],
)
def test_incorrect_card_input(card_input, expected):
    """Тест на проверку корректного ввода данных - число, строка.
    Card_input: входной номер карты
    expected: ожидаемый результат."""
    result = get_mask_card_number(card_input)
    assert result == expected


@pytest.mark.parametrize(
    "incorrect_input",
    [
        "1234",
        "",
        "12345678910111213",
    ],
)
def test_incorrect_input(incorrect_input):
    """Тестируем ввод длины карты и выброс ошибок при некорректных данных длины карты при вводе."""
    with pytest.raises(ValueError, match="Номер карты состоит из 16 цифр."):
        get_mask_card_number(incorrect_input)


def test_non_numeric_strings():
    """Тестируем ввод данных с буквами и выброс ошибок при нечисловых строках."""
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры."):
        get_mask_card_number("12452ds4f5sd41f5")
