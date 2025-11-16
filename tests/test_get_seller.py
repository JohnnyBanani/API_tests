import allure
import pytest


@allure.feature("Получение пользователя")
@allure.story("Проверка успешного получения продавца")
@allure.tag("Positive")
def test_get_seller_positive(api_client, create_seller):
    with allure.step("Создаём продавца через фикстуру"):
        expected_seller, seller_id = create_seller
        response = api_client.get_seller(seller_id)

    with allure.step("Проверяем стутус код и ответ"):
        assert (
            response.status_code == 200
        ), "Ожидался статус код 200, при создании пользователя"
        resp_json = response.json()
        assert resp_json["id"] == seller_id, f"Ожидался seller_id {seller_id}"
        assert (
            resp_json["company_name"] == expected_seller["company_name"]
        ), f'Ожидалось имя {expected_seller["company_name"]}'


@allure.feature("Получение пользователя")
@allure.story("Попытка получения пользователя с невалидным ID")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_seller_id, expected_status, "
    "expected_error_type, expected_error_keyword",
    [
        ("invalid", 422, "int_parsing", "integer"),
        ("10.5", 422, "int_parsing", "integer"),
        (-1, 422, "greater_than", "positive"),
        (0, 422, "greater_than", "positive"),
        (999999999, 404, "not_found", "not found"),
    ],
)
def test_get_seller_invalid_id(
        api_client, invalid_seller_id,
        expected_status,
        expected_error_type,
        expected_error_keyword
):
    with (allure.step(
            f"Пытаемся получить продавца с невалидным ID:"
            f" {invalid_seller_id}"
    )):
        response = api_client.get_seller(invalid_seller_id)

        with allure.step(f"Проверяем статус код (ожидаем {expected_status})"):
            assert response.status_code == expected_status, (
                f"Ожидался статус код {expected_status}, "
                f"получен {response.status_code}. Response: {response.text}"
            )

        with allure.step("Анализируем тело ошибки"):
            error_data = response.json()

            if expected_status == 422:
                assert "detail" in error_data
                assert isinstance(error_data["detail"], list)

                seller_id_errors = [
                    error for error in error_data["detail"]
                    if "seller_id" in error.get("loc", [])
                ]

                assert len(seller_id_errors) > 0, \
                    "Не найдены ошибки для seller_id"

                error_msg = str(seller_id_errors[0]).lower()
                assert expected_error_type in error_msg
                assert expected_error_keyword in error_msg

            elif expected_status == 404:
                assert "detail" in error_data
                error_msg = str(error_data["detail"]).lower()
                assert expected_error_keyword in error_msg
