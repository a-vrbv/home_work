def get_mask_card_number(card_number: int | str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску.
    Номер карты замаскирован и отображается в формате
    XXXX XX** **** XXXX"""
    card_str = str(card_number)
    """Преобразовываем в строку полученные значения"""

    if len(card_str) != 16:
        """Проверяем длину номера карты. Должно быть 16 цифр"""
        raise ValueError("Номер карты состоит из 16 цифр.")

    if not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры.")

    masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    """Преобразовываем номер карты в маску."""
    return masked_number


def get_mask_account(account_number: int | str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX"""

    account_str = str(account_number)

    if len(account_str) < 4:
        """Проверяем длину номера счета. Должно быть не менее 4 цифр"""
        raise ValueError("Номер счета содержит не менее 4 цифр.")

    if not account_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры.")

    masked_account_number = f"**{account_str[-4:]}"
    """Преобразовываем номер счета в маску."""
    return masked_account_number
