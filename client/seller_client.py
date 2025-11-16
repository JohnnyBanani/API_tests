import allure
import requests
from typing import Optional
from config import SELLER_SERVICE_HOST


class UserClient:
    def __init__(self, session: requests.Session,
                 headers: Optional[dict] = None):
        self.session = session
        if headers:
            self.session.headers.update(headers)
        self.base_url = SELLER_SERVICE_HOST

    @allure.step("Создание продавца")
    def create_seller(self, payload: dict) -> requests.Response:
        url = f"{self.base_url}/create_seller"
        return self.session.post(url, json=payload)

    @allure.step("Получение продавца")
    def get_seller(self, seller_id: int) -> requests.Response:
        url = f"{self.base_url}/get_seller?seller_id={seller_id}"
        return self.session.get(url)

    @allure.step("Блокировка продавца")
    def block_seller(self, seller_id: int) -> requests.Response:
        url = f"{self.base_url}/block_seller"
        return self.session.patch(
            url, json={"seller_id": seller_id, "is_blocked": True}
        )

    @allure.step("Разблокировка продавца")
    def unblock_seller(self, seller_id: int) -> requests.Response():
        url = f"{self.base_url}/block_seller"
        return self.session.patch(
            url, json={"seller_id": seller_id, "is_blocked": False}
        )

    @allure.step("Удаление продавца")
    def delete_seller(self, seller_id: int) -> requests.Response:
        url = f"{self.base_url}/delete/{seller_id}"
        return self.session.delete(url)
