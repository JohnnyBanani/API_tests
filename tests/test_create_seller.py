import allure
import pytest
from helpers.utils import (
    generate_random_string,
    generate_random_phone,
    generate_random_email,
    generate_random_account_number,
    generate_random_inn,
    generate_random_bik,
    create_seller_request,
)


@allure.feature("Создание продавца")
@allure.story("Успешное создание продавца")
@allure.tag("Positive")
def test_create_seller_success(api_client, seller_data_only):
    with allure.step("Создаём продавца"):
        response = api_client.create_seller(seller_data_only)

    with allure.step("Проверяем статус код и ответ"):
        assert (
            response.status_code == 200
        ), f"Ожидался статус код 200, получен {response.status_code}"

        response_data = response.json()
        assert "seller_id" in response_data, "В ответе отсутствует seller_id"
        assert isinstance(
            response_data["seller_id"], int
        ), "seller_id должен быть целым числом"
        assert (
            response_data["seller_id"] > 0
        ), "seller_id должен быть положительным числом"


@allure.feature("Создание продавца")
@allure.story("Невалидный ИНН")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_inn, expected_status, " "expected_error",
    [
        (783000229, 400, "INN must contain 10 characters"),
        (7830002294123, 400, "INN must contain 10 characters"),
        (-7830002294, 400, "INN must contain 10 characters"),
    ],
)
def test_create_seller_invalid_inn(
    api_client, invalid_inn, expected_status, expected_error
):
    with allure.step("Подготавливаем данные с невалидным ИНН"):
        seller_data = create_seller_request(inn=invalid_inn)

    with allure.step("Отправляем запрос с невалидным ИНН"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем статус код"):
        assert response.status_code == expected_status, (
            f"Ожидался статус код {expected_status}, "
            f"получен {response.status_code}"
        )

    with allure.step("Проверяем сообщение об ошибке"):
        if response.status_code == 400:
            error_data = response.json()
            assert "detail" in error_data, "В ответе отсутствует поле detail"
            assert error_data["detail"] == expected_error, (
                f"Ожидалась ошибка '{expected_error}', "
                f"получена '{error_data['detail']}'"
            )


@allure.feature("Создание продавца")
@allure.story("Невалидный телефон")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_phone, expected_status, expected_error",
    [
        (
            "89991234567",
            400,
            "Phone number must start with "
            "+7 and remain 12 characters long",
        ),
        (
            "+73564887223",
            400,
            "Phone number must start with "
            "+7 and remain 12 characters long",
        ),
        (
            "+7999ABC4569",
            400,
            "Phone number must start with "
            "+7 and remain 12 characters long",
        ),
        (" ", 400, "Phone number must start with "
                   "+7 and remain 12 characters long"),
    ],
)
def test_create_seller_invalid_phone(
        api_client, invalid_phone,
        expected_status, expected_error
):
    with allure.step("Подготавливаем данные с невалидным телефоном"):
        seller_data = create_seller_request(phone=invalid_phone)

    with allure.step("Отправляем запрос с невалидным телефоном"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем статус код"):
        assert response.status_code == expected_status, (
            f"Ожидался статус код {expected_status},"
            f"получен {response.status_code}"
        )

    with allure.step("Проверяем сообщение об ошибке"):
        if response.status_code == 400:
            error_data = response.json()
            assert "detail" in error_data, "В ответе отсутствует поле detail"
            assert error_data["detail"] == expected_error, (
                f"Ожидалась ошибка '{expected_error}', "
                f"получена '{error_data['detail']}'"
            )


@allure.feature("Создание продавца")
@allure.story("Невалидный БИК")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_bik, expected_status, expected_error",
    [
        (14452522, 400, "BIK must contain 9 characters"),
        (1445252221, 400, "BIK must contain 9 characters"),
        (-144525222, 400, "BIK must contain 9 characters"),
        (0, 400, "BIK must contain 9 characters"),
    ],
)
def test_create_seller_invalid_bik(
    api_client, invalid_bik, expected_status, expected_error
):
    with allure.step("Подготавливаем данные с невалидным БИК"):
        seller_data = create_seller_request(bik=invalid_bik)

    with allure.step("Отправляем запрос с невалидным БИК"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем статус код"):
        assert response.status_code == expected_status, (
            f"Ожидался статус код {expected_status},"
            f"получен {response.status_code}"
        )

    with allure.step("Проверяем сообщение об ошибке"):
        if response.status_code == 400:
            error_data = response.json()
            assert "detail" in error_data, "В ответе отсутствует поле detail"
            assert error_data["detail"] == expected_error, (
                f"Ожидалась ошибка '{expected_error}', "
                f"получена '{error_data['detail']}'"
            )


@allure.feature("Создание продавца")
@allure.story("Невалидный email")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_email, "
    "expected_status,"
    "expected_error",
    [
        ("capomail.ru", 400, "Invalid email"),
        ("capo@", 400, "Invalid email"),
        ("capo@.ru", 400, "Invalid email"),
        ("capo @mail.ru", 400, "Invalid email"),
        (" ", 400, "Invalid email"),
        ("капу@mail.ru", 400, "Invalid email"),
    ],
)
def test_create_seller_invalid_email(
    api_client, invalid_email, expected_status, expected_error
):
    with allure.step("Подготавливаем данные с невалидным email"):
        seller_data = create_seller_request(email=invalid_email)

    with allure.step("Отправляем запрос с невалидным email"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем статус код"):
        assert response.status_code == expected_status, (
            f"Ожидался статус код {expected_status},"
            f"получен {response.status_code}"
        )

    with allure.step("Проверяем сообщение об ошибке"):
        if response.status_code == 400:
            error_data = response.json()
            assert "detail" in error_data, \
                "В ответе отсутствует поле detail"
            assert error_data["detail"] == expected_error, (
                f"Ожидалась ошибка '{expected_error}', "
                f"получена '{error_data['detail']}'"
            )


@allure.feature("Создание продавца")
@allure.story("Невалидное название компании")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_company_name, expected_status, expected_error",
    [
        ("", 400, "Company name is required"),
        (" ", 400, "Company name is required"),
        ("company name", 400, "Company name must "
                              "start with ООО, ОАО or ЗАО"),
        ("company", 400, "Company name must start "
                         "with ООО, ОАО or ЗАО"),
        ("Cappuccino LLC", 400, "Company name "
                                "must be in Russian"),
        ("Капучинка Café", 400, "Company name "
                                "must be in Russian"),
    ],
)
def test_create_seller_invalid_company_name(
    api_client, invalid_company_name, expected_status, expected_error
):
    with allure.step("Подготавливаем данные с невалидным названием компании"):
        seller_data = create_seller_request(company_name=invalid_company_name)

    with allure.step("Отправляем запрос с невалидным названием компании"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем статус код"):
        assert response.status_code == expected_status, (
            f"Ожидался статус код {expected_status},"
            f"получен {response.status_code}"
        )

    with allure.step("Проверяем сообщение об ошибке"):
        if response.status_code == 400:
            error_data = response.json()
            assert "detail" in error_data, "В ответе отсутствует поле detail"
            assert error_data["detail"] == expected_error, (
                f"Ожидалась ошибка '{expected_error}', "
                f"получена '{error_data['detail']}'"
            )


@allure.feature("Создание продавца")
@allure.story("Дублирующий запрос")
@allure.tag("Negative")
def test_create_seller_duplicate_request(api_client, seller_data_only):
    with (allure.step("Отправляем первый запрос")):
        response1 = api_client.create_seller(seller_data_only)
        assert response1.status_code == 200, \
            "Первый запрос должен быть успешным"

    with allure.step("Отправляем второй идентичный запрос"):
        response2 = api_client.create_seller(seller_data_only)

    with allure.step("Проверяем конфликт"):
        assert (
            response2.status_code == 409
        ), (f"Ожидался статус код 409, "
            f"получен {response2.status_code}")

    with ((allure.step("Проверяем сообщение об ошибке"))):
        error_data = response2.json()
        assert "detail" in error_data, \
            "В ответе отсутствует поле detail"
        assert error_data["detail"] != "", \
            "Сообщение об ошибке не должно быть пустым"


@allure.feature("Создание продавца")
@allure.story("Валидные варианты email")
@allure.tag("Positive")
@pytest.mark.parametrize(
    "valid_email",
    [
        "CAPO@MAIL.RU",
        "capo_info@mail.ru",
        "capo-info@mail.ru",
        "capo2023@mail.ru",
        "capo.info@mail.ru",
        "capo@company.com",
        "capo@company.org",
        "capo@company.net",
    ],
)
def test_create_seller_valid_email_variations(api_client, valid_email):
    with allure.step("Подготавливаем данные с валидным email"):
        seller_data = create_seller_request(email=valid_email)

    with allure.step("Отправляем запрос с валидным email"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем успешное создание"):
        assert (
            response.status_code == 200
        ), f"Ожидался статус код 200, получен {response.status_code}"

        response_data = response.json()
        assert "seller_id" in response_data, "В ответе отсутствует seller_id"
        assert isinstance(
            response_data["seller_id"], int
        ), "seller_id должен быть целым числом"
        assert (
            response_data["seller_id"] > 0
        ), "seller_id должен быть положительным числом"


@allure.feature("Создание продавца")
@allure.story("Валидные варианты названия компании")
@allure.tag("Positive")
@pytest.mark.parametrize(
    "valid_company_name",
    [
        "ООО 'КАПУЧИНКА'",
        "ООО 'Капучинка-Групп'",
        "ООО 'Капучинка.Групп'",
        "ООО 'Капучинка, Групп'",
        "ООО 'Капучинка & Партнеры'",
    ],
)
def test_create_seller_valid_company_name_variations(api_client,
                                                     valid_company_name):
    with allure.step("Подготавливаем данные с валидным названием компании"):
        seller_data = create_seller_request(company_name=valid_company_name)

    with allure.step("Отправляем запрос с валидным названием компании"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем успешное создание"):
        assert (
            response.status_code == 200
        ), f"Ожидался статус код 200, получен {response.status_code}"

        response_data = response.json()
        assert "seller_id" in response_data, "В ответе отсутствует seller_id"
        assert isinstance(
            response_data["seller_id"], int
        ), "seller_id должен быть целым числом"
        assert (
            response_data["seller_id"] > 0
        ), "seller_id должен быть положительным числом"


@allure.feature("Создание продавца")
@allure.story("Поля в разном порядке")
@allure.tag("Positive")
def test_create_seller_fields_different_order(api_client):
    with allure.step("Подготавливаем данные с полями в разном порядке"):
        seller_data = {
            "bik": generate_random_bik(),
            "email": generate_random_email(),
            "company_name": f"ООО '{generate_random_string(8)}'",
            "inn": generate_random_inn(),
            "phone": generate_random_phone(),
            "account_number": generate_random_account_number(),
        }

    with allure.step("Отправляем запрос с полями в разном порядке"):
        response = api_client.create_seller(seller_data)

    with allure.step("Проверяем успешное создание"):
        assert (
            response.status_code == 200
        ), f"Ожидался статус код 200, получен {response.status_code}"

        response_data = response.json()
        assert "seller_id" in response_data, "В ответе отсутствует seller_id"
        assert isinstance(
            response_data["seller_id"], int
        ), "seller_id должен быть целым числом"
