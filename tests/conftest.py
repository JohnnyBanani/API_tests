import pytest
import requests
import sys
import os
from client.seller_client import UserClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

versions = {
    "versions": "5b1bd6b-49a2-4e74-80e4-bce55e92437b,"
    "29c6946a-9981-4fae-94db-35147e1444d5,"
    "fb8fd2d4-7f86-4891-bdc2-bf70999ce9ec"
}


@pytest.fixture(scope="session")
def api_client(request) -> UserClient:
    """Фикстура для создания клиента API"""
    session = requests.Session()
    session.headers.update(versions)
    yield UserClient(session=session)
    session.close()


@pytest.fixture()
def seller_payload():
    """Фикстура для генерации тестовых данных продавца."""
    from helpers.utils import create_seller_request

    return create_seller_request()


@pytest.fixture()
def create_seller(api_client, seller_payload):
    """Фикстура создает продавца и возвращает данные и ID."""
    resp = api_client.create_seller(seller_payload)

    if resp.status_code == 200:
        seller_id = resp.json().get("seller_id")
        if seller_id is not None:
            return seller_payload, seller_id
        else:
            pytest.fail("Идентификатор продавца в ответе не найден")
    else:
        pytest.fail(
            f"Не удалось создать продавца: "
            f"{resp.status_code} - {resp.text}"
        )


@pytest.fixture()
def seller_data_only():
    """Фикстура только для данных продавца без создания."""
    from helpers.utils import create_seller_request

    return create_seller_request()
