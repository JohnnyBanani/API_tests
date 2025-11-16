import allure
import pytest


@allure.feature("Блокировка продавца")
@allure.story("Успешная блокировка продавца")
@allure.tag("Positive")
def test_block_and_unblock_seller(api_client, create_seller):
    with allure.step("Создаём продавца через фикстуру"):
        seller_payload, seller_id = create_seller

    with allure.step("Проверяем, что продавец изначально не заблокирован"):
        initial_response = api_client.get_seller(seller_id)
        assert initial_response.json().get("is_blocked") is False

    with allure.step("Блокируем продавца"):
        block_response = api_client.block_seller(seller_id)
        assert block_response.status_code in [200, 204], (
            f"Ожидался статус код 200 или 204, "
            f"получен {block_response.status_code}"
        )

    with allure.step("Проверяем, что продавец заблокирован"):
        blocked_response = api_client.get_seller(seller_id)
        assert blocked_response.json()["is_blocked"] is True

    with allure.step("Разблокируем продавца"):
        unblock_response = api_client.unblock_seller(seller_id)
    assert unblock_response.status_code in [200, 204], (
        f"Ожидался статус код 200 или 204, "
        f"получен {unblock_response.status_code}"
    )

    with allure.step("Проверяем, что продавец разблокирован"):
        unblocked_response = api_client.get_seller(seller_id)
        assert unblocked_response.json()["is_blocked"] is False


@allure.feature("Блокировка продавца")
@allure.story("Попытка блокировки продавца с невалидным ID")
@allure.tag("Negative")
@pytest.mark.parametrize(
    "invalid_seller_id, expected_status, expected_error_pattern",
    [
        (999999, 404, "Seller not found"),
        (-1, 404, "Seller not found"),
        (0, 404, "Seller not found"),
    ],
)
def test_block_seller_invalid_id(
    api_client, invalid_seller_id,
        expected_status,
        expected_error_pattern
):
    with allure.step(
        f"Пытаемся блокировать продавца с невалидным ID: "
        f"{invalid_seller_id}"
    ):
        response = api_client.block_seller(invalid_seller_id)

    with allure.step("Проверяем статус код"):
        assert (
            response.status_code == expected_status
        ), f"Ожидался {expected_status}, получен {response.status_code}"

    with allure.step("Проверяем сообщение об ошибке"):
        if response.status_code in [400, 404, 422]:
            error_data = response.json()
            allure.attach(str(error_data), name="Тело ошибки")

            if isinstance(error_data, list):
                error_found = any(
                    expected_error_pattern in str(error_item)
                    for error_item in error_data
                )
                assert error_found, (
                    f"Ожидаемый текст "
                    f"{expected_error_pattern}'"
                    f" не найден в: {error_data}"
                )
            else:
                assert "detail" in error_data
                assert expected_error_pattern in error_data["detail"], (
                    f"Ожидаемый текст '{expected_error_pattern}"
                    f" не найден в: {error_data['detail']}"
                )
