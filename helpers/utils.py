import random
import string
from typing import Optional


def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку."""
    return "".join(random.choices(
        string.ascii_letters + string.digits, k=length))


def generate_random_phone() -> str:
    """Генерирует случайный телефонный номер."""
    return f"+7{random.randint(9000000000, 9999999999)}"


def generate_random_email() -> str:
    """Генерирует случайный email."""
    return f"test_{generate_random_string(8)}@example.com"


def generate_random_account_number() -> str:
    """Генерирует случайный account_number"""
    return str(random.randint(10000000000000000000, 99999999999999999999))


def generate_random_inn() -> int:
    """Генерирует валидный ИНН (10 цифр),
    согласно российской классификации.
    """
    tax_office_codes = [
        "7701", "7702", "7703", "7704", "7705",
        "7706", "7707", "7708", "7709", "7710",
        "7801", "7802", "7803", "7804", "7805",
        "7806", "7807", "7808", "7809", "7810",
        "5201", "5202", "5203", "5204", "5205",
        "5401", "5402", "5403", "5404", "5405",
        "5501", "5502", "5503", "5504", "5505",
        "8600", "8601", "8602", "6601", "6602",
        "6603", "6604", "6605", "6301", "6302",
        "6303", "6304", "6305",
    ]
    tax_office_code = random.choice(tax_office_codes)
    record_number = str(random.randint(0, 99999)).zfill(5)
    first_9_digits = tax_office_code + record_number
    coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum = 0
    for i in range(9):
        checksum += int(first_9_digits[i]) * coefficients[i]

    checksum = checksum % 11
    if checksum == 10:
        checksum = 0

    full_inn = first_9_digits + str(checksum)
    return int(full_inn)


def generate_random_bik() -> int:
    """Генерирует валидный БИК"""
    country_code = "14"
    territory_codes = [
        "00", "01", "02", "03", "05",
        "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15",
        "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25",
        "26", "27", "28", "29", "30",
        "31", "32", "33", "34", "35",
        "36", "37", "38", "39", "40",
        "41", "42", "43", "44", "45",
        "46", "47", "48", "49", "50",
        "51", "52", "53", "54", "55",
        "56", "57", "58", "59", "60",
        "61", "62", "63", "64", "65",
        "66", "67", "68", "69", "70",
        "71", "72", "73", "74", "75",
        "76", "77", "78", "79", "80",
        "81", "82", "83", "84", "85",
    ]

    territory_code = random.choice(territory_codes)
    branch_number = str(random.randint(0, 999)).zfill(3)
    control_digit = str(random.randint(0, 99)).zfill(2)

    full_bik = country_code + territory_code + branch_number + control_digit
    return int(full_bik)


def create_seller_request(
    company_name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    account_number: Optional[str] = None,
    inn: Optional[int] = None,
    bik: Optional[int] = None,
) -> dict:
    """Создает запрос на создание продавца с псевдоуникальными значениями."""
    return {
        "company_name": company_name or f"Company_{generate_random_string(8)}",
        "phone": phone or generate_random_phone(),
        "email": email or generate_random_email(),
        "account_number": account_number or generate_random_account_number(),
        "inn": inn or generate_random_inn(),
        "bik": bik or generate_random_bik(),
    }
