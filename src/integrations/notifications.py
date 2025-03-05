from helpers.clients.http_client import BaseApiClient


class NotificationsClient(BaseApiClient):
    _base_url = ''

    async def send_email_code(self, email: str, code: str) -> None:
        # TODO: сделать когда будет готов сервис уведомлений
        pass
