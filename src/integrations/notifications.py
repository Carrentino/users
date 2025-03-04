from helpers.clients.http_client import BaseApiClient


class NotificationsClient(BaseApiClient):

    async def send_email_code(self, email: str, code: str) -> None:
        # TODO: сделать когда будет готов сервис уведомлений
        pass
