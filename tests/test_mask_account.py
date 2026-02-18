import pytest

from src.masks import get_mask_account


# фикстура для проверки корректной маскировки номера счета
@pytest.fixture()
def incorrect_number_account():
    """Фикстура с номерами счет для тестирования. Возвращает список номеров счета, которые содержат, более 4 цифр
    и представлены в форматах строк и целых чисел"""
    return [
        "1234",
        1234,
        "123456",
        123456,
        "1111222233334444",
        1111222233334444,
    ]


def test_incorrect_number_account_from_fixture(incorrect_number_account):
    """Тестируем маскировку корректных номеров счета. Используем фикстуру и проверяем, что результат имеет
    длину более 4 символов без пробела, маскировка выполнена верно и соответствует шаблону.
    Возвращаем которые больше 4 символов."""
    for account in incorrect_number_account:
        result = get_mask_account(account)
        account_str = str(account)

        assert result[-4:] == account_str[-4:]
        assert len(result) == 6
        assert result[:2] == "**"
        assert result[2:].isdigit()


@pytest.fixture()
def incorrect_number_account_length():
    """Фикстура проверки корректной длины счета. Содержит ошибки: короткие номера меньше 4 символов, пустая строка."""
    return [
        "1",
        "12",
        "123",
        "",
    ]


def test_incorrect_number_account_length_from_fixture(incorrect_number_account_length):
    """Тестируем ввод длины карты и выброс ошибок при некорректных данных длины карты при вводе."""
    for account in incorrect_number_account_length:
        with pytest.raises(ValueError, match="Номер счета содержит не менее 4 цифр."):
            get_mask_account(account)


@pytest.mark.parametrize(
    "input_number_account, expected",
    [("1234", "**1234"), (1234, "**1234"), ("12344567", "**4567"), (12344567, "**4567"), ("1234565789", "**5789")],
)
def test_incorrect_number_account(input_number_account, expected):
    """Тест для проверки корректного ввода данных разных типов.
    incorrect_number_account:номер счёта может быть строкой или целым числом
    expected: ожидаемый результат маскировки в формате **XXXX."""
    result = get_mask_account(input_number_account)
    assert result == expected


def test_non_numeric_account():
    """Тест на проверку корректности ввода номера счета. Выбрасывает ошибку, если при вводе были добавлены нечисловые
    символы."""
    with pytest.raises(ValueError, match="Номер счета должен состоять только из цифр."):
        get_mask_account("1#25d5!45d")


def test_non_space_account():
    """Тест на проверку корректности ввода номера счета. Выбрасывает ошибку, если при вводе были добавлены пробелы."""
    with pytest.raises(ValueError, match="Номер счета должен состоять только из цифр."):
        get_mask_account("112 121")
