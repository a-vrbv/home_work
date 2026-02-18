from masks import get_mask_card_number, get_mask_account


def mask_account_card(mask_number: str) -> str:
    """Функция принимает аргумент - строку, содержащую тип и номер карты или счета.
    Аргументом может быть строка типа
    Visa Platinum 7000792289606361, или Maestro 7000792289606361,
    или Счет 73654108430135874305.
    Возвращать строку с замаскированным номером."""

    elements = mask_number.strip().split()
    number = elements[-1]
    """Разбиваем строку на элементы, удаляем пробелы,
    создаем список."""

    if "Счет" in mask_number or "Счёт" in mask_number:
        """Проверяем содержит ли строку 'Счет'.
        Для счета показываем последние 4 цифры"""
        # Используем импортированную функцию для маскирования номера счёта
        hidden_number = get_mask_account(number)
        return f"Счет {hidden_number}"
    else:
        """Для карты показываем первые 6 цифр и последние 4 цифры,
        середину маскируем."""
        # Используем импортированную функцию для маскирования номера карты
        hidden_middle_element = get_mask_card_number(number)
        """Берем название карты и соединяем со скрытым номером."""
        card_name = " ".join(elements[:-1])
        return f"{card_name} {hidden_middle_element}"


def get_date(date_today: str) -> str:
    """Получаем строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"."""

    day = date_today[8:10]
    month = date_today[5:7]
    year = date_today[:4]
    return f"{day}.{month}.{year}"
