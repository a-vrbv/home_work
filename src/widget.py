from masks import get_mask_card_number, get_mask_account

def get_mask_card_number(cart_number: int | str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску.
    Номер карты замаскирован и отображается в формате
    XXXX XX** **** XXXX"""
    cart_str = str(cart_number)
    """Преобразовываем в строку полученные значения"""

    if len(cart_str) != 16:
        """Проверяем длину номера карты. Должно быть 16 цифр"""
        raise ValueError("Номер карты состоит из 16 цифр.")

    masked_number = f"{cart_str[:4]} {cart_str[4:6]}** ****{cart_str[-4:]}"
    """Преобразовываем номер карты в маску."""
    return masked_number


def get_mask_account(account_number: int | str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX"""

    account_str = str(account_number)

    if len(account_str) < 4:
        """Проверяем длину номера счета. Должно быть не менее 4 цифр"""
        raise ValueError("Номер счета содержит не менее 4 цифр.")

    masked_account_number = f"**{account_str[-4:]}"
    """Преобразовываем номер счета в маску."""
    return masked_account_number



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
        hidden_number = f"**{number[-4:]}"
        return f"Счет {hidden_number}"
    else:
        """Для карты показываем первые 6 цифр и последние 4 цифры,
        середину маскируем."""
        hidden_middle_element = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        """Берем название карты и соединяем со скрытым номером."""
        cart_name = " ".join(elements[:-1])
        return f"{cart_name} {hidden_middle_element}"


def get_date(date_today: str) -> str:
    """Получаем строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"."""

    day = date_today[8:10]
    month = date_today[5:7]
    year = date_today[:4]
    return f"{day}.{month}.{year}"
