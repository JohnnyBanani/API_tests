import allure
import pytest


@allure.feature("Удаление продавца")
@allure.story("Успешное удаление пользователя")
@allure.tag("Positive")
def test_delete_seller_success(api_client, create_seller):
    with allure.step("Создаём продавца через фикстуру"):
        seller_payload, seller_id = create_seller

    with allure.step("Проверяем перед удалением, что продавец существует"):
        get_response_before = api_client.get_seller(seller_id)
        assert get_response_before.status_code == 200

    with allure.step("Удаляем продавца"):
        response = api_client.delete_seller(seller_id)

    with allure.step("Проверяем статус код"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    with allure.step("Проверяем, что продавец удалён"):
        get_response = api_client.get_seller(seller_id)

    with allure.step("Проверяем статус код, что продавец не найден"):
        assert (
            get_response.status_code == 404
        ), f"Ожидался 404, получен {get_response.status_code}"


@allure.feature("Удаление продавца")
@allure.story("Попытка удалить продавца с невалидными данными")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_seller_id, expected_status, expected_error_pattern",
    [
        ("abc", 422, "valid integer"),
        (-1, 404, "Seller not found"),
        (999999, 404, "Seller not found"),
    ],
)
def test_delete_seller_invalid_id(
    api_client, invalid_seller_id, expected_status, expected_error_pattern
):
    with allure.step(
        f"Пытаемся удалить продавца с невалидным ID:" f" {invalid_seller_id}"
    ):
        response = api_client.delete_seller(invalid_seller_id)

    with allure.step("Проверяем статус код"):
        assert (
            response.status_code == expected_status
        ), f"Ожидался {expected_status}, получен {response.status_code}"

    with allure.step("Проверяем наличие сообщения об ошибке"):
        if response.status_code >= 400 and response.text:
            assert expected_error_pattern in response.text, (
                f"Ожидаемый текст '{expected_error_pattern}'"
                f" не найден в: {response.text}"
            )
