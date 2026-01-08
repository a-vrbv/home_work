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
        Для счета показываем последние 4 цифры, остальное маскируем"""
        hidden_element = '*' * (len(number) - 4)
        hidden_number = f"{hidden_element}{number[-4:]}"
        return f"Счет {hidden_number}"
    else:
        """Для карты показываем первые 6 цифр и последние 4 цифры,
        середину маскируем."""
        middle_element = '*' * (len(number) - 10)
        hidden_middle_element = f"{number[:6]}{middle_element}{number[-4:]}"

        """Берем название карты и соединяем со скрытым номером."""
        cart_name = " ".join(elements[:-1])
        return f"{cart_name} {hidden_middle_element}"
